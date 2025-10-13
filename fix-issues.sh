#!/bin/bash
# 🔧 Auto-Fix Common Cursor Issues
# This script automatically fixes the most common problems

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              🔧 AUTO-FIX CURSOR ISSUES 🔧                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "This script will automatically fix common Cursor AI issues."
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 APPLYING FIXES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fix 1: Configure Git (if not configured)
echo -n "Checking Git configuration... "
git_name=$(git config --global user.name 2>/dev/null || echo "")
if [ -z "$git_name" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Git not configured${NC}"
    echo "   Please run manually:"
    echo "   git config --global user.name \"Your Name\""
    echo "   git config --global user.email \"your@email.com\""
else
    echo -e "${GREEN}✅ Already configured${NC}"
fi

# Fix 2: Create .env file if missing
echo -n "Checking .env file... "
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}Creating .env file...${NC}"
    touch .env
    echo "# Add your API keys here" > .env
    echo "# OPENROUTER_API_KEY=your-key-here" >> .env
    echo "# ANTHROPIC_API_KEY=your-key-here" >> .env
    echo "# OPENAI_API_KEY=your-key-here" >> .env
    echo -e "${GREEN}✅ Created .env file${NC}"
else
    echo -e "${GREEN}✅ Exists${NC}"
fi

# Fix 3: Create virtual environment if missing
echo -n "Checking Python virtual environment... "
if [ ! -d "venv" ] && [ -f "requirements.txt" ]; then
    echo ""
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
    echo "   Run: source venv/bin/activate"
else
    echo -e "${GREEN}✅ OK${NC}"
fi

# Fix 4: Make scripts executable
echo -n "Making scripts executable... "
chmod +x *.sh 2>/dev/null
echo -e "${GREEN}✅ Done${NC}"

# Fix 5: Check for .gitignore
echo -n "Checking .gitignore... "
if [ ! -f ".gitignore" ]; then
    echo ""
    echo -e "${YELLOW}Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Environment and API keys
.env
*.env

# Python
__pycache__/
*.py[cod]
venv/
env/

# OS
.DS_Store

# IDE
.vscode/
.idea/
EOF
    echo -e "${GREEN}✅ Created .gitignore${NC}"
else
    echo -e "${GREEN}✅ Exists${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ AUTO-FIX COMPLETE!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Open Cursor"
echo "2. Restart Cursor if it was open (⌘Q → reopen)"
echo "3. Press ⌘K to test AI"
echo ""
echo "If still having issues, run: ./verify-setup.sh"
echo ""
