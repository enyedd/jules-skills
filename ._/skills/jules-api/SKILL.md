---
name: jules-api
description: Interacts with the Jules REST API to manage sources, sessions, activities, and cross-agent messaging. Use this skill when you need to communicate with other agents or inspect remote sessions.
compatibility: Requires `requests` library and `JULES_API_KEY` environment variable.
---

# Jules API Skill

This skill provides a Python-based tool to interact with the Jules REST API. It is optimized for robustness, handling long sessions with automatic pagination and efficient polling.

## Usage

The primary tool is located at `scripts/jules_skill.py`.

### Global Flags
*   `--session_id <ID>`: Specify the session ID. If omitted, it defaults to the `JULES_SESSION_ID` environment variable.

### Commands

*   **List Sources**: `./scripts/jules_skill.py list_sources`
*   **List Sessions**: `./scripts/jules_skill.py list_sessions [--page_size <SIZE>]`
*   **Get Session Details**: `./scripts/jules_skill.py get_session [<SESSION_ID>]`
*   **List Activities**: `./scripts/jules_skill.py list_activities [<SESSION_ID>] [--page_size <SIZE>] [--originator <user|agent>] [--type <TYPE>] [--tail]`
    *   `--originator`: Filter activities by who created them.
    *   `--type`: Filter by activity type (e.g., `userMessage`, `agentMessaged`, `planGenerated`).
    *   `--tail`: Jump to the end of the session and return only the latest page of results.
*   **List All Activities**: `./scripts/jules_skill.py list_all_activities [<SESSION_ID>] [--originator <user|agent>] [--type <TYPE>]` (Auto-paginated)
*   **Get Latest Activities**: `./scripts/jules_skill.py get_latest_activities [<SESSION_ID>] [--count <COUNT>] [--originator <user|agent>] [--type <TYPE>]`
*   **Poll New Activities**: `./scripts/jules_skill.py poll_new [<SESSION_ID>] [--last_id <ID>] [--last_token <TOKEN>] [--originator <user|agent>] [--type <TYPE>]`
*   **Wait For Activity**: `./scripts/jules_skill.py wait_for [<SESSION_ID>] [--originator <user|agent>] [--type <TYPE>] [--timeout <SECONDS>]`
    *   Blocks until a matching activity appears.
*   **Send Message**: `./scripts/jules_skill.py send_message [<SESSION_ID>] "<MESSAGE>"`

## Message Schema Guide

When inspecting activities, keep in mind where the actual text content lives:

| Originator | Activity Type | Content Key |
| :--- | :--- | :--- |
| `user` | `userMessage` | `.userMessage.userMessage` |
| `agent` | `agentMessaged` | `.agentMessaged.agentMessage` |
| `agent` | `planGenerated` | `.planGenerated.plan.steps[].title` |

## Polling Best Practices: Token Checkpointing

To keep polling efficient in long sessions, use **Token Checkpointing**:
1. When you first poll, record the `lastPageToken` and `lastId` from the response.
2. In the next poll, pass these back using `--last_token` and `--last_id`.
3. The script will resume from that token, avoiding a slow scan of historical data.

## Setup

Ensure you have the `requests` library installed:
```bash
pip install requests
```

Ensure the `JULES_API_KEY` is set in your environment.
