#!/usr/bin/env python3
import requests
import os
import json
import sys
import argparse
import time
import random

API_BASE_URL = "https://jules.googleapis.com/v1alpha"

class JulesAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("JULES_API_KEY")
        if not self.api_key:
            raise ValueError("JULES_API_KEY not found in environment or arguments.")
        self.headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def request_with_retry(self, method, url, max_retries=5, **kwargs):
        """Execute a request with exponential backoff for transient errors."""
        retries = 0
        while retries < max_retries:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            if response.status_code in [429, 503]:
                wait_time = (2 ** retries) + random.random()
                sys.stderr.write(f"Transient error {response.status_code}. Retrying in {wait_time:.2f}s...\n")
                time.sleep(wait_time)
                retries += 1
                continue

            try:
                response.raise_for_status()
                if response.status_code == 204:
                    return {"status": "success"}
                return response.json()
            except requests.exceptions.HTTPError as e:
                return {
                    "error": str(e),
                    "status_code": response.status_code,
                    "response": response.text
                }

        return {"error": "Max retries reached", "status_code": response.status_code}

    def list_sources(self):
        url = f"{API_BASE_URL}/sources"
        return self.request_with_retry("GET", url)

    def list_sessions(self, page_size=10):
        url = f"{API_BASE_URL}/sessions"
        params = {"pageSize": page_size}
        return self.request_with_retry("GET", url, params=params)

    def get_session(self, session_id):
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"
        url = f"{API_BASE_URL}/{session_id}"
        return self.request_with_retry("GET", url)

    def _filter_activities(self, activities, originator=None, activity_type=None):
        filtered = []
        for act in activities:
            if originator and act.get("originator") != originator:
                continue
            if activity_type:
                if activity_type not in act:
                    continue
            filtered.append(act)
        return filtered

    def list_activities(self, session_id, page_size=30, page_token=None, originator=None, activity_type=None):
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"
        url = f"{API_BASE_URL}/{session_id}/activities"

        all_filtered = []
        current_token = page_token

        while len(all_filtered) < page_size:
            params = {"pageSize": 100 if (originator or activity_type) else page_size}
            if current_token:
                params["pageToken"] = current_token

            data = self.request_with_retry("GET", url, params=params)
            if "error" in data:
                return data

            activities = data.get("activities", [])
            filtered = self._filter_activities(activities, originator, activity_type)
            all_filtered.extend(filtered)

            current_token = data.get("nextPageToken")
            if not current_token or not (originator or activity_type):
                break

        return {
            "activities": all_filtered[:page_size],
            "nextPageToken": current_token
        }

    def list_all_activities(self, session_id, originator=None, activity_type=None):
        """Automatically paginates through all activities."""
        all_activities = []
        page_token = None
        while True:
            # Use a large page size for efficiency
            data = self.list_activities(session_id, page_size=100, page_token=page_token, originator=originator, activity_type=activity_type)
            if "error" in data:
                return data

            if "activities" in data:
                all_activities.extend(data["activities"])

            page_token = data.get("nextPageToken")
            if not page_token:
                break
        return {"activities": all_activities}

    def get_latest_activities(self, session_id, count=10, originator=None, activity_type=None):
        """Optimized retrieval of the most recent activities by jumping through pages to the end."""
        page_token = None
        last_matching_activities = []

        # Traverse to the end of the stream
        while True:
            # We use a large page size to reach the end quickly
            url = f"{API_BASE_URL}/{(session_id if session_id.startswith('sessions/') else f'sessions/{session_id}')}/activities"
            params = {"pageSize": 100}
            if page_token:
                params["pageToken"] = page_token

            data = self.request_with_retry("GET", url, params=params)
            if "error" in data:
                return data

            activities = data.get("activities", [])
            filtered = self._filter_activities(activities, originator, activity_type)

            if filtered:
                last_matching_activities.extend(filtered)
                if len(last_matching_activities) > count:
                    last_matching_activities = last_matching_activities[-count:]

            page_token = data.get("nextPageToken")
            if not page_token:
                break

        return {"activities": last_matching_activities}

    def poll_new_activities(self, session_id, last_processed_id=None, last_page_token=None, originator=None, activity_type=None):
        """
        Poll only new activities since last_processed_id or from last_page_token.
        """
        new_activities = []
        current_token = last_page_token
        latest_valid_token = last_page_token

        found_last_id = (last_processed_id is None)

        while True:
            url = f"{API_BASE_URL}/{(session_id if session_id.startswith('sessions/') else f'sessions/{session_id}')}/activities"
            params = {"pageSize": 100}
            if current_token:
                params["pageToken"] = current_token

            data = self.request_with_retry("GET", url, params=params)
            if "error" in data:
                return data

            activities = data.get("activities", [])
            for act in activities:
                if not found_last_id:
                    if act.get("id") == last_processed_id:
                        found_last_id = True
                    continue
                new_activities.append(act)

            next_token = data.get("nextPageToken")
            if next_token:
                latest_valid_token = next_token
                current_token = next_token
            else:
                break

        filtered = self._filter_activities(new_activities, originator, activity_type)

        return {
            "activities": filtered,
            "lastPageToken": latest_valid_token,
            "lastId": new_activities[-1].get("id") if new_activities else last_processed_id
        }

    def wait_for(self, session_id, originator=None, activity_type=None, timeout=300, poll_interval=5):
        """Blocks until an activity matching the filter appears, or timeout is reached."""
        start_time = time.time()

        # Determine the starting point (the current end)
        tail = self.get_latest_activities(session_id, count=1)
        last_id = None
        if tail.get("activities"):
            last_id = tail["activities"][-1].get("id")

        # We also need a token to avoid historical scan
        # Finding the last token...
        last_token = None
        url = f"{API_BASE_URL}/{(session_id if session_id.startswith('sessions/') else f'sessions/{session_id}')}/activities"
        params = {"pageSize": 100}
        while True:
            d = self.request_with_retry("GET", url, params=params)
            if "error" in d: break
            nt = d.get("nextPageToken")
            if nt:
                params["pageToken"] = nt
                last_token = nt
            else:
                break

        sys.stderr.write(f"Waiting for activity (originator={originator}, type={activity_type}) in {session_id}...\n")

        while time.time() - start_time < timeout:
            result = self.poll_new_activities(session_id, last_processed_id=last_id, last_page_token=last_token, originator=originator, activity_type=activity_type)
            if "error" in result:
                return result

            if result.get("activities"):
                return {"activities": result["activities"]}

            last_id = result.get("lastId")
            last_token = result.get("lastPageToken")

            time.sleep(poll_interval)

        return {"error": "Timeout reached waiting for activity", "status": "timeout"}

    def send_message(self, session_id, prompt):
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"
        url = f"{API_BASE_URL}/{session_id}:sendMessage"
        data = {"prompt": prompt}
        return self.request_with_retry("POST", url, json=data)

