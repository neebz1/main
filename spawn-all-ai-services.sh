#!/bin/bash
# 🚀 Master AI Services Spawner
# Loads credentials from Bitwarden and starts ALL AI services

echo "🚀 Starting ALL AI Services..."
echo "======================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Step 1: Load credentials from Bitwarden
echo "🔐 Step 1: Loading credentials from Bitwarden..."
echo ""

# Source shell configuration to get bwload function
source ~/.zshrc 2>/dev/null

# Load Bitwarden credentials file
if [ -f "$HOME/Documents/GitHub/main/.bitwarden-oauth" ]; then
    source "$HOME/Documents/GitHub/main/.bitwarden-oauth"
else
    echo "❌ Bitwarden credentials file not found!"
    echo "   Expected: $HOME/Documents/GitHub/main/.bitwarden-oauth"
    exit 1
fi

# Run bwload to unlock vault and load API keys
if ! bwload 2>/dev/null; then
    echo "❌ Failed to load API keys from Bitwarden"
    echo "   Try running: bwload"
    exit 1
fi

echo ""

# Step 2: Create/Update .env file
echo "📝 Step 2: Creating .env file with credentials..."
echo ""

cat > .env << EOF
# API Keys loaded from Bitwarden
# Generated on $(date)

# OpenRouter - Multi-model API access
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}

# Google/Gemini API
GOOGLE_API_KEY=${GOOGLE_API_KEY}

# Moonshot/Kimi API
MOONSHOT_API_KEY=${MOONSHOT_API_KEY}

# OpenAI API
OPENAI_API_KEY=${OPENAI_API_KEY}

# Anthropic/Claude API
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Hugging Face Token
HF_TOKEN=${HF_TOKEN}

# GitHub Token
GITHUB_TOKEN=${GITHUB_TOKEN}

# Brave Search API
BRAVE_API_KEY=${BRAVE_API_KEY}
EOF

echo "✅ .env file created with all API keys"
echo ""

# Step 3: Check Python virtual environment
echo "🐍 Step 3: Checking Python environment..."
echo ""

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "✅ Python environment ready"
echo ""

# Step 4: Install dependencies
echo "📦 Step 4: Installing/Updating dependencies..."
echo ""

echo "   Installing base requirements..."
pip install -q -r requirements.txt 2>/dev/null || echo "   (base requirements already satisfied)"

echo "   Installing mixing engineer requirements..."
pip install -q -r requirements_mixing.txt 2>/dev/null || echo "   (mixing requirements already satisfied)"

echo "   Installing music copilot requirements..."
pip install -q -r requirements_lite.txt 2>/dev/null || echo "   (copilot requirements already satisfied)"

echo "   Installing live assistant requirements..."
pip install -q -r requirements_live_ai.txt 2>/dev/null || echo "   (live AI requirements already satisfied)"

echo "   Installing Logic plugin requirements..."
pip install -q -r requirements_plugin.txt 2>/dev/null || echo "   (plugin requirements already satisfied)"

echo ""
echo "✅ All dependencies installed"
echo ""

# Step 5: Start all services
echo "🎉 Step 5: Starting all AI services..."
echo ""
echo "======================================"
echo "Services will start in the background"
echo "======================================"
echo ""

# Create logs directory
mkdir -p logs

# Kill any existing processes on these ports
echo "🧹 Cleaning up old processes..."
lsof -ti:7860 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:7861 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:7862 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:7863 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:7864 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

# 1. Start AI Mixing Engineer (Port 7861)
echo "🎚️  Starting AI Mixing Engineer (Port 7861)..."
nohup python ai_mixing_engineer.py > logs/mixing-engineer.log 2>&1 &
MIXING_PID=$!
echo "   PID: $MIXING_PID"

sleep 2

# 2. Start Music Copilot (Port 7860)
echo "🎵 Starting Music Copilot (Port 7860)..."
nohup python logic_copilot_lite.py > logs/music-copilot.log 2>&1 &
COPILOT_PID=$!
echo "   PID: $COPILOT_PID"

sleep 2

# 3. Start Cloud AI Builder (Port 7862)
echo "☁️  Starting Cloud AI Builder (Port 7862)..."
nohup python cloud_ai_builder.py > logs/cloud-builder.log 2>&1 &
CLOUD_PID=$!
echo "   PID: $CLOUD_PID"

sleep 2

# 4. Start Live AI Assistant (Port 7863)
echo "🎤 Starting Live AI Assistant (Port 7863)..."
nohup python live_ai_assistant.py > logs/live-assistant.log 2>&1 &
LIVE_PID=$!
echo "   PID: $LIVE_PID"

sleep 2

# 5. Start Logic AI Plugin (Port 7864)
echo "🎹 Starting Logic AI Plugin (Port 7864)..."
nohup python logic_ai_plugin.py > logs/logic-plugin.log 2>&1 &
PLUGIN_PID=$!
echo "   PID: $PLUGIN_PID"

echo ""
echo "⏳ Waiting for services to initialize..."
sleep 5

# Step 6: Verify services
echo ""
echo "======================================"
echo "🔍 Checking Service Status..."
echo "======================================"
echo ""

check_service() {
    local port=$1
    local name=$2
    local pid=$3

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ $name is running on port $port (PID: $pid)"
        return 0
    else
        echo "❌ $name failed to start on port $port"
        return 1
    fi
}

SERVICES_OK=0

check_service 7861 "AI Mixing Engineer" $MIXING_PID && ((SERVICES_OK++))
check_service 7860 "Music Copilot" $COPILOT_PID && ((SERVICES_OK++))
check_service 7862 "Cloud AI Builder" $CLOUD_PID && ((SERVICES_OK++))
check_service 7863 "Live AI Assistant" $LIVE_PID && ((SERVICES_OK++))
check_service 7864 "Logic AI Plugin" $PLUGIN_PID && ((SERVICES_OK++))

echo ""
echo "======================================"
echo "🎉 Deployment Complete!"
echo "======================================"
echo ""
echo "Services Running: $SERVICES_OK/5"
echo ""
echo "📱 Access Your AI Services:"
echo "   🎚️  AI Mixing Engineer:  http://localhost:7861"
echo "   🎵 Music Copilot:        http://localhost:7860"
echo "   ☁️  Cloud AI Builder:     http://localhost:7862"
echo "   🎤 Live AI Assistant:    http://localhost:7863"
echo "   🎹 Logic AI Plugin:      http://localhost:7864"
echo ""
echo "📊 View Logs:"
echo "   tail -f logs/mixing-engineer.log"
echo "   tail -f logs/music-copilot.log"
echo "   tail -f logs/cloud-builder.log"
echo "   tail -f logs/live-assistant.log"
echo "   tail -f logs/logic-plugin.log"
echo ""
echo "🛑 Stop All Services:"
echo "   ./stop-all-ai-services.sh"
echo ""
echo "======================================"
echo "✨ Your complete AI suite is now live!"
echo "======================================"


