#!/bin/bash
# 🔍 Cursor AI Setup Verification Script
# Checks if everything is working correctly and fixes common issues

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🔍 CURSOR AI SETUP VERIFICATION 🔍                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "This script checks if your Cursor AI setup is working correctly."
echo "It will identify and help fix common issues."
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

passed=0
failed=0
warnings=0

# Function to print status
print_check() {
    echo -n "Checking $1... "
}

print_pass() {
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
}

print_fail() {
    echo -e "${RED}❌ FAIL${NC}"
    echo "   → $1"
    ((failed++))
}

print_warn() {
    echo -e "${YELLOW}⚠️  WARNING${NC}"
    echo "   → $1"
    ((warnings++))
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 SYSTEM CHECKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check 1: Cursor Installation
print_check "Cursor installation"
if [ -d "/Applications/Cursor.app" ]; then
    print_pass
else
    print_fail "Cursor not found at /Applications/Cursor.app - Install from cursor.sh"
fi

# Check 2: Git Configuration
print_check "Git configuration"
git_name=$(git config --global user.name 2>/dev/null || echo "")
git_email=$(git config --global user.email 2>/dev/null || echo "")

if [ -n "$git_name" ] && [ -n "$git_email" ]; then
    print_pass
    echo "   Git user: $git_name <$git_email>"
else
    print_fail "Git not configured. Run:
   git config --global user.name \"Your Name\"
   git config --global user.email \"your@email.com\""
fi

# Check 3: Python Installation
print_check "Python installation"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    print_pass
    echo "   $python_version"
else
    print_fail "Python 3 not found - Install from python.org"
fi

# Check 4: Environment File
print_check ".env file existence"
if [ -f ".env" ]; then
    print_pass
    # Check for API keys in .env
    if grep -q "API" .env 2>/dev/null; then
        echo "   Contains API keys ✓"
    else
        print_warn ".env exists but may be empty"
    fi
else
    print_warn ".env file not found - Create one if you need API keys"
fi

# Check 5: Cursor Settings Directory
print_check "Cursor settings directory"
if [ -d "$HOME/.cursor" ]; then
    print_pass
else
    print_warn "Cursor settings directory not found - may not have been run yet"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 API KEY CHECKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f ".env" ]; then
    # Check for various API keys
    print_check "OpenRouter API key"
    if grep -q "OPENROUTER" .env 2>/dev/null; then
        print_pass
    else
        print_warn "Not found - needed for Cline extension"
    fi

    print_check "Anthropic API key"
    if grep -q "ANTHROPIC" .env 2>/dev/null; then
        print_pass
    else
        print_warn "Not found - optional for Claude access"
    fi

    print_check "OpenAI API key"
    if grep -q "OPENAI" .env 2>/dev/null; then
        print_pass
    else
        print_warn "Not found - optional for GPT access"
    fi
else
    echo "Skipping API key checks (no .env file)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 DEPENDENCIES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_check "Python requirements.txt"
    print_pass
    
    # Check if virtual environment exists
    print_check "Virtual environment"
    if [ -d "venv" ] || [ -d ".venv" ]; then
        print_pass
    else
        print_warn "No venv found - consider creating one:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt"
    fi
else
    echo "No requirements.txt found - skipping Python checks"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RESULTS SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}Passed:${NC}   $passed checks"
echo -e "${RED}Failed:${NC}   $failed checks"
echo -e "${YELLOW}Warnings:${NC} $warnings checks"
echo ""

if [ $failed -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}🎉 SUCCESS! Your setup looks good!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Next steps:"
    echo "   1. Open Cursor"
    echo "   2. Press ⌘K to start using AI"
    echo "   3. Press ⌘L to chat with AI"
    echo ""
    if [ $warnings -gt 0 ]; then
        echo "⚠️  Note: You have $warnings warnings. Review them above."
        echo "   Most warnings are optional and won't prevent Cursor from working."
    fi
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${RED}❌ ISSUES FOUND!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Please fix the failed checks above before using Cursor."
    echo "Refer to ZERO-ISSUES-SETUP.md for detailed troubleshooting."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 HELPFUL COMMANDS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Quick Start:"
echo "  open -a Cursor                    # Open Cursor"
echo "  cat ZERO-ISSUES-SETUP.md          # Read troubleshooting guide"
echo ""
echo "Cursor Shortcuts:"
echo "  ⌘K         # Generate/edit code with AI"
echo "  ⌘L         # Chat with AI"
echo "  ⌘⇧P        # Command palette"
echo ""
echo "Fix Common Issues:"
echo "  ./verify-setup.sh                 # Run this script again"
echo "  git config --global user.name \"Your Name\""
echo "  git config --global user.email \"your@email.com\""
echo ""

exit 0
