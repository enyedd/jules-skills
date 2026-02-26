---
name: git-curl
description: Unified tool for remote Git operations (commit, diff, watch) via GitHub API and curl. Use when you need to push local changes to a remote branch, compare local files with remote versions, or monitor remote files for changes. Triggers include "commit FILE to BRANCH", "compare FILE with remote", "watch FILE for changes", etc.
compatibility: Requires a `GITHUB_PAT` environment variable.
---

# Git Curl

This skill provides a unified interface for interacting with GitHub repositories using `curl` and the GitHub REST API. It combines functionalities for committing files, retrieving remote changes, and monitoring files for updates.

## Prerequisites

- `GITHUB_PAT` environment variable must be set with a valid GitHub Personal Access Token.
- Git must be configured if using defaults for repository and branch.

## Usage

All scripts support the parameters `<repo> <branch> <file>`. Use `.` for `<repo>` or `<branch>` to use the current repository or branch.

### 1. Committing Files
Push a local file to a remote branch.
- **Script**: `python3 ._/skills/git-curl/scripts/git_curl_commit.py <repo> <branch> <file> [commit-message]`
- **Example**: `python3 ._/skills/git-curl/scripts/git_curl_commit.py . . README.md "Update documentation"`

### 2. Getting Remote Changes
Compare a local file with its remote version (outputs a unified diff).
- **Script**: `bash ._/skills/git-curl/scripts/git_curl_changes.sh <repo> <branch> <file>`
- **Example**: `bash ._/skills/git-curl/scripts/git_curl_changes.sh . main src/app.py`

### 3. Waiting for Changes
Monitor a remote file until changes are detected or a timeout occurs.
- **Script**: `bash ._/skills/git-curl/scripts/git_curl_watch.sh <repo> <branch> <file> [interval_min] [max_checks]`
- **Example**: `bash ._/skills/git-curl/scripts/git_curl_watch.sh enyedd/jules-play-ground develop config.json 5 12`

## Parameters

- `<repo>`: The GitHub repository in `owner/repo` format. Use `.` for current repo.
- `<branch>`: The branch name. Use `.` for the starting/current branch.
- `<file>`: The path to the file within the repository.
- `[commit-message]`: (Optional) Message for the commit.
- `[interval_min]`: (Optional) Minutes between checks (default: 5).
- `[max_checks]`: (Optional) Maximum number of checks (default: 10).
