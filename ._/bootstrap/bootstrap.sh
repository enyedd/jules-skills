#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")/../.."

# Set permissions if needed
sudo chmod +x ._/bootstrap/bootstrap.py

# Run the discovery script
# The output of this script is captured by Jules during startup
python3 ._/bootstrap/bootstrap.py

if [ $? -eq 0 ]; then
    echo "ASP Discovery successful."
else
    echo "ASP Discovery failed." >&2
    exit 1
fi