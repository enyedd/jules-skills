#!/bin/bash
# Usage: ./git_curl_changes.sh <repo> <branch> <file-path>

REPO=$1
BRANCH=$2
FILE_PATH=$3
LOG_FILE="._/jules/logs/tool-calls.md"

# Function to get current repo info
get_current_repo() {
    git remote get-url origin | sed -E 's/.*github.com[:\/]//;s/\.git$//'
}

# Function to get current branch
get_current_branch() {
    git branch --show-current
}

if [ -z "$REPO" ] || [ "$REPO" == "." ]; then
    REPO=$(get_current_repo)
fi

if [ -z "$BRANCH" ] || [ "$BRANCH" == "." ]; then
    BRANCH=$(get_current_branch)
fi

if [ -z "$FILE_PATH" ]; then
    echo "Usage: $0 <repo> <branch> <file-path>"
    exit 1
fi

REPO_URL="https://api.github.com/repos/$REPO/contents"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# 1. Download the remote version to a temporary file
TEMP_FILE=$(mktemp)
echo "Check for Changes in repo $REPO branch $BRANCH file $FILE_PATH"
echo "| changes ($FILE_PATH on $BRANCH in $REPO) | YES | - |" >> "$LOG_FILE"

curl -L -f -s -H "Accept: application/vnd.github.v3.raw" -H "Authorization: token $GITHUB_PAT" "$REPO_URL/$FILE_PATH?ref=$BRANCH" -o "$TEMP_FILE"

if [ $? -eq 0 ]; then
    # SUCCESS
    echo "| changes ($FILE_PATH on $BRANCH in $REPO) | SUCCESS | - |" >> "$LOG_FILE"
else
    # FAILURE
    ERROR_MSG="FAILED: Check GITHUB_PAT env (key still valid) and/or Path ($REPO_URL/$FILE_PATH?ref=$BRANCH)."
    echo "| changes ($FILE_PATH on $BRANCH in $REPO) | NO | $ERROR_MSG |" >> "$LOG_FILE"
    echo "$ERROR_MSG" >&2
    rm "$TEMP_FILE"
    exit 1
fi

# 2. Run the diff between the temporary file and your local file
diff -u "$TEMP_FILE" "$FILE_PATH"

# 3. Clean up
rm "$TEMP_FILE"
