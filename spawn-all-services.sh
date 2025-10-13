#!/bin/bash
# 🚀 Master Deployment Script
# Spawn all AI services using Bitwarden credentials

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       🚀 Spawning All AI Services from Bitwarden Creds       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Go to project directory
cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

# Load .env file
if [ -f ".env" ]; then
    echo "✅ Loading API keys from .env..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    exit 1
fi

# Kill any existing services
echo "🧹 Cleaning up existing services..."
pkill -f "ai_mixing_engineer.py" 2>/dev/null
pkill -f "logic_copilot_lite.py" 2>/dev/null
pkill -f "cloud_ai_builder.py" 2>/dev/null
pkill -f "api_server.py" 2>/dev/null
sleep 2

# Create logs directory
mkdir -p logs

echo ""
echo "Starting services..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start AI Mixing Engineer (port 7861)
echo "🎚️  [1/4] Starting AI Mixing Engineer on port 7861..."
nohup python ai_mixing_engineer.py > logs/mixing_engineer.log 2>&1 &
MIXING_PID=$!
echo "    PID: $MIXING_PID"
sleep 2

# Start Music Copilot (port 7860)
echo "🎵 [2/4] Starting Music Copilot on port 7860..."
nohup python logic_copilot_lite.py > logs/music_copilot.log 2>&1 &
COPILOT_PID=$!
echo "    PID: $COPILOT_PID"
sleep 2

# Start Cloud AI Builder (port 7862)
echo "🤖 [3/4] Starting Cloud AI Builder on port 7862..."
nohup python cloud_ai_builder.py > logs/cloud_builder.log 2>&1 &
BUILDER_PID=$!
echo "    PID: $BUILDER_PID"
sleep 2

# Start CursorDocsIndex API Server (port 8000)
echo "📚 [4/4] Starting CursorDocsIndex API on port 8000..."
cd CursorDocsIndex
nohup python api_server.py > ../logs/docs_api.log 2>&1 &
DOCS_PID=$!
echo "    PID: $DOCS_PID"
cd ..
sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏳ Waiting for services to initialize..."
sleep 8

echo ""
echo "Verifying services..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check which ports are active
ACTIVE_SERVICES=0

if lsof -nP -iTCP:7861 | grep -q LISTEN; then
    echo "✅ AI Mixing Engineer    → http://localhost:7861"
    ((ACTIVE_SERVICES++))
else
    echo "❌ AI Mixing Engineer failed to start (check logs/mixing_engineer.log)"
fi

if lsof -nP -iTCP:7860 | grep -q LISTEN; then
    echo "✅ Music Copilot         → http://localhost:7860"
    ((ACTIVE_SERVICES++))
else
    echo "❌ Music Copilot failed to start (check logs/music_copilot.log)"
fi

if lsof -nP -iTCP:7862 | grep -q LISTEN; then
    echo "✅ Cloud AI Builder      → http://localhost:7862"
    ((ACTIVE_SERVICES++))
else
    echo "❌ Cloud AI Builder failed to start (check logs/cloud_builder.log)"
fi

if lsof -nP -iTCP:8000 | grep -q LISTEN; then
    echo "✅ CursorDocsIndex API   → http://localhost:8000"
    echo "   API Docs             → http://localhost:8000/docs"
    ((ACTIVE_SERVICES++))
else
    echo "❌ CursorDocsIndex API failed to start (check logs/docs_api.log)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ACTIVE_SERVICES -eq 4 ]; then
    echo "🎉 All 4 services are running!"
    echo ""
    echo "📊 Service Dashboard:"
    echo "   • AI Mixing Engineer: http://localhost:7861"
    echo "   • Music Copilot:      http://localhost:7860"
    echo "   • Cloud AI Builder:   http://localhost:7862"
    echo "   • Docs API:           http://localhost:8000"
    echo ""
    echo "📝 Logs are in: $PROJECT_DIR/logs/"
    echo ""
    echo "To stop all services:"
    echo "   pkill -f 'ai_mixing_engineer.py|logic_copilot_lite.py|cloud_ai_builder.py|api_server.py'"
else
    echo "⚠️  Only $ACTIVE_SERVICES/4 services started successfully"
    echo ""
    echo "Check logs:"
    echo "   tail -f logs/*.log"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 🚀 Deployment Complete! 🚀                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"

