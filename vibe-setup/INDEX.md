# 📚 Vibe Coding Environment - Complete Index

## 📂 File Structure

```
vibe-setup/
├── 📖 Documentation
│   ├── README.md                    # Complete documentation
│   ├── QUICK-START.md              # Quick start guide
│   ├── TERMINAL-COMMANDS.md        # Copy-paste terminal commands
│   └── INDEX.md                    # This file
│
├── 🚀 Installation Scripts
│   ├── INSTALL.sh                  # Master installer (run this!)
│   ├── 00-main-setup.sh           # Core tools installation
│   ├── 01-detect-ides.sh          # IDE detection & config
│   ├── 02-zshrc-config.sh         # Shell environment
│   ├── 03-bitwarden-setup.sh      # Bitwarden CLI setup
│   ├── 04-theme-setup.sh          # Tokyo Night theme
│   ├── 05-global-shortcuts.sh     # Hammerspoon shortcuts
│   ├── 06-music-integration.sh    # Lo-fi music setup
│   ├── 07-ai-integrations.sh      # AI tools config
│   └── 08-terminal-dashboard.sh   # Dashboard setup
│
└── 🔄 Maintenance
    └── update.sh                   # Update all tools
```

---

## 🚀 Quick Navigation

### For First-Time Users
1. **[QUICK-START.md](QUICK-START.md)** - Start here! 5-minute setup guide
2. **[TERMINAL-COMMANDS.md](TERMINAL-COMMANDS.md)** - Copy-paste commands
3. **[README.md](README.md)** - Full documentation

### For Installation
- **One-Command**: `./INSTALL.sh`
- **Manual Steps**: See [TERMINAL-COMMANDS.md](TERMINAL-COMMANDS.md)

### For Updates
- Run: `./update.sh`

---

## 📋 Installation Checklist

### Phase 1: Core Setup ✓
- [ ] Run `./00-main-setup.sh` - Installs Homebrew, Node, Python, Docker, etc.
- [ ] Verify: `brew --version`, `node --version`, `python3 --version`

### Phase 2: IDE Configuration ✓
- [ ] Run `./01-detect-ides.sh` - Detects and configures IDEs
- [ ] Check: `~/.config/vibe-coding/` directory created

### Phase 3: Shell Environment ✓
- [ ] Run `./02-zshrc-config.sh` - Enhanced .zshrc
- [ ] Run: `source ~/.zshrc`
- [ ] Test: `vibe_start` command works

### Phase 4: Security ✓
- [ ] Run `./03-bitwarden-setup.sh`
- [ ] Run: `bw login`
- [ ] Add API keys to Bitwarden vault
- [ ] Run: `bwload`
- [ ] Verify: `ai_status` shows ✅

### Phase 5: Aesthetics ✓
- [ ] Run `./04-theme-setup.sh`
- [ ] Import Tokyo Night theme in Terminal
- [ ] Restart IDEs

### Phase 6: Shortcuts ✓
- [ ] Run `./05-global-shortcuts.sh`
- [ ] Grant Accessibility permissions to Hammerspoon
- [ ] Test: Press ⌘ ⌥ D

### Phase 7: Music ✓
- [ ] Run `./06-music-integration.sh`
- [ ] Test: `lofi` command
- [ ] Test: ⌘ ⌥ M shortcut

### Phase 8: AI Tools ✓
- [ ] Run `./07-ai-integrations.sh`
- [ ] Test: `ai-ask "Hello"`
- [ ] Test: `vibe-ai or "Test"`

### Phase 9: Dashboard ✓
- [ ] Run `./08-terminal-dashboard.sh`
- [ ] Test: `vibe-dash`
- [ ] Test: `vibe-help`

---

## 🎯 Essential Commands

### Quick Reference
| Category | Command | Description |
|----------|---------|-------------|
| **Start** | `vibe_start` | Initialize vibe session |
| **Help** | `vibe-help` | Show all commands |
| **Dashboard** | `vibe-dash` | Full dashboard |
| **AI** | `ai-ask <prompt>` | Quick AI query |
| **Music** | `lofi` | Start lo-fi beats |
| **Status** | `ai_status` | Check AI tools |
| **Update** | `./update.sh` | Update everything |

### Global Shortcuts
| Shortcut | Action |
|----------|--------|
| ⌘ ⌥ G | GitHub Copilot Chat |
| ⌘ ⌥ A | Terminal (AI Console) |
| ⌘ ⌥ C | Open Cursor |
| ⌘ ⌥ V | Open VS Code Insiders |
| ⌘ ⌥ W | Open Windsurf |
| ⌘ ⌥ L | Open Logic Pro |
| ⌘ ⌥ M | Start Music |
| ⌘ ⌥ D | Show Dashboard |
| ⌘ ⌥ S | AI Status |

