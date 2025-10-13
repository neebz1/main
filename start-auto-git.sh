#!/bin/bash

# Start Autonomous Git Watcher
# Automatically commits and pushes changes every 5 minutes

echo "🤖 Starting Autonomous Git Watcher..."
echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment if it exists
if [ -d "$DIR/venv" ]; then
    source "$DIR/venv/bin/activate"
fi

# Check if running in a git repository
if [ ! -d "$DIR/.git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Start the watcher
python3 "$DIR/auto_git_watcher.py" --dir "$DIR" "$@"
