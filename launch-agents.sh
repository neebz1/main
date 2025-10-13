#!/bin/bash
# 🚀 Launch All Autonomous Agents in Cursor Terminals

echo "🤖 Launching Autonomous Agents..."
echo "=================================="
echo ""

# Load Bitwarden credentials
source ~/.zshrc
bwload

# Make agents executable
chmod +x /Users/nr/Documents/GitHub/main/agents/*.py

echo "✅ Credentials loaded"
echo ""
echo "Opening Cursor terminals with agents..."
echo ""

# Open Cursor and trigger tasks
open -a "Cursor" /Users/nr/Documents/GitHub/main

echo "✅ Agents ready!"
echo ""
echo "In Cursor, press:"
echo "  Cmd+Shift+P → Tasks: Run Task → 🚀 Launch ALL Agents"
echo ""
echo "Or run individually:"
echo "  🤖 Launch Deployment Agent"
echo "  ☁️ Launch Cloud Agent"
echo "  👁️ Launch Monitoring Agent"
echo ""

