#!/bin/bash
# 💬 Talk to Your Agents - No Coding Required!

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                 💬 AGENT COMMAND CENTER                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose your interface:"
echo ""
echo "  1) 💬 Chat Agent     - Type commands"
echo "  2) 🎤 Voice Agent    - Speak commands (hands-free!)"
echo "  3) 🚀 Quick Deploy   - Deploy everything now"
echo "  4) 📊 Quick Status   - Check what's running"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting Chat Agent..."
        python3 agents/conversational_agent.py
        ;;
    2)
        echo ""
        echo "Starting Voice Agent..."
        python3 agents/voice_agent.py
        ;;
    3)
        echo ""
        echo "🚀 Deploying everything..."
        source ~/.zshrc && bwload
        python3 agents/deployment_agent.py &
        echo "✅ Services deploying in background!"
        echo ""
        echo "Visit:"
        echo "  - AI Mixing Engineer: http://localhost:7861"
        echo "  - Music Copilot: http://localhost:7860"
        ;;
    4)
        echo ""
        echo "📊 Checking status..."
        echo ""

        if curl -s http://localhost:7861 > /dev/null 2>&1; then
            echo "🟢 AI Mixing Engineer: Running (http://localhost:7861)"
        else
            echo "🔴 AI Mixing Engineer: Stopped"
        fi

        if curl -s http://localhost:7860 > /dev/null 2>&1; then
            echo "🟢 Music Copilot: Running (http://localhost:7860)"
        else
            echo "🔴 Music Copilot: Stopped"
        fi

        echo ""
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

