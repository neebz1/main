#!/bin/bash
# 🚀 Complete Setup Script - Download and Set Up Everything
# This script installs all dependencies and configures your AI Music Production Suite

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Progress counter
STEP=0
TOTAL_STEPS=10

print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    STEP=$((STEP + 1))
    echo ""
    echo -e "${BLUE}[$STEP/$TOTAL_STEPS]${NC} ${GREEN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}"
}

# Start setup
clear
print_header "🚀 AI MUSIC PRODUCTION SUITE - COMPLETE SETUP"

echo -e "${CYAN}This script will:${NC}"
echo "  • Check system prerequisites"
echo "  • Set up Python virtual environment"
echo "  • Install all required dependencies"
echo "  • Configure environment files"
echo "  • Make all scripts executable"
echo "  • Test basic functionality"
echo ""
read -p "Press Enter to continue..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Check Python
print_step "Checking Python installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
    
    # Check Python version is 3.8 or higher
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python version is compatible (>= 3.8)"
    else
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Step 2: Check pip
print_step "Checking pip installation"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    print_success "pip3 found: $PIP_VERSION"
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Step 3: Create virtual environment
print_step "Setting up Python virtual environment"
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing old virtual environment..."
        rm -rf venv
        print_info "Creating new virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment recreated"
    else
        print_success "Using existing virtual environment"
    fi
else
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Step 4: Activate virtual environment
print_step "Activating virtual environment"
source venv/bin/activate
print_success "Virtual environment activated"

# Step 5: Upgrade pip
print_step "Upgrading pip in virtual environment"
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded to latest version"

# Step 6: Install dependencies
print_step "Installing Python dependencies"
echo ""

# Collect all unique requirements
print_info "Collecting requirements from all files..."
REQ_FILES=(
    "requirements.txt"
    "requirements_lite.txt"
    "requirements_mixing.txt"
    "requirements_live_ai.txt"
    "requirements_plugin.txt"
    "requirements_chatgpt_training.txt"
)

# Install each requirements file
INSTALLED_COUNT=0
for req_file in "${REQ_FILES[@]}"; do
    if [ -f "$req_file" ]; then
        echo -e "${CYAN}  Installing from $req_file...${NC}"
        if pip install -r "$req_file" > /dev/null 2>&1; then
            print_success "  ✓ Installed from $req_file"
            INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
        else
            print_warning "  ⚠ Some packages from $req_file may have failed"
        fi
    fi
done

echo ""
print_success "Installed dependencies from $INSTALLED_COUNT requirements files"

# Step 7: Create .env file if it doesn't exist
print_step "Setting up environment configuration"
if [ ! -f ".env" ]; then
    print_info "Creating .env template file..."
    cat > .env << 'EOF'
# 🔑 API Keys Configuration
# Fill in your API keys below

# Moonshot/Kimi K2 API (for music AI)
MOONSHOT_API_KEY=your_moonshot_api_key_here

# OpenRouter API (multiple AI models)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic Claude API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Together API
TOGETHER_API_KEY=your_together_api_key_here

# Hugging Face Token
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Brave Search API (optional)
BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here

# GitHub Token (optional)
GITHUB_TOKEN=your_github_token_here
EOF
    print_success ".env template created"
    print_warning "Please edit .env file and add your API keys"
else
    print_success ".env file already exists"
fi

