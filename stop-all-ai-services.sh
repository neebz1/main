#!/bin/bash
# 🛑 Stop All AI Services

echo "🛑 Stopping All AI Services..."
echo "======================================"
echo ""

# Function to kill process on a port
kill_port() {
    local port=$1
    local name=$2
    local pids=$(lsof -ti:$port 2>/dev/null)

    if [ -n "$pids" ]; then
        echo "🔴 Stopping $name on port $port..."
        kill -9 $pids 2>/dev/null
        echo "   ✅ Stopped (PIDs: $pids)"
    else
        echo "⚪ $name not running on port $port"
    fi
}

# Stop all services
kill_port 7860 "Music Copilot"
kill_port 7861 "AI Mixing Engineer"
kill_port 7862 "Cloud AI Builder"
kill_port 7863 "Live AI Assistant"
kill_port 7864 "Logic AI Plugin"

echo ""
echo "======================================"
echo "✅ All AI services stopped!"
echo "======================================"
echo ""
echo "To restart: ./spawn-all-ai-services.sh"
echo ""


