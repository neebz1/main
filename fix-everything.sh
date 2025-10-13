#!/bin/bash
# 🆘 EMERGENCY FIX SCRIPT
# Run this when nothing else works!

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🆘 EMERGENCY FIX - Your Last Hope!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Check Python
echo "🔍 Step 1: Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Python found: $PYTHON_VERSION"
else
    echo "   ❌ Python3 not found! Please install Python 3.8+"
    exit 1
fi
echo ""

# Step 2: Check/Create .env file
echo "🔍 Step 2: Checking API keys..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
    
    # Check if keys are actually configured
    if grep -q "API_KEY=your_" .env; then
        echo "   ⚠️  Warning: .env file has placeholder values"
        echo "   📝 Edit .env and add your real API keys"
    else
        echo "   ✅ API keys appear to be configured"
    fi
else
    echo "   ⚠️  .env file not found"
    if [ -f "config_example.txt" ]; then
        echo "   📝 Creating .env from config_example.txt..."
        cp config_example.txt .env
        echo "   ✅ Created .env - please add your API keys!"
    else
        echo "   📝 Creating blank .env file..."
        cat > .env << 'EOF'
# AI API Keys - Add your keys here
TOGETHER_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
HUGGINGFACE_TOKEN=
EOF
        echo "   ✅ Created .env - please add your API keys!"
    fi
fi
echo ""

# Step 3: Install dependencies
echo "🔍 Step 3: Installing/Updating dependencies..."
echo "   This might take a minute..."

# Core dependencies
pip3 install --upgrade pip -q 2>&1 | grep -v "already satisfied" | tail -3

CORE_DEPS="gradio>=4.0.0 together>=1.0.0 python-dotenv>=1.0.0"
echo "   Installing core dependencies..."
pip3 install $CORE_DEPS -q 2>&1 | grep -v "already satisfied" | tail -3

# Optional AI clients
OPTIONAL_DEPS="anthropic>=0.7.0 openai>=1.0.0"
echo "   Installing AI clients..."
pip3 install $OPTIONAL_DEPS -q 2>&1 | grep -v "already satisfied" | tail -3

# Audio processing (for mixing engineer)
AUDIO_DEPS="librosa>=0.10.0 soundfile>=0.12.0 matplotlib>=3.7.0 numpy>=1.24.0 pillow>=10.0.0"
echo "   Installing audio processing libraries..."
pip3 install $AUDIO_DEPS -q 2>&1 | grep -v "already satisfied" | tail -3

echo "   ✅ Dependencies installed!"
echo ""

# Step 4: Check if apps can import modules
echo "🔍 Step 4: Testing imports..."

# Test Logic Pro Copilot dependencies
if python3 -c "import gradio, together, dotenv" 2>/dev/null; then
    echo "   ✅ Logic Pro Copilot dependencies OK"
else
    echo "   ❌ Logic Pro Copilot dependencies missing"
fi

# Test AI Mixing Engineer dependencies
if python3 -c "import gradio, librosa, matplotlib, numpy" 2>/dev/null; then
    echo "   ✅ AI Mixing Engineer dependencies OK"
else
    echo "   ⚠️  AI Mixing Engineer dependencies incomplete (optional)"
fi

# Test Live AI Assistant dependencies
if python3 -c "import google.generativeai" 2>/dev/null; then
    echo "   ✅ Live AI Assistant dependencies OK"
else
    echo "   ⚠️  Live AI Assistant dependencies missing (install: pip3 install google-generativeai)"
fi
echo ""

# Step 5: Make scripts executable
echo "🔍 Step 5: Fixing script permissions..."
chmod +x start-*.sh 2>/dev/null
chmod +x fix-everything.sh 2>/dev/null
echo "   ✅ Scripts are now executable"
echo ""

# Step 6: Create missing directories
echo "🔍 Step 6: Creating directories..."
mkdir -p sound_packs 2>/dev/null
echo "   ✅ Directories ready"
echo ""

# Step 7: Check for port conflicts
echo "🔍 Step 7: Checking ports..."
if lsof -Pi :7860 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "   ⚠️  Port 7860 is in use (Logic Pro Copilot)"
    echo "      Run: kill -9 $(lsof -t -i:7860)"
else
    echo "   ✅ Port 7860 available"
fi

if lsof -Pi :7861 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "   ⚠️  Port 7861 is in use (AI Mixing Engineer)"
    echo "      Run: kill -9 $(lsof -t -i:7861)"
else
    echo "   ✅ Port 7861 available"
fi
echo ""

# Final Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SYSTEM STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Python: $(python3 --version)"
echo "✅ Dependencies: Installed"
echo "✅ Scripts: Executable"
echo "✅ Directories: Created"
echo ""

# Check .env status
if [ -f ".env" ] && ! grep -q "API_KEY=your_" .env 2>/dev/null; then
    echo "✅ API Keys: Configured"
else
    echo "⚠️  API Keys: Need configuration"
    echo ""
    echo "📝 NEXT STEP: Add your API keys to .env file"
    echo "   Edit .env and add:"
    echo "   - TOGETHER_API_KEY (Kimi K2)"
    echo "   - OPENAI_API_KEY (ChatGPT)"
    echo "   - ANTHROPIC_API_KEY (Claude)"
    echo "   - GEMINI_API_KEY (Google)"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 READY TO LAUNCH!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run these commands:"
echo ""
echo "   ./start-music-ai.sh              # Logic Pro Copilot"
echo "   ./start-ai-mixing-engineer.sh    # AI Mixing Engineer"
echo "   ./start-live-ai-assistant.sh     # Live Voice Assistant"
echo ""
echo "Or run directly:"
echo ""
echo "   python3 logic_copilot_lite.py"
echo "   python3 ai_mixing_engineer.py"
echo ""
echo "Need more help? Run: python3 help.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