def main():
    parser = argparse.ArgumentParser(description="Jules API Skill Tool")
    parser.add_argument("--session_id", help="Session ID (defaults to JULES_SESSION_ID env var)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    subparsers.add_parser("list_sources", help="List available sources")

    list_sessions_parser = subparsers.add_parser("list_sessions", help="List sessions")
    list_sessions_parser.add_argument("--page_size", type=int, default=10, help="Number of sessions to list")

    get_session_parser = subparsers.add_parser("get_session", help="Get session details")
    get_session_parser.add_argument("session_id", nargs='?', help="Session ID or full name")

    list_activities_parser = subparsers.add_parser("list_activities", help="List session activities")
    list_activities_parser.add_argument("session_id", nargs='?', help="Session ID or full name")
    list_activities_parser.add_argument("--page_size", type=int, default=30, help="Number of activities to list")
    list_activities_parser.add_argument("--page_token", help="Token for the next page")
    list_activities_parser.add_argument("--originator", choices=['user', 'agent'], help="Filter by originator")
    list_activities_parser.add_argument("--type", help="Filter by activity type (e.g. userMessage, agentMessaged)")
    list_activities_parser.add_argument("--tail", action="store_true", help="Jump to the end and return only the latest page")

    list_all_parser = subparsers.add_parser("list_all_activities", help="List all session activities (auto-paginated)")
    list_all_parser.add_argument("session_id", nargs='?', help="Session ID or full name")
    list_all_parser.add_argument("--originator", choices=['user', 'agent'], help="Filter by originator")
    list_all_parser.add_argument("--type", help="Filter by activity type")

    latest_parser = subparsers.add_parser("get_latest_activities", help="Get the most recent activities (optimized)")
    latest_parser.add_argument("session_id", nargs='?', help="Session ID or full name")
    latest_parser.add_argument("--count", type=int, default=10, help="Number of recent activities to return")
    latest_parser.add_argument("--originator", choices=['user', 'agent'], help="Filter by originator")
    latest_parser.add_argument("--type", help="Filter by activity type")

    poll_parser = subparsers.add_parser("poll_new", help="Poll only new activities")
    poll_parser.add_argument("session_id", nargs='?', help="Session ID")
    poll_parser.add_argument("--last_id", help="Last processed activity ID")
    poll_parser.add_argument("--last_token", help="Last received page token")
    poll_parser.add_argument("--originator", choices=['user', 'agent'], help="Filter by originator")
    poll_parser.add_argument("--type", help="Filter by activity type")

    wait_parser = subparsers.add_parser("wait_for", help="Wait for a specific activity to appear")
    wait_parser.add_argument("session_id", nargs='?', help="Session ID")
    wait_parser.add_argument("--originator", choices=['user', 'agent'], help="Filter by originator")
    wait_parser.add_argument("--type", help="Filter by activity type")
    wait_parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")

    send_message_parser = subparsers.add_parser("send_message", help="Send a message to a session")
    send_message_parser.add_argument("session_id", nargs='?', help="Session ID or full name")
    send_message_parser.add_argument("prompt", help="Message text")

    args = parser.parse_args()

    # Determine session_id from flags, positional, or environment
    session_id = args.session_id or (getattr(args, 'session_id', None) if hasattr(args, 'session_id') else None) or os.environ.get("JULES_SESSION_ID")

    try:
        api = JulesAPI()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.command == "list_sources":
        print(json.dumps(api.list_sources(), indent=2))
    elif args.command == "list_sessions":
        print(json.dumps(api.list_sessions(args.page_size), indent=2))
    elif args.command == "get_session":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.get_session(sid), indent=2))
    elif args.command == "list_activities":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        if args.tail:
            print(json.dumps(api.get_latest_activities(sid, args.page_size, args.originator, args.type), indent=2))
        else:
            print(json.dumps(api.list_activities(sid, args.page_size, args.page_token, args.originator, args.type), indent=2))
    elif args.command == "list_all_activities":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.list_all_activities(sid, args.originator, args.type), indent=2))
    elif args.command == "get_latest_activities":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.get_latest_activities(sid, args.count, args.originator, args.type), indent=2))
    elif args.command == "poll_new":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.poll_new_activities(sid, args.last_id, args.last_token, args.originator, args.type), indent=2))
    elif args.command == "wait_for":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.wait_for(sid, args.originator, args.type, args.timeout), indent=2))
    elif args.command == "send_message":
        sid = args.session_id or session_id
        if not sid:
            print("Error: session_id is required.")
            sys.exit(1)
        print(json.dumps(api.send_message(sid, args.prompt), indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