---

## 🗂️ Configuration Locations

### Shell
- Main config: `~/.zshrc`
- Starship: `~/.config/starship.toml`
- Hammerspoon: `~/.hammerspoon/init.lua`

### Vibe Coding
- Base: `~/.config/vibe-coding/`
- AI tools: `~/.config/vibe-coding/ai-tools/`
- Music: `~/.config/vibe-coding/music/`
- Dashboard: `~/.config/vibe-coding/dashboard/`
- Themes: `~/.config/vibe-coding/themes/`

### IDE Configs
- Cursor: `~/Library/Application Support/Cursor/User/`
- VS Code Insiders: `~/Library/Application Support/Code - Insiders/User/`
- Windsurf: `~/Library/Application Support/Windsurf/User/`

### Shared IDE
- Settings: `~/.config/vibe-coding/settings.json`
- Keybindings: `~/.config/vibe-coding/keybindings.json`

---

## 🔧 What Each Script Does

### 00-main-setup.sh
- Installs Homebrew (if needed)
- Installs core dev tools: Git, Node, Python, pnpm, Docker, ngrok
- Installs terminal tools: eza, bat, btop, fastfetch, fzf, ripgrep, zoxide
- Installs Bitwarden CLI, Hammerspoon
- Installs JetBrains Mono Nerd Font
- Sets up fzf key bindings

### 01-detect-ides.sh
- Detects Cursor, VS Code Insiders, Windsurf
- Creates shared config directory
- Generates keybindings.json with vibe shortcuts
- Generates settings.json with Tokyo Night theme
- Symlinks configs to each IDE
- Lists recommended extensions

### 02-zshrc-config.sh
- Backs up existing .zshrc
- Creates new enhanced .zshrc with:
  - Homebrew setup
  - PATH configuration
  - AI tool environment variables
  - Bitwarden integration functions
  - Starship prompt
  - Enhanced tool aliases (eza, bat, zoxide)
  - AI shortcuts and functions
  - Vibe functions (vibe_start, vibe_dash, vibe_music)
  - Auto-startup initialization

### 03-bitwarden-setup.sh
- Ensures Bitwarden CLI is installed
- Provides setup instructions
- Lists API keys to add
- Creates helper script for adding keys via CLI

### 04-theme-setup.sh
- Installs Oh My Zsh (optional)
- Installs Powerlevel10k theme
- Creates Starship config with Tokyo Night colors
- Generates iTerm2 color scheme
- Generates Terminal.app profile
- Installs IDE theme extensions

### 05-global-shortcuts.sh
- Installs Hammerspoon
- Creates init.lua with shortcuts:
  - App launchers (⌘ ⌥ C/V/W/L/B)
  - AI shortcuts (⌘ ⌥ G/A/D/S)
  - Music shortcut (⌘ ⌥ M)
  - Window management (⌘ ⌥ arrows)
- Auto-reload on config change
- Starts Hammerspoon

### 06-music-integration.sh
- Creates music player script
- Configures lo-fi playlists (Lofi Girl, Chillhop, Synthwave)
- Creates Spotify CLI controls
- Creates Music.app controls
- Adds music aliases
- Sets up workspace triggers

### 07-ai-integrations.sh
- Creates Cursor AI rules file
- Configures OpenRouter with model presets
- Creates OpenRouter CLI (Python)
- Configures Kimi K2 integration
- Creates Hugging Face CLI
- Creates unified vibe-ai interface
- Adds AI tool aliases

### 08-terminal-dashboard.sh
- Configures fastfetch with custom layout
- Creates vibe-dashboard.sh with:
  - Mood indicator (time-based)
  - System info (fastfetch/neofetch)
  - Live metrics (CPU, RAM, disk, temp)
  - AI tools status
  - Running services
  - Network info
  - Git status (if in repo)
- Creates AI usage monitor
- Creates help system (vibe-help)
- Adds dashboard aliases

### INSTALL.sh (Master)
- Runs all 9 phases in order
- Shows progress
- Displays next steps
- Lists shortcuts
- Provides troubleshooting tips

### update.sh
- Updates Homebrew packages
- Updates npm global packages
- Updates Python packages
- Updates IDE extensions
- Reloads configurations

---

## 🎨 Theme Details