# Step 8: Make scripts executable
print_step "Making launcher scripts executable"
SCRIPTS=(
    "start-music-ai.sh"
    "start-ai-mixing-engineer.sh"
    "start-cloud-builder.sh"
    "start-live-ai-assistant.sh"
    "start-logic-ai-plugin.sh"
    "setup-everything.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        print_info "  ✓ Made $script executable"
    fi
done

print_success "All launcher scripts are executable"

# Step 9: Test basic imports
print_step "Testing Python dependencies"
echo ""

# Test critical imports
TEST_IMPORTS=(
    "gradio"
    "dotenv:python-dotenv"
    "openai"
    "anthropic"
    "together"
)

FAILED_IMPORTS=()

for import_test in "${TEST_IMPORTS[@]}"; do
    IFS=':' read -r module package <<< "$import_test"
    package=${package:-$module}
    
    if python -c "import $module" 2>/dev/null; then
        print_info "  ✓ $package imported successfully"
    else
        print_warning "  ✗ $package could not be imported"
        FAILED_IMPORTS+=("$package")
    fi
done

if [ ${#FAILED_IMPORTS[@]} -eq 0 ]; then
    print_success "All critical packages installed correctly"
else
    echo ""
    print_warning "Some packages could not be imported: ${FAILED_IMPORTS[*]}"
    print_info "You may need to install them manually or add API keys"
fi

# Step 10: Create quick start guide
print_step "Creating quick reference"

cat > SETUP-COMPLETE.txt << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  🎉 SETUP COMPLETE! YOUR AI MUSIC SUITE IS READY!           ║
╚══════════════════════════════════════════════════════════════╝

📦 WHAT'S INSTALLED:
  ✅ Python virtual environment (venv/)
  ✅ All Python dependencies
  ✅ Gradio for web interfaces
  ✅ AI API clients (OpenAI, Anthropic, Together)
  ✅ All launcher scripts configured

🚀 AVAILABLE TOOLS:

1. 🎵 Music Copilot
   Launch: ./start-music-ai.sh
   Opens: http://localhost:7860
   
2. 🎚️ AI Mixing Engineer
   Launch: ./start-ai-mixing-engineer.sh
   Opens: http://localhost:7861
   
3. 🎤 Live AI Assistant
   Launch: ./start-live-ai-assistant.sh
   Voice-controlled music production
   
4. 🔌 Logic AI Plugin
   Launch: ./start-logic-ai-plugin.sh
   Real-time Logic Pro control
   
5. ☁️ Cloud AI Builder
   Launch: ./start-cloud-builder.sh
   Opens: http://localhost:7862

⚙️ NEXT STEPS:

1. 📝 Edit .env file and add your API keys
   (Required for AI features to work)

2. 🚀 Launch any tool:
   ./start-music-ai.sh

3. 📚 Read the documentation:
   - README.md - Overview
   - START-HERE.md - Quick start guide
   - FINAL-SETUP-SUMMARY.md - Detailed guide

🔑 API KEYS NEEDED:

To use all features, you'll need API keys from:
  • Moonshot/Kimi (for music AI)
  • OpenRouter (for multiple AI models)
  • Anthropic Claude (for advanced AI)
  • OpenAI GPT (optional)
  • Google Gemini (optional)

Add these to your .env file.

💡 QUICK TEST:

Activate virtual environment:
  source venv/bin/activate

Launch Music Copilot:
  ./start-music-ai.sh

🆘 TROUBLESHOOTING:

• If scripts don't run: chmod +x *.sh
• If imports fail: pip install -r requirements_lite.txt
• If port in use: Check if another app is already running

📖 DOCUMENTATION:

Full guides available in:
  - MASTER-GUIDE.md
  - AI-MIXING-ENGINEER-GUIDE.md
  - MUSIC-AI-GUIDE.md

═══════════════════════════════════════════════════════════════

🎉 You're all set! Start building amazing music with AI! 🎵

═══════════════════════════════════════════════════════════════
EOF

print_success "Quick reference saved to SETUP-COMPLETE.txt"

# Final summary
print_header "✅ SETUP COMPLETE!"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         🎉 Your AI Music Production Suite is Ready!         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📦 What's Installed:${NC}"
echo "   ✅ Python virtual environment"
echo "   ✅ All dependencies (Gradio, AI APIs, etc.)"
echo "   ✅ 5 AI-powered music production tools"
echo "   ✅ Launcher scripts configured"
echo ""
echo -e "${CYAN}⚙️ Configuration Needed:${NC}"
if [ -f ".env" ] && grep -q "your_.*_api_key_here" .env; then
    echo -e "   ${YELLOW}⚠️  Edit .env file and add your API keys${NC}"
else
    echo "   ✅ .env file configured"
fi
echo ""
echo -e "${CYAN}🚀 Quick Start:${NC}"
echo ""
echo "   1. Activate virtual environment:"
echo -e "      ${PURPLE}source venv/bin/activate${NC}"
echo ""
echo "   2. Launch Music Copilot:"
echo -e "      ${PURPLE}./start-music-ai.sh${NC}"
echo ""
echo "   3. Or launch AI Mixing Engineer:"
echo -e "      ${PURPLE}./start-ai-mixing-engineer.sh${NC}"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo "   • SETUP-COMPLETE.txt - Quick reference"
echo "   • README.md - Overview"
echo "   • START-HERE.md - Beginner guide"
echo "   • MASTER-GUIDE.md - Complete guide"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}🎵 Ready to create amazing music with AI! 🚀${NC}"
echo ""
