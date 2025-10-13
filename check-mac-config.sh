#!/bin/bash

# Mac Configuration Check for AI Apps
# This script verifies your Mac is properly configured to run all apps in this project

echo "🔍 Checking Mac Configuration for AI Apps..."
echo "================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ISSUES=0

# Function to check and report
check_item() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        ISSUES=$((ISSUES + 1))
    fi
}

# Function to check and warn
warn_item() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check Python
echo "1️⃣  Python Environment"
echo "-------------------"
python3 --version > /dev/null 2>&1
check_item $? "Python 3 installed"

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Version: $PYTHON_VERSION"

# Check if Python >= 3.8
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
    check_item 0 "Python version >= 3.8 (recommended)"
else
    check_item 1 "Python version >= 3.8 (you have $PYTHON_VERSION)"
fi
echo ""

# 2. Check Virtual Environment
echo "2️⃣  Virtual Environment"
echo "-------------------"
if [ -d "venv" ]; then
    check_item 0 "Virtual environment exists"

    # Check if venv has pip
    if [ -f "venv/bin/pip" ]; then
        check_item 0 "pip available in venv"
    else
        check_item 1 "pip not found in venv"
    fi

    # Check installed packages
    source venv/bin/activate
    PKG_COUNT=$(pip list 2>/dev/null | wc -l)
    if [ $PKG_COUNT -gt 5 ]; then
        check_item 0 "Dependencies installed ($PKG_COUNT packages)"
    else
        check_item 1 "Few or no dependencies installed"
    fi
    deactivate
else
    check_item 1 "Virtual environment not found"
    echo "   Run: python3 -m venv venv"
fi
echo ""

# 3. Check System Tools
echo "3️⃣  System Tools"
echo "-------------------"
which git > /dev/null 2>&1
check_item $? "Git installed"

which brew > /dev/null 2>&1
check_item $? "Homebrew installed"

which node > /dev/null 2>&1
check_item $? "Node.js installed"

which curl > /dev/null 2>&1
check_item $? "curl installed"

which jq > /dev/null 2>&1
if [ $? -eq 0 ]; then
    check_item 0 "jq installed (JSON processor)"
else
    warn_item "jq not installed (optional but recommended)"
    echo "   Install with: brew install jq"
fi
echo ""

# 4. Check Script Permissions
echo "4️⃣  Script Permissions"
echo "-------------------"
EXECUTABLE_SCRIPTS=$(find . -maxdepth 1 -name "*.sh" -perm +111 2>/dev/null | wc -l)
TOTAL_SCRIPTS=$(find . -maxdepth 1 -name "*.sh" 2>/dev/null | wc -l)
if [ $EXECUTABLE_SCRIPTS -eq $TOTAL_SCRIPTS ] && [ $TOTAL_SCRIPTS -gt 0 ]; then
    check_item 0 "All shell scripts are executable ($EXECUTABLE_SCRIPTS/$TOTAL_SCRIPTS)"
else
    warn_item "Some scripts may not be executable ($EXECUTABLE_SCRIPTS/$TOTAL_SCRIPTS)"
    echo "   Fixed with: chmod +x *.sh"
fi
echo ""

# 5. Check Environment Variables
echo "5️⃣  Environment Variables"
echo "-------------------"
if [ -f ".env" ]; then
    check_item 0 ".env file exists"

    # Check for common API keys
    if grep -q "OPENAI_API_KEY" .env 2>/dev/null; then
        check_item 0 "OpenAI API key configured"
    else
        warn_item "OpenAI API key not found in .env"
    fi

    if grep -q "ANTHROPIC_API_KEY" .env 2>/dev/null; then
        check_item 0 "Anthropic API key configured"
    else
        warn_item "Anthropic API key not found in .env"
    fi

    if grep -q "TOGETHER_API_KEY" .env 2>/dev/null; then
        check_item 0 "Together API key configured"
    else
        warn_item "Together API key not found in .env"
    fi
