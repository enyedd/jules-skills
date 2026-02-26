#!/bin/bash
# Usage: ./git_curl_watch.sh <repo> <branch> <file_path> [interval_min] [max_checks]

REPO=$1
BRANCH=$2
FILE_PATH=$3
INTERVAL_MIN=${4:-5}
MAX_CHECKS=${5:-10}
LOG_FILE="._/jules/logs/tool-calls.md"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Calculate interval in seconds for the 'sleep' command
INTERVAL_SEC=$((INTERVAL_MIN * 60))

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for ((i=1; i<=MAX_CHECKS; i++)); do
    # Run the diff tool
    DIFF_RESULT=$("$SCRIPT_DIR/git_curl_changes.sh" "$REPO" "$BRANCH" "$FILE_PATH" 2>/dev/null)

    # Check for changes (look for + or - at the beginning of a line)
    if echo "$DIFF_RESULT" | grep -q "^[+-]"; then
        echo "| watch_changes ($FILE_PATH on $BRANCH in $REPO) | YES | Changes detected after $((i * INTERVAL_MIN)) minutes |" >> "$LOG_FILE"
        exit 0
    fi

    # If this is not the final check, wait
    if [ "$i" -lt "$MAX_CHECKS" ]; then
        sleep "$INTERVAL_SEC"
    fi
done

# When we get here, the file hasn't changed within the allowed time
echo "| watch_changes ($FILE_PATH on $BRANCH in $REPO) | NO | Timeout: no changes detected after $((INTERVAL_MIN * MAX_CHECKS)) minutes |" >> "$LOG_FILE"
exit 1
