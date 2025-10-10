#!/usr/bin/env bash
# 🎨 Enhanced .zshrc Configuration
# Sets up shell environment with AI integrations and vibe elements

set -e

ZSHRC="$HOME/.zshrc"
BACKUP="$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)"

echo "🎨 Configuring enhanced .zshrc..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Backup existing .zshrc
if [ -f "$ZSHRC" ]; then
    cp "$ZSHRC" "$BACKUP"
    echo "💾 Backed up existing .zshrc to $BACKUP"
fi

# Create new .zshrc
cat > "$ZSHRC" << 'EOF'
# 🎨 Ultimate Vibe-Coding Environment
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Homebrew setup
if [[ $(uname -m) == 'arm64' ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    eval "$(/usr/local/bin/brew shellenv)"
fi

# ━━━ PATH Configuration ━━━
export PATH="/opt/homebrew/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Node & pnpm
export PNPM_HOME="$HOME/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"

# Python
export PATH="/opt/homebrew/opt/python@3/libexec/bin:$PATH"

# ━━━ AI Tool Configuration ━━━
export VIBE_CONFIG="$HOME/.config/vibe-coding"

# OpenRouter
export OPENROUTER_API_KEY=""  # Loaded from Bitwarden

# Hugging Face
export HF_TOKEN=""  # Loaded from Bitwarden

# OpenAI (for Copilot)
export OPENAI_API_KEY=""  # Loaded from Bitwarden

# Anthropic
export ANTHROPIC_API_KEY=""  # Loaded from Bitwarden

# ━━━ Bitwarden Integration ━━━
# Auto-load API keys from Bitwarden
load_api_keys() {
    if command -v bw &> /dev/null; then
        if [ -z "$BW_SESSION" ]; then
            echo "🔐 Bitwarden session not active. Run: bw unlock"
            return 1
        fi
        
        # Load keys from Bitwarden (customize these item names)
        export OPENROUTER_API_KEY=$(bw get password "OpenRouter API" 2>/dev/null || echo "")
        export HF_TOKEN=$(bw get password "Hugging Face Token" 2>/dev/null || echo "")
        export OPENAI_API_KEY=$(bw get password "OpenAI API Key" 2>/dev/null || echo "")
        export ANTHROPIC_API_KEY=$(bw get password "Anthropic API Key" 2>/dev/null || echo "")
        
        echo "✅ API keys loaded from Bitwarden"
    fi
}

# Alias to unlock and load
alias bwload='export BW_SESSION=$(bw unlock --raw) && load_api_keys'

# ━━━ Starship Prompt ━━━
eval "$(starship init zsh)"

# ━━━ Enhanced Tools ━━━
# eza (modern ls)
alias ls='eza --icons --group-directories-first'
alias ll='eza -l --icons --group-directories-first'
alias la='eza -la --icons --group-directories-first'
alias lt='eza --tree --level=2 --icons'

# bat (modern cat)
alias cat='bat --style=plain'
alias catt='bat'

# zoxide (smart cd)
eval "$(zoxide init zsh)"
alias cd='z'

# fzf (fuzzy finder)
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
export FZF_DEFAULT_OPTS="
  --color=fg:#c0caf5,bg:#1a1b26,hl:#bb9af7
  --color=fg+:#c0caf5,bg+:#292e42,hl+:#7dcfff
  --color=info:#7aa2f7,prompt:#7dcfff,pointer:#7dcfff
  --color=marker:#9ece6a,spinner:#9ece6a,header:#9ece6a
  --layout=reverse
  --border
  --height=40%
"

# ━━━ AI Shortcuts ━━━
# Quick AI prompting
alias ai='f(){ echo "$@" | pbcopy && echo "📋 Prompt copied to clipboard"; }; f'

# Open AI consoles
alias copilot='gh copilot'
alias chat='gh copilot chat'

# Cursor from terminal
alias cursor='open -a Cursor'

# ━━━ Workspace Shortcuts ━━━
# Quick workspace navigation
alias ws='cd ~/main && cursor .'
alias logic='open -a "Logic Pro"'

# ━━━ Git Shortcuts ━━━
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias gco='git checkout'
alias gcb='git checkout -b'
alias glog='git log --oneline --graph --decorate'

# ━━━ Docker Shortcuts ━━━
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dimg='docker images'

# ━━━ Development Shortcuts ━━━
alias serve='python3 -m http.server'
alias ports='lsof -i -P | grep LISTEN'
alias myip='curl -s https://api.ipify.org && echo'

# ━━━ Vibe Functions ━━━

# Start vibe coding session
vibe_start() {
    clear
    fastfetch
    echo ""
    echo "🎨 Vibe Coding Mode Activated"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🤖 AI Tools: Ready"
    echo "🎵 Soundtrack: Use 'vibe_music' to start lo-fi"
    echo "⚡ Shortcuts: cmd+alt+g (Copilot), cmd+alt+a (Terminal)"
    echo ""
    
    # Load API keys if Bitwarden is unlocked
    load_api_keys 2>/dev/null || echo "💡 Run 'bwload' to load API keys from Bitwarden"
}

# Open vibe dashboard
vibe_dash() {
    clear
    btop
}

# Music integration (opens lo-fi stream in browser)
vibe_music() {
    echo "🎵 Opening lo-fi coding soundtrack..."
    open "https://www.youtube.com/watch?v=jfKfPfyJRdk" # Lofi Girl
}

# Show AI status
ai_status() {
    echo "🤖 AI Tools Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    [ -n "$OPENROUTER_API_KEY" ] && echo "✅ OpenRouter" || echo "❌ OpenRouter"
    [ -n "$HF_TOKEN" ] && echo "✅ Hugging Face" || echo "❌ Hugging Face"
    [ -n "$OPENAI_API_KEY" ] && echo "✅ OpenAI" || echo "❌ OpenAI"
    [ -n "$ANTHROPIC_API_KEY" ] && echo "✅ Anthropic" || echo "❌ Anthropic"
    command -v gh &> /dev/null && echo "✅ GitHub CLI" || echo "❌ GitHub CLI"
    [ -d "/Applications/Cursor.app" ] && echo "✅ Cursor" || echo "❌ Cursor"
}

# ━━━ Startup ━━━
# Show welcome message on new terminal
if [ -z "$VIBE_INITIALIZED" ]; then
    export VIBE_INITIALIZED=1
    vibe_start
fi

# ━━━ Additional Completions ━━━
autoload -Uz compinit
compinit

# Case-insensitive completion
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Better completion menu
zstyle ':completion:*' menu select

EOF

echo ""
echo "✅ .zshrc configuration complete!"
echo "🔄 Run 'source ~/.zshrc' or restart terminal to apply"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