else
    warn_item ".env file not found"
    echo "   Create one with: cp .env.example .env (if available)"
    echo "   Or run: ./get-my-keys.sh"
fi
echo ""

# 6. Check Network/Firewall
echo "6️⃣  Network & Firewall"
echo "-------------------"
# Check if we can reach common APIs
curl -s --max-time 5 https://api.openai.com > /dev/null 2>&1
check_item $? "Can reach OpenAI API"

curl -s --max-time 5 https://api.anthropic.com > /dev/null 2>&1
check_item $? "Can reach Anthropic API"

# Check if localhost ports are available
lsof -i :8000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    warn_item "Port 8000 is in use"
    echo "   Currently used by: $(lsof -i :8000 | tail -1 | awk '{print $1}')"
else
    check_item 0 "Port 8000 available"
fi

lsof -i :7860 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    warn_item "Port 7860 is in use (Gradio default)"
else
    check_item 0 "Port 7860 available (Gradio)"
fi
echo ""

# 7. Check macOS Permissions
echo "7️⃣  macOS Permissions"
echo "-------------------"
# Check if Terminal/iTerm has full disk access (for some operations)
if [ -r "$HOME/Library/Application Support" ]; then
    check_item 0 "Can read user Library folder"
else
    warn_item "Cannot read Library folder (may need permissions)"
fi

# Check if Xcode Command Line Tools are installed
xcode-select -p > /dev/null 2>&1
check_item $? "Xcode Command Line Tools installed"
echo ""

# 8. Check App-Specific Requirements
echo "8️⃣  App-Specific Checks"
echo "-------------------"
# Check for audio libraries (needed for mixing engineer)
source venv/bin/activate 2>/dev/null
python3 -c "import librosa" 2>/dev/null
check_item $? "librosa (audio processing) available"

python3 -c "import gradio" 2>/dev/null
check_item $? "gradio (web UI) available"

python3 -c "import openai" 2>/dev/null
if [ $? -eq 0 ]; then
    check_item 0 "openai library available"
else
    warn_item "openai library not installed"
fi

python3 -c "import anthropic" 2>/dev/null
if [ $? -eq 0 ]; then
    check_item 0 "anthropic library available"
else
    warn_item "anthropic library not installed"
fi
deactivate 2>/dev/null
echo ""

# 9. Check Memory and Storage
echo "9️⃣  System Resources"
echo "-------------------"
# Check available RAM (in GB)
TOTAL_RAM=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
if [ $TOTAL_RAM -ge 8 ]; then
    check_item 0 "Sufficient RAM (${TOTAL_RAM}GB)"
else
    warn_item "Low RAM (${TOTAL_RAM}GB) - 8GB+ recommended"
fi

# Check available disk space
AVAILABLE_SPACE=$(df -H . | tail -1 | awk '{print $4}')
echo "   Available disk space: $AVAILABLE_SPACE"
check_item 0 "Disk space checked"
echo ""

# Summary
echo "================================================"
echo "📊 Configuration Check Complete"
echo "================================================"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Your Mac is fully configured to run all apps!${NC}"
else
    echo -e "${YELLOW}⚠️  Found $ISSUES critical issues that need attention${NC}"
    echo ""
    echo "Recommendations:"
    echo "1. Install missing dependencies: source venv/bin/activate && pip install -r requirements.txt"
    echo "2. Set up API keys: run ./get-my-keys.sh or ./bw-test.sh"
    echo "3. Make scripts executable: chmod +x *.sh"
    echo "4. Check the setup guides: START-HERE.md"
fi

echo ""
echo "Quick Start Commands:"
echo "  ./start-api.sh              - Start the API server"
echo "  ./start-live-ai-assistant.sh - Start the AI assistant"
echo "  ./start-ai-mixing-engineer.sh - Start mixing engineer"
echo "  ./spawn-all-ai-services.sh   - Start all services"
echo ""

exit $ISSUES

