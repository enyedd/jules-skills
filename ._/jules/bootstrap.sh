#!/bin/bash

# Jules Agent Bootstrap Script
# This script initializes the agent context by loading configuration and discovering skills.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_PY="$SCRIPT_DIR/_bootstrap.py"

if [ ! -f "$BOOTSTRAP_PY" ]; then
    echo "Error: bootstrap.py not found in $SCRIPT_DIR"
    exit 1
fi

# Run the python bootstrap script
python3 "$BOOTSTRAP_PY"

echo ""
echo "Bootstrap complete. You are ready to work."
