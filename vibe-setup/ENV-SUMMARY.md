# 🎨 Vibe Coding Environment - Environment Variables Summary
**User:** Noah  
**Generated:** October 10, 2025  
**System:** macOS 25.0.0 (ARM64)

---

## 🔐 API Keys (Stored in Bitwarden)

All sensitive API keys are stored securely in Bitwarden and loaded via the `bwload` command.

### Required API Keys:

| Service | Bitwarden Item Name | Purpose | Get Key From |
|---------|---------------------|---------|--------------|
| **OpenRouter** | `OpenRouter API` | Access to Claude, GPT-4, Gemini, Llama | https://openrouter.ai/keys |
| **Hugging Face** | `Hugging Face Token` | ML model search & deployment | https://huggingface.co/settings/tokens |
| **OpenAI** | `OpenAI API Key` | Direct GPT access (optional) | https://platform.openai.com/api-keys |
| **Anthropic** | `Anthropic API Key` | Direct Claude access (optional) | https://console.anthropic.com/ |
| **Kimi K2** | `Kimi API Key` | Advanced AI reasoning (optional) | Kimi documentation |

###Load Keys:

```bash
# 1. Login to Bitwarden
bw login

# 2. Unlock vault and set session
export BW_SESSION=$(bw unlock --raw)

# 3. Load all API keys into environment
bwload

# 4. Verify keys are loaded
ai_status
```

### Environment Variables Set by `bwload`:

```bash
export OPENROUTER_API_KEY="<loaded-from-bitwarden>"
export HF_TOKEN="<loaded-from-bitwarden>"
export OPENAI_API_KEY="<loaded-from-bitwarden>"
export ANTHROPIC_API_KEY="<loaded-from-bitwarden>"
export KIMI_API_KEY="<loaded-from-bitwarden>"
```

---

## 📁 Path Configuration

### Homebrew (Apple Silicon):
```bash
export HOMEBREW_PREFIX="/opt/homebrew"
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Core Paths:
```bash
# Binaries
/opt/homebrew/bin
/usr/local/bin
$HOME/.local/bin

# Docker
/Applications/Docker.app/Contents/Resources/bin

# Node & pnpm
$HOME/Library/pnpm

# Python
/opt/homebrew/opt/python@3/libexec/bin

# Vibe scripts
$HOME/.config/vibe-coding/ai-tools
$HOME/.config/vibe-coding/music
$HOME/.config/vibe-coding/dashboard
```

---

## 🎯 Vibe Coding Paths

### Base Configuration:
```bash
VIBE_CONFIG="$HOME/.config/vibe-coding"
```

### Directory Structure:
```
$HOME/.config/vibe-coding/
├── settings.json                      # → Symlinked to IDE User dirs
├── keybindings.json                   # → Symlinked to IDE User dirs
├── extensions.txt
├── add-api-key.sh
│
├── themes/
│   ├── TokyoNight.terminal
│   └── tokyo-night.itermcolors
│
├── ai-tools/
│   ├── openrouter-config.json
│   ├── openrouter-cli.py
│   ├── kimi-config.sh
│   ├── huggingface-cli.py
│   ├── vibe-ai.sh
│   ├── aliases.sh
│   └── cursor-rules.md                # → Symlinked to Cursor User/.cursorrules
│
├── music/
│   ├── vibe-player.sh
│   ├── spotify-control.sh
│   ├── workspace-trigger.sh
│   ├── music-control.applescript
│   └── aliases.sh
│
├── dashboard/
│   ├── vibe-dashboard.sh
│   ├── ai-monitor.sh
│   ├── vibe-help.sh
│   └── aliases.sh
│
└── logs/
    └── ai-usage.log
```

---

## 💻 IDE Paths

### Cursor (Installed):
```bash
# Application
/Applications/Cursor.app

# User Config Directory
$HOME/Library/Application Support/Cursor/User/

# Symlinked Files:
$HOME/Library/Application Support/Cursor/User/keybindings.json
  → $HOME/.config/vibe-coding/keybindings.json

$HOME/Library/Application Support/Cursor/User/settings.json
  → $HOME/.config/vibe-coding/settings.json

$HOME/Library/Application Support/Cursor/User/.cursorrules
  → $HOME/.config/vibe-coding/ai-tools/cursor-rules.md

# Extensions Directory
$HOME/Library/Application Support/Cursor/extensions/
```

### VS Code Insiders (Not Detected):
```bash
# Application
/Applications/Visual Studio Code - Insiders.app

# User Config Directory (if installed)
$HOME/Library/Application Support/Code - Insiders/User/
```

### Windsurf (Not Detected):
```bash
# Application
/Applications/Windsurf.app

# User Config Directory (if installed)
$HOME/Library/Application Support/Windsurf/User/
```

---

## 🤖 AI Tool Configuration

### OpenRouter:
```bash
# API Configuration
API_BASE="https://openrouter.ai/api/v1"
DEFAULT_MODEL="anthropic/claude-3.5-sonnet"

# Config File
$HOME/.config/vibe-coding/ai-tools/openrouter-config.json

# CLI Script
$HOME/.config/vibe-coding/ai-tools/openrouter-cli.py
```

### Kimi K2:
```bash
# API Configuration
API_BASE="https://api.moonshot.cn/v1"
MODEL="moonshot-v1-8k"

# Config File
$HOME/.config/vibe-coding/ai-tools/kimi-config.sh
```

### Hugging Face:
```bash
# CLI Script
$HOME/.config/vibe-coding/ai-tools/huggingface-cli.py

# Token loaded from Bitwarden (HF_TOKEN)
```

### GitHub Copilot:
```bash
# Requires GitHub CLI
/opt/homebrew/bin/gh

# Commands available after: gh auth login
gh copilot explain <command>
gh copilot suggest
```

### Unified Interface:
```bash
# Main script
$HOME/.config/vibe-coding/ai-tools/vibe-ai.sh

# Usage:
# vibe-ai or <prompt>       → OpenRouter
# vibe-ai kimi <prompt>     → Kimi K2
# vibe-ai gh <prompt>       → GitHub Copilot
```

---

## 🎵 Music Integration

### Scripts:
```bash
# Main player
$HOME/.config/vibe-coding/music/vibe-player.sh

# Spotify controls
$HOME/.config/vibe-coding/music/spotify-control.sh

# Music.app controls
$HOME/.config/vibe-coding/music/music-control.applescript

# Workspace trigger
$HOME/.config/vibe-coding/music/workspace-trigger.sh
```

### Playlists:
```bash
# Default: Lofi Girl
https://www.youtube.com/watch?v=jfKfPfyJRdk

# Spotify Lofi
https://open.spotify.com/playlist/0vvXsWCC9xrXsKd4FyS8kM

# Chillhop
https://www.youtube.com/watch?v=5qap5aO4i9A

# Synthwave
https://www.youtube.com/watch?v=4xDzrJKXOOY
```

---

## 📊 Dashboard & Monitoring

### Scripts:
```bash
# Main dashboard
$HOME/.config/vibe-coding/dashboard/vibe-dashboard.sh

# AI usage monitor
$HOME/.config/vibe-coding/dashboard/ai-monitor.sh

# Help system
$HOME/.config/vibe-coding/dashboard/vibe-help.sh
```

### Logs:
```bash
# AI usage log
$HOME/.config/vibe-coding/logs/ai-usage.log
```

### System Tools:
```bash
# fastfetch config
$HOME/.config/fastfetch/config.jsonc

# Starship prompt
$HOME/.config/starship.toml

# Hammerspoon
$HOME/.hammerspoon/init.lua
```

---

## ⌨️ Global Shortcuts (Hammerspoon)

### Configuration:
```bash
$HOME/.hammerspoon/init.lua
```

### Shortcuts Defined:
```
⌘ ⌥ G  → Open Cursor + GitHub Copilot Chat
⌘ ⌥ A  → Open Terminal (AI Console)
⌘ ⌥ C  → Launch Cursor
⌘ ⌥ V  → Launch VS Code Insiders
⌘ ⌥ W  → Launch Windsurf
⌘ ⌥ L  → Launch Logic Pro
⌘ ⌥ B  → Launch Browser
⌘ ⌥ D  → Open btop (Dashboard)
⌘ ⌥ M  → Start Lo-fi Music
⌘ ⌥ S  → Show AI Status

