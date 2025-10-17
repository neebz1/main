#!/bin/bash

# Show Top 20 GitHub Repositories
# Quick launcher for the top GitHub repos tool

echo "🌟 Top GitHub Repositories Finder 🌟"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Run the script with offline mode by default (no API rate limits)
python3 top20_github_repos.py --offline "$@"