### Colors (Tokyo Night)
- Background: `#1a1b26`
- Foreground: `#c0caf5`
- Accent Blue: `#7aa2f7`
- Accent Purple: `#bb9af7`
- Accent Cyan: `#7dcfff`
- Accent Green: `#9ece6a`
- Accent Orange: `#ff9e64`
- Accent Red: `#f7768e`

### Font
- **Primary**: JetBrains Mono Nerd Font
- **Size**: 14px (editor), 13px (terminal)
- **Features**: Ligatures enabled
- **Line Height**: 1.6

---

## 🤖 AI Tool Endpoints

### OpenRouter
- API Base: `https://openrouter.ai/api/v1`
- Default Model: `anthropic/claude-3.5-sonnet`
- Config: `~/.config/vibe-coding/ai-tools/openrouter-config.json`

### Kimi K2
- API Base: `https://api.moonshot.cn/v1`
- Model: `moonshot-v1-8k`
- Config: `~/.config/vibe-coding/ai-tools/kimi-config.sh`

### Hugging Face
- Token env: `HF_TOKEN`
- CLI: `~/.config/vibe-coding/ai-tools/huggingface-cli.py`

### GitHub Copilot
- Requires: GitHub CLI (`gh`)
- Commands: `gh copilot explain`, `gh copilot suggest`

---

## 🔐 API Keys Required

Store these in Bitwarden:

1. **OpenRouter API** (Required for `ai-ask`, `vibe-ai`)
   - Get from: https://openrouter.ai/

2. **Hugging Face Token** (Optional - for model search)
   - Get from: https://huggingface.co/settings/tokens

3. **OpenAI API Key** (Optional - for direct OpenAI access)
   - Get from: https://platform.openai.com/api-keys

4. **Anthropic API Key** (Optional - for direct Claude access)
   - Get from: https://console.anthropic.com/

5. **Kimi K2 API Key** (Optional - for Kimi integration)
   - Get from: Kimi documentation

---

## 📊 Monitoring & Logs

### AI Usage Tracking
- Log: `~/.config/vibe-coding/logs/ai-usage.log`
- View: `ai-monitor stats`
- Reset: `ai-monitor reset`

### System Monitoring
- Live: `btop` or `vibe-dash`
- Network: `sudo nettop`
- Ports: `ports` (alias for `lsof -i -P | grep LISTEN`)

---

## 🆘 Troubleshooting Index

### Common Issues

| Issue | Solution |
|-------|----------|
| Shortcuts not working | Grant Hammerspoon Accessibility permissions |
| API keys not loading | Run `bw unlock` then `bwload` |
| Theme not applied | Restart IDE, check font installation |
| Command not found | Run `source ~/.zshrc` |
| Starship not showing | Check `.zshrc` has `eval "$(starship init zsh)"` |

### Reset Commands

```bash
# Reset Bitwarden session
bw lock && bw unlock

# Reset Hammerspoon
killall Hammerspoon && open -a Hammerspoon

# Reset shell config
source ~/.zshrc

# Reset AI usage log
ai-monitor reset

# Reinstall everything
./INSTALL.sh
```

---

## 🚀 Next Steps After Installation

1. **Test Everything**
   ```bash
   vibe_start
   ai_status
   vibe-dash
   ```

2. **Add Your Projects**
   ```bash
   # Edit ~/.zshrc to add
   alias myproject='cd ~/path && cursor .'
   ```

3. **Customize Shortcuts**
   ```bash
   # Edit ~/.hammerspoon/init.lua
   nano ~/.hammerspoon/init.lua
   ```

4. **Set Up Git**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   gh auth login
   ```

5. **Explore AI Tools**
   ```bash
   ai-ask "Explain async/await"
   ai-code "Write a React hook"
   ai-review  # In git repo
   ```

---

## 📚 Additional Resources

### Official Docs
- [Homebrew](https://brew.sh)
- [Starship](https://starship.rs)
- [Hammerspoon](https://www.hammerspoon.org)
- [Bitwarden CLI](https://bitwarden.com/help/cli/)
- [OpenRouter](https://openrouter.ai/docs)

### Vibe Coding Docs
- Full Guide: [README.md](README.md)
- Quick Start: [QUICK-START.md](QUICK-START.md)
- Commands: [TERMINAL-COMMANDS.md](TERMINAL-COMMANDS.md)

### Community
- Create issues/PRs for improvements
- Share your customizations
- Add more AI integrations

---

**🎨 Made with 💜 for vibe coders**

*Last updated: October 2025*

