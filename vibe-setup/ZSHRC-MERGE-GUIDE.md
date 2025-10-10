# 🔧 .zshrc Merge Guide

## ⚠️ Issue: Oh My Zsh Overwrote Vibe Configuration

During Phase 5 (Theme Setup), Oh My Zsh was installed, which created a new `.zshrc` file and backed up the vibe-coding `.zshrc` to `.zshrc.pre-oh-my-zsh`.

**We need to merge the vibe-coding configurations into the Oh My Zsh `.zshrc`.**

---

## 📋 Current State

### Files:
- `~/.zshrc` - Current (Oh My Zsh template)
- `~/.zshrc.pre-oh-my-zsh` - Vibe configs (from Phase 3)
- `~/.zshrc.backup.20251010_030938` - Original backup

---

## 🚀 Option 1: Automated Merge (Recommended)

Run this script to automatically merge vibe configs into Oh My Zsh `.zshrc`:

```bash
cd ~/main/vibe-setup
./merge-zshrc.sh
```

This will:
1. Backup current Oh My Zsh `.zshrc`
2. Keep Oh My Zsh framework
3. Add all vibe-coding configurations
4. Source all vibe scripts
5. Apply Starship prompt
6. Add all aliases and functions

---

## 🛠️ Option 2: Manual Merge

### Step 1: Backup Current .zshrc
```bash
cp ~/.zshrc ~/.zshrc.oh-my-zsh.backup
```

### Step 2: Edit ~/.zshrc

Add the following sections to your `~/.zshrc` (after Oh My Zsh setup):

#### A. At the Top (After Shebang):
```bash
# 🎨 Vibe Coding Environment Configuration
```

#### B. After Oh My Zsh Initialization:

Find this line in your `.zshrc`:
```bash
source $ZSH/oh-my-zsh.sh
```

**Add after it:**

```bash
# ━━━ Vibe Coding Configuration ━━━

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
```

### Step 3: Apply Changes
```bash
source ~/.zshrc
```

### Step 4: Test
```bash
vibe_start
ai_status
vibe-help
```

---

## 🤖 Option 3: Use the Automated Script

I'll create a merge script for you:


