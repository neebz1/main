# 🖥️ Terminal Commands - Copy & Paste Installation

Complete step-by-step shell commands ready to paste into macOS Terminal.

---

## 📋 Prerequisites

Open Terminal.app (⌘ + Space, type "Terminal")

---

## 🚀 Installation Commands

### Step 1: Navigate to Setup Directory

```bash
cd ~/main/vibe-setup
```

### Step 2: Make Scripts Executable

```bash
chmod +x *.sh
```

### Step 3: Run Complete Installation

**Option A: One-Command Install (Recommended)**

```bash
./INSTALL.sh
```

**Option B: Manual Step-by-Step**

```bash
# Phase 1: Core tools
./00-main-setup.sh

# Phase 2: IDE detection
./01-detect-ides.sh

# Phase 3: Shell config
./02-zshrc-config.sh

# Phase 4: Bitwarden
./03-bitwarden-setup.sh

# Phase 5: Theme
./04-theme-setup.sh

# Phase 6: Shortcuts
./05-global-shortcuts.sh

# Phase 7: Music
./06-music-integration.sh

# Phase 8: AI tools
./07-ai-integrations.sh

# Phase 9: Dashboard
./08-terminal-dashboard.sh
```

### Step 4: Reload Shell

```bash
source ~/.zshrc
```

---

## 🔐 Bitwarden Setup Commands

### Login to Bitwarden

```bash
bw login
```

*(Enter your email and master password when prompted)*

### Unlock Vault

```bash
export BW_SESSION=$(bw unlock --raw)
```

*(Enter master password when prompted)*

### Add API Keys

**Method 1: Using Bitwarden App/Website**

1. Open Bitwarden
2. Create new Login items with these names:
   - `OpenRouter API`
   - `Hugging Face Token`
   - `OpenAI API Key`
   - `Anthropic API Key`
3. Store your API keys in the Password field

**Method 2: Using CLI Helper**

```bash
~/.config/vibe-coding/add-api-key.sh
```

*(Follow prompts to add each key)*

### Load Keys into Environment

```bash
bwload
```

### Verify Keys Loaded

```bash
ai_status
```

---

## 🧪 Testing Commands

### Test Vibe Session

```bash
vibe_start
```

### Test Dashboard

```bash
vibe-dash
```

### Test AI Integration

```bash
ai-ask "Say hello in 5 languages"
```

### Test Music

```bash
lofi
```

### Show Help

```bash
vibe-help
```

---

## 🎨 Optional Manual Steps

### 1. Import Terminal Theme

**For Terminal.app:**

```bash
open ~/.config/vibe-coding/themes/TokyoNight.terminal
```

Then in Terminal:
1. Go to Preferences (⌘ + ,)
2. Profiles tab
3. Select "Tokyo Night"
4. Click "Default" button

**For iTerm2:**

1. Open iTerm2 → Preferences → Profiles → Colors
2. Click "Color Presets..." → Import
3. Navigate to: `~/.config/vibe-coding/themes/tokyo-night.itermcolors`
4. Select the imported theme

### 2. Grant Hammerspoon Permissions

```bash
# Open System Preferences
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

Then:
1. Click the lock to make changes
2. Click "+"
3. Add Hammerspoon.app
4. Restart Hammerspoon:

```bash
killall Hammerspoon && open -a Hammerspoon
```

### 3. GitHub CLI Login

```bash
gh auth login
```

Follow prompts:
- Account: GitHub.com
- Protocol: HTTPS
- Authenticate: Login with web browser

### 4. Install IDE Extensions

**For Cursor:**

```bash
cursor --install-extension enkia.tokyo-night
cursor --install-extension vscode-icons-team.vscode-icons
cursor --install-extension GitHub.copilot
cursor --install-extension GitHub.copilot-chat
```

**For VS Code Insiders:**

```bash
code-insiders --install-extension enkia.tokyo-night
code-insiders --install-extension vscode-icons-team.vscode-icons
code-insiders --install-extension GitHub.copilot
code-insiders --install-extension GitHub.copilot-chat
```

---

## 🔄 Update Commands

### Update All Tools

```bash
cd ~/main/vibe-setup
./update.sh
```

### Update Homebrew Only

```bash
brew update && brew upgrade
```

### Update Node Packages

```bash
npm update -g
```

### Update Python Packages

```bash
pip3 install --upgrade pip
pip3 install --upgrade openai anthropic requests httpx
```

---

## 🧹 Maintenance Commands

### Clean Homebrew Cache

```bash
brew cleanup
```

### Clean npm Cache

```bash
npm cache clean --force
```

### View AI Usage Stats

```bash
ai-monitor stats
```

### Reset AI Usage Log

```bash
ai-monitor reset
```

### Backup Configurations

```bash
# Backup directory
mkdir -p ~/vibe-backup

# Backup important configs
cp ~/.zshrc ~/vibe-backup/
cp -r ~/.config/vibe-coding ~/vibe-backup/
cp ~/.hammerspoon/init.lua ~/vibe-backup/
```

---

## 🐛 Troubleshooting Commands

### Check Installation Status

```bash
# Check Homebrew
brew --version

# Check Node
node --version

# Check Python
python3 --version

# Check pnpm
pnpm --version

# Check Docker
docker --version

# Check Bitwarden CLI
bw --version

# Check GitHub CLI
gh --version
```

### Fix Permissions

```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) $(brew --prefix)/*

# Fix config directory permissions
chmod -R 755 ~/.config/vibe-coding
```

### Reload Hammerspoon Config

```bash
osascript -e 'tell application "Hammerspoon" to reload config'
```

### Reset Starship

```bash
# Reinstall
brew reinstall starship

# Test
starship --version
```

### Check Running Processes

```bash
# Check Hammerspoon
pgrep -x "Hammerspoon"

# Check Docker
pgrep -x "Docker"

# Check IDEs
pgrep -x "Cursor"
pgrep -x "Code"
```

### View Logs

```bash
# Homebrew logs
brew doctor

# AI usage logs
cat ~/.config/vibe-coding/logs/ai-usage.log

# System logs (recent errors)
log show --predicate 'eventMessage contains "error"' --info --last 1h
```

---

## 🎯 Daily Usage Commands

### Morning Routine

```bash
# 1. Unlock Bitwarden and load keys
export BW_SESSION=$(bw unlock --raw) && bwload

# 2. Start vibe session
vibe_start

# 3. Open workspace
ws

# 4. Start music
lofi
```

### Coding Session

```bash
# Quick AI question
ai-ask "Your question here"

# Code-specific question
ai-code "Your code question"

# Review changes
ai-review

# System status
vibe-dash
```

### End of Day

```bash
# Check AI usage
ai-monitor

# Lock Bitwarden
bw lock

# Git status (if in repo)
git status
```

---

## 📚 Learning Commands

### Explore Tools

```bash
# List all vibe commands
compgen -c | grep vibe

# List all AI commands
compgen -c | grep ai-

# List all aliases
alias | grep -E "vibe|ai|lofi"
```

### View Configurations

```bash
# View .zshrc additions
tail -100 ~/.zshrc

# View Starship config
cat ~/.config/starship.toml

# View Hammerspoon config
cat ~/.hammerspoon/init.lua

# View AI configs
ls -la ~/.config/vibe-coding/ai-tools/
```

---

## 🚀 Advanced Commands

### Custom AI Model

```bash
# Use specific model
ai-fast "Quick question"      # Haiku (fast)
ai-powerful "Complex task"    # Opus (powerful)
ai-code "Code help"           # CodeLlama
```

### Spotify Integration

```bash
# Play/pause
sp play
sp pause

# Skip tracks
sp next
sp prev

# Current track
sp status
```

### Window Management

Use keyboard shortcuts:
- `⌘ ⌥ ←` - Snap left
- `⌘ ⌥ →` - Snap right
- `⌘ ⌥ ↑` - Maximize
- `⌘ ⌥ ↓` - Center

### Network Tools

```bash
# Show local IP
ipconfig getifaddr en0

# Show public IP
myip

# Show open ports
ports

# Network monitor
sudo nettop
```

---

## 💡 Pro Tips

### Create Custom Aliases

Add to `~/.zshrc`:

```bash
# Your custom aliases
alias myproject='cd ~/path/to/project && cursor .'
alias deploy='npm run build && vercel --prod'
```

Then reload:

```bash
source ~/.zshrc
```

### Create Custom Shortcuts

Edit `~/.hammerspoon/init.lua`:

```lua
-- Custom shortcut
hs.hotkey.bind({"cmd", "alt"}, "P", function()
    -- Your custom action
end)
```

### Use AI with Pipes

```bash
# Review file
cat myfile.js | ai-code "Review this code"

# Document code
cat myfile.js | ai-ask "Generate JSDoc comments"

# Explain logs
tail -20 error.log | ai-ask "Explain these errors"
```

---

**🎨 Happy Vibe Coding!** Type `vibe-help` anytime for command reference.

