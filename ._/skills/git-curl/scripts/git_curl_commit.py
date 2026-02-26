import os
import base64
import json
import sys
import urllib.request
import urllib.error
import subprocess
import re

def get_current_repo_info():
    try:
        remote_v = subprocess.check_output(["git", "remote", "-v"]).decode()
        # Look for the origin fetch URL
        match = re.search(r"origin\s+(?:https://github\.com/|git@github\.com:)([^/]+)/([^/\s.]+)", remote_v)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
    except Exception as e:
        print(f"Error deriving repo info: {e}")
    return None

def get_current_branch():
    try:
        return subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()
    except Exception as e:
        print(f"Error deriving branch info: {e}")
    return None

def main():
    if len(sys.argv) < 4:
        print("Usage: python git_curl_commit.py <repo> <branch> <path> [commit_message]")
        sys.exit(1)

    repo_arg = sys.argv[1]
    branch_arg = sys.argv[2]
    path = sys.argv[3]
    commit_message = sys.argv[4] if len(sys.argv) > 4 else f"Update {path}"

    if repo_arg == "." or not repo_arg:
        repo_full = get_current_repo_info()
    else:
        repo_full = repo_arg

    if branch_arg == "." or not branch_arg:
        branch = get_current_branch()
    else:
        branch = branch_arg

    if not repo_full or not branch:
        print("Could not determine repo or branch")
        sys.exit(1)

    if "/" not in repo_full:
        print(f"Invalid repo format: {repo_full}. Expected 'owner/repo'")
        sys.exit(1)

    owner, repo = repo_full.split("/", 1)

    token = os.environ.get("GITHUB_PAT")
    if not token:
        print("GITHUB_PAT environment variable not set")
        sys.exit(1)

    print(f"Target: {owner}/{repo} on branch {branch}, file {path}")

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

    # 1. Get the current file's SHA
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")

    sha = None
    try:
        with urllib.request.urlopen(req) as response:
            file_info = json.loads(response.read().decode())
            sha = file_info["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"File {path} not found on branch {branch}. Creating new file.")
        else:
            print(f"Failed to get file info: {e.code}")
            print(e.read().decode())
            sys.exit(1)

    # 2. Read local file content
    try:
        with open(path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read local file: {path} - {e}")
        sys.exit(1)

    # 3. Update or create the file
    content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    data = {
        "message": commit_message,
        "content": content_b64,
        "branch": branch
    }
    if sha:
        data["sha"] = sha

    update_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    req = urllib.request.Request(update_url, data=json.dumps(data).encode("utf-8"), method="PUT")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201]:
                action = "updated" if sha else "created"
                print(f"Successfully {action} remote file: {path}")
            else:
                print(f"Action returned status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"Failed to push changes: {e.code}")
        print(e.read().decode())
        sys.exit(1)

if __name__ == "__main__":
    main()
