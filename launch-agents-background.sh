#!/bin/bash
# 🚀 Launch All Agents in Background
# Runs all autonomous agents automatically

echo "🤖 Launching Autonomous Agent System..."
echo "========================================"

# Load Bitwarden credentials
source ~/.zshrc
bwload

cd /Users/nr/Documents/GitHub/main

# Create logs directory
mkdir -p logs

echo ""
echo "🚀 Starting agents..."

# Launch Deployment Agent
echo "  Starting Deployment Agent..."
python3 agents/deployment_agent.py > logs/deployment_agent.log 2>&1 &
DEPLOY_PID=$!
echo "    ✅ PID: $DEPLOY_PID"

# Wait a bit for services to start
sleep 5

# Launch Monitoring Agent
echo "  Starting Monitoring Agent..."
python3 agents/monitoring_agent.py > logs/monitoring_agent.log 2>&1 &
MONITOR_PID=$!
echo "    ✅ PID: $MONITOR_PID"

# Launch Cloud Agent (optional - uncomment if you want cloud deployment)
# echo "  Starting Cloud Agent..."
# python3 agents/cloud_agent.py > logs/cloud_agent.log 2>&1 &
# CLOUD_PID=$!
# echo "    ✅ PID: $CLOUD_PID"

echo ""
echo "="*60
echo "✅ All agents launched!"
echo "="*60
echo ""
echo "Agent PIDs:"
echo "  Deployment Agent: $DEPLOY_PID"
echo "  Monitoring Agent: $MONITOR_PID"
echo ""
echo "View logs:"
echo "  tail -f logs/deployment_agent.log"
echo "  tail -f logs/monitoring_agent.log"
echo ""
echo "Stop all agents:"
echo "  kill $DEPLOY_PID $MONITOR_PID"
echo ""
echo "Services will be available at:"
echo "  AI Mixing Engineer: http://localhost:7861"
echo "  Music Copilot: http://localhost:7860"
echo ""

# Save PIDs for easy stopping
echo "$DEPLOY_PID" > logs/deployment_agent.pid
echo "$MONITOR_PID" > logs/monitoring_agent.pid

echo "💡 Agents are now running autonomously!"
echo "   They will auto-restart services if they crash."
echo ""

