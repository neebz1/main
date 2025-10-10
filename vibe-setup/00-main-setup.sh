#!/usr/bin/env bash
# 🎨 Ultimate Vibe-Coding Environment Setup for macOS
# Phase 0: Core Tools Installation

set -e

echo "🚀 Starting Ultimate Vibe-Coding Setup..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    exit 1
fi

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew already installed"
    brew update
fi

# Install core development tools
echo ""
echo "🔧 Installing core development tools..."
brew install --quiet git node python3 pnpm docker ngrok || true

# Install additional essential tools
echo ""
echo "🎯 Installing productivity & terminal tools..."
brew install --quiet \
    gh \
    jq \
    ripgrep \
    fzf \
    bat \
    eza \
    btop \
    fastfetch \
    neofetch \
    starship \
    zoxide \
    bitwarden-cli \
    hammerspoon \
    || true

# Install casks for GUI apps
echo ""
echo "💻 Checking for IDE installations..."
brew install --cask --quiet \
    docker \
    ngrok \
    || true

# Setup Docker if not running
if ! docker info &> /dev/null; then
    echo "🐋 Starting Docker..."
    open -a Docker
    echo "⏳ Waiting for Docker to start..."
    sleep 10
fi

# Install global npm packages
echo ""
echo "📦 Installing global npm packages..."
npm install -g npm@latest
npm install -g \
    typescript \
    ts-node \
    nodemon \
    prettier \
    eslint \
    vercel \
    netlify-cli \
    firebase-tools

# Setup Python environment
echo ""
echo "🐍 Setting up Python environment..."
pip3 install --upgrade pip
pip3 install \
    openai \
    anthropic \
    requests \
    python-dotenv \
    httpx \
    rich \
    typer

# Install JetBrains Mono font
echo ""
echo "🔤 Installing JetBrains Mono Nerd Font..."
brew tap homebrew/cask-fonts
brew install --cask --quiet font-jetbrains-mono-nerd-font || true

# Setup fzf key bindings
echo ""
echo "⚡ Setting up fzf..."
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish

echo ""
echo "✅ Core tools installation complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

