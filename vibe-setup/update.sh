#!/usr/bin/env bash
# 🔄 Vibe Coding Environment - Update Script
# Keep your environment fresh and up-to-date

set -e

echo "🔄 Updating Vibe Coding Environment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Update Homebrew and packages
echo ""
echo "📦 Updating Homebrew packages..."
brew update
brew upgrade

# Update global npm packages
echo ""
echo "📦 Updating npm packages..."
npm update -g

# Update Python packages
echo ""
echo "🐍 Updating Python packages..."
pip3 install --upgrade pip
pip3 install --upgrade \
    openai \
    anthropic \
    requests \
    python-dotenv \
    httpx \
    rich \
    typer

# Update IDE extensions
echo ""
echo "📦 Updating IDE extensions..."

if command -v cursor &> /dev/null; then
    echo "Updating Cursor extensions..."
    cursor --update-extensions 2>/dev/null || true
fi

if command -v code-insiders &> /dev/null; then
    echo "Updating VS Code Insiders extensions..."
    code-insiders --update-extensions 2>/dev/null || true
fi

# Reload shell configurations
echo ""
echo "🔄 Reloading configurations..."
source ~/.zshrc 2>/dev/null || true

# Update fastfetch
echo ""
echo "📊 Updating system info tools..."
brew upgrade fastfetch btop eza bat 2>/dev/null || true

echo ""
echo "✅ Update complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Updated:"
echo "  • Homebrew packages"
echo "  • npm global packages"
echo "  • Python packages"
echo "  • IDE extensions"
echo "  • Shell configurations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Restart terminal to apply all updates"

