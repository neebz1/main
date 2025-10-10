#!/bin/bash
# 📚 Docs-Agent Installation Script

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           📚 Installing Docs-Agent Module 📚                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make CLI executable
chmod +x docs_cli.py

# Initialize index
echo ""
echo "🔧 Initializing documentation index..."
python3 docs_cli.py init

# Create alias in vibe environment
ALIAS_LINE='alias docs="cd ~/CursorDocsIndex && source venv/bin/activate && python docs_cli.py"'

if ! grep -q "alias docs=" ~/.zshrc; then
    echo ""
    echo "🔗 Adding 'docs' alias to .zshrc..."
    echo "" >> ~/.zshrc
    echo "# Docs-Agent CLI" >> ~/.zshrc
    echo "$ALIAS_LINE" >> ~/.zshrc
    echo "✅ Alias added! Run 'source ~/.zshrc' to use it"
else
    echo "✅ Alias already exists in .zshrc"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Installation Complete! ✅                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "1. Activate environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Or use the alias (after reloading shell):"
echo "   source ~/.zshrc"
echo "   docs search 'your query'"
echo ""
echo "3. Try the demo:"
echo "   python docs_cli.py demo"
echo ""
echo "📚 Commands:"
echo "   python docs_cli.py ingest <url>"
echo "   python docs_cli.py search <query>"
echo "   python docs_cli.py lookup <query>"
echo "   python docs_cli.py stats"
echo ""