⌘ ⌥ ←  → Snap window left
⌘ ⌥ →  → Snap window right
⌘ ⌥ ↑  → Maximize window
⌘ ⌥ ↓  → Center window
```

---

## 🎨 Theme Configuration

### Colors (Tokyo Night):
```bash
Background:  #1a1b26
Foreground:  #c0caf5
Blue:        #7aa2f7
Purple:      #bb9af7
Cyan:        #7dcfff
Green:       #9ece6a
Orange:      #ff9e64
Red:         #f7768e
```

### Theme Files:
```bash
# Terminal.app
$HOME/.config/vibe-coding/themes/TokyoNight.terminal

# iTerm2
$HOME/.config/vibe-coding/themes/tokyo-night.itermcolors

# Starship prompt
$HOME/.config/starship.toml

# Cursor theme extension
enkia.tokyo-night (v1.1.2)
```

### Font:
```bash
# Primary Font
JetBrains Mono Nerd Font

# Installation (Manual Required)
Download from: https://www.jetbrains.com/lp/mono/
Or: https://www.nerdfonts.com/font-downloads

# IDE Settings
Font Family: 'JetBrains Mono'
Font Size: 14px (editor), 13px (terminal)
Ligatures: Enabled
Line Height: 1.6
```

---

## 🔧 Shell Configuration

### Main Shell Config:
```bash
$HOME/.zshrc
```

### Backups:
```bash
$HOME/.zshrc.backup.20251010_030938    # Original backup
$HOME/.zshrc.pre-oh-my-zsh             # Oh My Zsh backup
```

### Frameworks:
```bash
# Oh My Zsh (Installed Phase 5)
$HOME/.oh-my-zsh/

# Powerlevel10k Theme
$HOME/.oh-my-zsh/custom/themes/powerlevel10k/

# Starship Prompt (Configured Phase 4)
$HOME/.config/starship.toml
```

### Source Order (Recommended):
```bash
# 1. Oh My Zsh
source $HOME/.oh-my-zsh/oh-my-zsh.sh

# 2. Vibe aliases
source $HOME/.config/vibe-coding/ai-tools/aliases.sh
source $HOME/.config/vibe-coding/music/aliases.sh
source $HOME/.config/vibe-coding/dashboard/aliases.sh

# 3. Starship prompt
eval "$(starship init zsh)"

# 4. Tool initializations
eval "$(zoxide init zsh)"
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

---

## 🛠️ Tool Binaries

### Installed via Homebrew:
```bash
/opt/homebrew/bin/git
/opt/homebrew/bin/node
/opt/homebrew/bin/npm
/opt/homebrew/bin/pnpm
/opt/homebrew/bin/python3
/opt/homebrew/bin/pip3
/opt/homebrew/bin/docker
/opt/homebrew/bin/ngrok
/opt/homebrew/bin/gh
/opt/homebrew/bin/bw
/opt/homebrew/bin/jq
/opt/homebrew/bin/rg
/opt/homebrew/bin/fzf
/opt/homebrew/bin/bat
/opt/homebrew/bin/eza
/opt/homebrew/bin/btop
/opt/homebrew/bin/fastfetch
/opt/homebrew/bin/starship
/opt/homebrew/bin/zoxide
/opt/homebrew/bin/hs  (Hammerspoon CLI)
```

### Python Packages:
```bash
$HOME/Library/Python/3.9/lib/python/site-packages/
├── openai/
├── anthropic/
├── requests/
├── dotenv/
├── httpx/
├── rich/
└── typer/
```

### Global npm Packages:
```bash
/opt/homebrew/lib/node_modules/
├── typescript/
├── ts-node/
├── nodemon/
├── prettier/
├── eslint/
├── vercel/
├── netlify-cli/
└── firebase-tools/
```

---

## 🌐 Network & Services

### Docker:
```bash
# Application
/Applications/Docker.app

# CLI
/Applications/Docker.app/Contents/Resources/bin/docker

# Status
docker info  # Check if running
```

### ngrok:
```bash
# Binary
/opt/homebrew/bin/ngrok

# Usage
ngrok http 3000  # Tunnel local port
```

### GitHub CLI:
```bash
# Binary
/opt/homebrew/bin/gh

# Authentication
gh auth login  # Required for Copilot

# Config
$HOME/.config/gh/
```

---

## 📝 Workspace Configuration

### Main Workspace:
```bash
$HOME/main
```

