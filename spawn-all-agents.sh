#!/bin/bash
# 🚀 Spawn All Autonomous Agents
# This script launches all agents in separate Cursor terminal tabs

echo "🤖 Spawning Autonomous Agents..."
echo "=================================="

# Load Bitwarden credentials
source ~/.zshrc
bwload

# Create agents directory if it doesn't exist
mkdir -p /Users/nr/Documents/GitHub/main/agents

# Make Python agents executable
chmod +x /Users/nr/Documents/GitHub/main/agents/*.py

echo ""
echo "🚀 Launching agents in Cursor terminals..."
echo ""

# Open Cursor workspace
echo "Opening Cursor workspace..."
open -a "Cursor" /Users/nr/Documents/GitHub/main

# Wait for Cursor to open
sleep 3

# Instructions for user
echo "="*60
echo "✅ Agents are ready to launch!"
echo "="*60
echo ""
echo "In Cursor, open 3 terminal tabs and run:"
echo ""
echo "Terminal 1 - Deployment Agent:"
echo "  python3 agents/deployment_agent.py"
echo ""
echo "Terminal 2 - Cloud Agent:"
echo "  python3 agents/cloud_agent.py"
echo ""
echo "Terminal 3 - Monitoring Agent:"
echo "  python3 agents/monitoring_agent.py"
echo ""
echo "="*60
echo ""
echo "Or run all at once:"
echo "  ./launch-agents-background.sh"
echo ""


