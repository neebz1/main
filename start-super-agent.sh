#!/bin/bash
# 🦸 Super Agent Launcher
# Coordinates all AI agents to work simultaneously

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🦸 Super Agent Orchestration System 🦸                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for Python and dependencies
echo "🔍 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install super agent dependencies if needed
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "📦 Installing super agent dependencies..."
    pip3 install psutil pyyaml 2>/dev/null || {
        echo "⚠️  Could not install dependencies automatically"
        echo "   Please run: pip3 install psutil pyyaml"
    }
fi

echo "✅ Dependencies OK"
echo ""

# Show menu
echo "Choose mode:"
echo "1) Start super agent orchestrator only"
echo "2) Start orchestrator + music agents"
echo "3) Start orchestrator + all web agents"
echo "4) Show agent status"
echo "5) Stop all agents"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🦸 Starting Super Agent Orchestrator..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        python3 super_agent/orchestrator.py
        ;;
    
    2)
        echo ""
        echo "🎵 Starting Super Agent + Music Agents..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Start orchestrator in background
        python3 super_agent/orchestrator.py &
        ORCHESTRATOR_PID=$!
        sleep 2
        
        # Start music agents
        if [ -f "./start-music-ai.sh" ]; then
            echo "🎵 Starting Logic Copilot (port 7860)..."
            ./start-music-ai.sh &
        fi
        
        if [ -f "./start-ai-mixing-engineer.sh" ]; then
            echo "🎚️ Starting AI Mixing Engineer (port 7861)..."
            ./start-ai-mixing-engineer.sh &
        fi
        
        echo ""
        echo "✅ Super Agent System Running!"
        echo ""
        echo "Components:"
        echo "  🎭 Orchestrator: PID $ORCHESTRATOR_PID"
        echo "  🎵 Logic Copilot: http://localhost:7860"
        echo "  🎚️ Mixing Engineer: http://localhost:7861"
        echo ""
        echo "IDE Agents (use directly):"
        echo "  💻 Cline: Open in Cursor (⌘⇧P → Cline)"
        echo "  ✨ Cursor AI: ⌘K (generate) ⌘L (chat)"
        echo ""
        echo "Press Ctrl+C to stop all agents"
        
        # Wait for user to stop
        wait $ORCHESTRATOR_PID
        ;;
    
    3)
        echo ""
        echo "🚀 Starting Super Agent + All Web Agents..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Start orchestrator
        python3 super_agent/orchestrator.py &
        ORCHESTRATOR_PID=$!
        sleep 2
        
        # Start music agents
        if [ -f "./start-music-ai.sh" ]; then
            echo "🎵 Starting Logic Copilot..."
            ./start-music-ai.sh &
            sleep 1
        fi
        
        if [ -f "./start-ai-mixing-engineer.sh" ]; then
            echo "🎚️ Starting AI Mixing Engineer..."
            ./start-ai-mixing-engineer.sh &
            sleep 1
        fi
        
        # Start docs agent
        if [ -d "./CursorDocsIndex" ]; then
            echo "📚 Starting Docs Agent..."
            cd CursorDocsIndex
            python3 api_server.py &
            cd ..
            sleep 1
        fi
        
        echo ""
        echo "✅ Complete Super Agent System Running!"
        echo ""
        echo "Web Services:"
        echo "  🎵 Logic Copilot: http://localhost:7860"
        echo "  🎚️ Mixing Engineer: http://localhost:7861"
        echo "  📚 Docs Agent API: http://localhost:8000"
        echo "  📖 Docs Agent Swagger: http://localhost:8000/docs"
        echo ""
        echo "IDE Agents:"
        echo "  💻 Cline: ⌘⇧P → Cline"
        echo "  ✨ Cursor AI: ⌘K / ⌘L"
        echo ""
        echo "Press Ctrl+C to stop all"
        
        wait $ORCHESTRATOR_PID
        ;;
    
    4)
        echo ""
        echo "📊 Agent Status"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Check what's running
        echo ""
        echo "Web Services:"
        
        if lsof -i:7860 &>/dev/null; then
            echo "  ✅ Logic Copilot (7860) - RUNNING"
        else
            echo "  ⭕ Logic Copilot (7860) - STOPPED"
        fi
        
        if lsof -i:7861 &>/dev/null; then
            echo "  ✅ AI Mixing Engineer (7861) - RUNNING"
        else
            echo "  ⭕ AI Mixing Engineer (7861) - STOPPED"
        fi
        
        if lsof -i:8000 &>/dev/null; then
            echo "  ✅ Docs Agent (8000) - RUNNING"
        else
            echo "  ⭕ Docs Agent (8000) - STOPPED"
        fi
        
        echo ""
        echo "IDE Agents (check in Cursor):"
        echo "  💻 Cline: ⌘⇧P → Cline"
        echo "  ✨ Cursor AI: ⌘K / ⌘L"
        echo ""
        ;;
    
    5)
        echo ""
        echo "🛑 Stopping all agents..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Kill processes on known ports
        for port in 7860 7861 8000 9000; do
            if lsof -i:$port &>/dev/null; then
                echo "  Stopping service on port $port..."
                lsof -ti:$port | xargs kill -9 2>/dev/null || true
            fi
        done
        
        echo ""
        echo "✅ All web agents stopped"
        echo "   (IDE agents remain active in Cursor)"
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              🦸 Super Agent System 🦸                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