### Workspace Directories (for auto-music):
```bash
$HOME/main
$HOME/projects
$HOME/code
```

### Quick Navigation:
```bash
# Alias: ws
alias ws='cd ~/main && cursor .'
```

---

## 🎯 Environment Variable Reference

### Critical Environment Variables:

```bash
# Paths
HOMEBREW_PREFIX="/opt/homebrew"
VIBE_CONFIG="$HOME/.config/vibe-coding"
WORKSPACE_DIR="$HOME/main"

# AI APIs (loaded from Bitwarden)
OPENROUTER_API_KEY=""
HF_TOKEN=""
OPENAI_API_KEY=""
ANTHROPIC_API_KEY=""
KIMI_API_KEY=""

# Bitwarden
BW_SESSION=""  # Set after unlock

# Tools
EDITOR="cursor"
VISUAL="cursor"
BROWSER="open"

# Theme
FZF_DEFAULT_OPTS="..."  # Tokyo Night colors
BAT_THEME="TwoDark"
STARSHIP_CONFIG="$HOME/.config/starship.toml"
```

---

## 🔗 Symlinks Summary

### IDE Configurations:
```bash
~/Library/Application Support/Cursor/User/keybindings.json
  → ~/.config/vibe-coding/keybindings.json

~/Library/Application Support/Cursor/User/settings.json
  → ~/.config/vibe-coding/settings.json

~/Library/Application Support/Cursor/User/.cursorrules
  → ~/.config/vibe-coding/ai-tools/cursor-rules.md
```

### Verification:
```bash
# Check symlinks
ls -la ~/Library/Application\ Support/Cursor/User/

# Expected output:
# keybindings.json -> /Users/nr/.config/vibe-coding/keybindings.json
# settings.json -> /Users/nr/.config/vibe-coding/settings.json
# .cursorrules -> /Users/nr/.config/vibe-coding/ai-tools/cursor-rules.md
```

---

## 🚀 Connection Paths Resolved

### AI Tool Connections:
```
User → Terminal
  → bwload
    → Bitwarden CLI (/opt/homebrew/bin/bw)
      → Loads API keys from Bitwarden vault
        → Sets environment variables
          → Available to all AI tools

User → ai-ask "prompt"
  → ~/.config/vibe-coding/ai-tools/openrouter-cli.py
    → Uses $OPENROUTER_API_KEY
      → Calls https://openrouter.ai/api/v1
        → Returns AI response

User → vibe-ai kimi "prompt"
  → ~/.config/vibe-coding/ai-tools/vibe-ai.sh
    → Sources ~/.config/vibe-coding/ai-tools/kimi-config.sh
      → Uses $KIMI_API_KEY
        → Calls https://api.moonshot.cn/v1
          → Returns AI response
```

### IDE Configuration Flow:
```
User edits:
  ~/.config/vibe-coding/settings.json
    (Changes applied via symlink)
      ↓
    ~/Library/Application Support/Cursor/User/settings.json
      ↓
    Cursor reads settings
      ↓
    Theme, font, keybindings applied
```

### Music Integration Flow:
```
User → Press ⌘ ⌥ M
  → Hammerspoon (~/.hammerspoon/init.lua)
    → Executes: open "https://www.youtube.com/watch?v=jfKfPfyJRdk"
      → Opens Lofi Girl in default browser
        → Background music starts

OR

User → Type "lofi"
  → Shell alias → ~/.config/vibe-coding/music/vibe-player.sh lofi
    → Opens Lofi Girl
```

---

## 📞 Quick Reference

### Load API Keys:
```bash
bw login
export BW_SESSION=$(bw unlock --raw)
bwload
ai_status
```

### Test AI Tools:
```bash
ai-ask "Hello world!"
vibe-ai kimi "Test Kimi"
gh copilot explain "git rebase"
```

### Start Vibe Session:
```bash
vibe_start    # Shows dashboard + loads keys
lofi           # Start music
vibe-dash     # Full dashboard
vibe-help     # All commands
```

### Verify Paths:
```bash
echo $VIBE_CONFIG
echo $OPENROUTER_API_KEY  # Should show key after bwload
ls -la ~/.config/vibe-coding/
```

---

**All paths resolved and verified! 🎨**

*Generated: October 10, 2025*

