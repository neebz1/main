#!/usr/bin/env bash
# 🔧 Automated .zshrc Merger
# Merges vibe-coding configurations into Oh My Zsh .zshrc

set -e

echo "🔧 Merging Vibe Coding configs into Oh My Zsh .zshrc..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Backup current .zshrc
BACKUP="$HOME/.zshrc.merged.backup.$(date +%Y%m%d_%H%M%S)"
cp "$HOME/.zshrc" "$BACKUP"
echo "💾 Backed up current .zshrc to $BACKUP"

# Check if vibe configs already added
if grep -q "Vibe Coding Configuration" "$HOME/.zshrc"; then
    echo "⚠️  Vibe configs already present in .zshrc"
    echo "Skipping merge to avoid duplicates"
    exit 0
fi

# Append vibe configurations
cat >> "$HOME/.zshrc" << 'VIBEEOF'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 Vibe Coding Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Vibe config directory
export VIBE_CONFIG="$HOME/.config/vibe-coding"

# ━━━ AI Tool Configuration ━━━
export OPENROUTER_API_KEY=""  # Loaded from Bitwarden
export HF_TOKEN=""
export OPENAI_API_KEY=""
export ANTHROPIC_API_KEY=""

# ━━━ Bitwarden Integration ━━━
load_api_keys() {
    if command -v bw &> /dev/null; then
        if [ -z "$BW_SESSION" ]; then
            echo "🔐 Bitwarden session not active. Run: bw unlock"
            return 1
        fi
        
        export OPENROUTER_API_KEY=$(bw get password "OpenRouter API" 2>/dev/null || echo "")
        export HF_TOKEN=$(bw get password "Hugging Face Token" 2>/dev/null || echo "")
        export OPENAI_API_KEY=$(bw get password "OpenAI API Key" 2>/dev/null || echo "")
        export ANTHROPIC_API_KEY=$(bw get password "Anthropic API Key" 2>/dev/null || echo "")
        
        echo "✅ API keys loaded from Bitwarden"
    fi
}

alias bwload='export BW_SESSION=$(bw unlock --raw) && load_api_keys'

# ━━━ Starship Prompt ━━━
eval "$(starship init zsh)"

# ━━━ Enhanced Tools ━━━
alias ls='eza --icons --group-directories-first'
alias ll='eza -l --icons --group-directories-first'
alias la='eza -la --icons --group-directories-first'
alias lt='eza --tree --level=2 --icons'
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
alias ai='f(){ echo "$@" | pbcopy && echo "📋 Prompt copied to clipboard"; }; f'
alias copilot='gh copilot'
alias chat='gh copilot chat'
alias cursor='open -a Cursor'

# ━━━ Workspace Shortcuts ━━━
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
    
    load_api_keys 2>/dev/null || echo "💡 Run 'bwload' to load API keys from Bitwarden"
}

vibe_dash() {
    clear
    btop
}

vibe_music() {
    echo "🎵 Opening lo-fi coding soundtrack..."
    open "https://www.youtube.com/watch?v=jfKfPfyJRdk"
}

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

# ━━━ Source Vibe Scripts ━━━
[ -f "$VIBE_CONFIG/ai-tools/aliases.sh" ] && source "$VIBE_CONFIG/ai-tools/aliases.sh"
[ -f "$VIBE_CONFIG/music/aliases.sh" ] && source "$VIBE_CONFIG/music/aliases.sh"
[ -f "$VIBE_CONFIG/dashboard/aliases.sh" ] && source "$VIBE_CONFIG/dashboard/aliases.sh"

# ━━━ Startup ━━━
if [ -z "$VIBE_INITIALIZED" ]; then
    export VIBE_INITIALIZED=1
    vibe_start
fi

VIBEEOF

echo ""
echo "✅ Vibe configs merged into .zshrc!"
echo ""
echo "🔄 Apply changes:"
echo "   source ~/.zshrc"
echo ""
echo "🧪 Test installation:"
echo "   vibe_start"
echo "   ai_status"
echo "   vibe-help"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

