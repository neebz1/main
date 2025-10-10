# 🎨 Vibe Coding Environment - START HERE

## ✅ Setup Complete!

Your ultimate vibe-coding environment is ready to install. Everything has been configured for friction-free development with aesthetic vibes.

---

## 📦 What's Included

### 🚀 Installation Scripts (9 phases)
All scripts are **executable** and ready to run:

1. **00-main-setup.sh** - Core tools (Homebrew, Node, Python, Docker, etc.)
2. **01-detect-ides.sh** - IDE detection & shared configs
3. **02-zshrc-config.sh** - Enhanced shell with AI integrations
4. **03-bitwarden-setup.sh** - Secure API key management
5. **04-theme-setup.sh** - Tokyo Night theme + JetBrains Mono
6. **05-global-shortcuts.sh** - Hammerspoon global shortcuts
7. **06-music-integration.sh** - Lo-fi music integration
8. **07-ai-integrations.sh** - AI tools (OpenRouter, Kimi, HF, Copilot)
9. **08-terminal-dashboard.sh** - System + AI monitoring dashboard

### 📚 Documentation Files

- **INDEX.md** - Complete index of everything
- **README.md** - Full documentation (9.8KB)
- **QUICK-START.md** - 5-minute quick start guide
- **TERMINAL-COMMANDS.md** - Copy-paste terminal commands
- **INSTALL.sh** - Master installer (runs all 9 phases)
- **update.sh** - Update script for maintenance

---

## 🚀 Installation (Choose One Method)

### Method 1: One-Command Install (Recommended)

```bash
cd ~/main/vibe-setup
./INSTALL.sh
```

That's it! The installer will:
- ✅ Install all tools (Homebrew, Node, Python, Docker, etc.)
- ✅ Detect and configure your IDEs
- ✅ Set up enhanced .zshrc
- ✅ Install Bitwarden CLI
- ✅ Apply Tokyo Night theme
- ✅ Configure Hammerspoon shortcuts
- ✅ Set up lo-fi music integration
- ✅ Configure AI tools
- ✅ Create terminal dashboard

**Time: ~10-15 minutes** (depending on your internet speed)

### Method 2: Manual Step-by-Step

Follow the detailed guide in **[TERMINAL-COMMANDS.md](TERMINAL-COMMANDS.md)**

---

## 📋 After Installation

### 1. Reload Shell
```bash
source ~/.zshrc
```

### 2. Setup Bitwarden & API Keys
```bash
# Login
bw login

# Unlock and load keys
export BW_SESSION=$(bw unlock --raw)
bwload
```

### 3. Test Everything
```bash
vibe_start              # Initialize session
vibe-dash               # Show dashboard
ai-ask "Hello world!"   # Test AI
lofi                    # Start music
```

---

## ⌨️ Global Shortcuts (Hammerspoon)

After installation, these shortcuts work system-wide:

| Shortcut | Action |
|----------|--------|
| **⌘ ⌥ G** | GitHub Copilot Chat |
| **⌘ ⌥ A** | AI Console (Terminal) |
| **⌘ ⌥ C** | Open Cursor |
| **⌘ ⌥ V** | Open VS Code Insiders |
| **⌘ ⌥ W** | Open Windsurf |
| **⌘ ⌥ L** | Open Logic Pro |
| **⌘ ⌥ M** | Start Lo-fi Music |
| **⌘ ⌥ D** | Show Dashboard |
| **⌘ ⌥ S** | AI Status |
| **⌘ ⌥ ←/→** | Snap Window Left/Right |
| **⌘ ⌥ ↑/↓** | Maximize/Center Window |

---

## 🤖 AI Tools Integration

### Supported AI Platforms
- ✅ **OpenRouter** - Access to Claude, GPT-4, Gemini, Llama
- ✅ **Kimi K2** - Advanced reasoning
- ✅ **GitHub Copilot** - Code completion & chat
- ✅ **Hugging Face Hub** - ML model search

### Quick Commands
```bash
ai-ask "Your question"           # Quick AI query
ai-code "Code question"          # Code-focused
ai-review                        # Review git diff
vibe-ai or "Your prompt"         # OpenRouter
vibe-ai kimi "Your prompt"       # Kimi K2
```

---

## 🎨 Theme & Aesthetics

### Visual Identity
- **Theme**: Tokyo Night (dark, neon-inspired)
- **Font**: JetBrains Mono Nerd Font with ligatures
- **Icons**: VSCode Icons + Fluent Icons
- **Prompt**: Starship with custom vibe config

### Color Palette
```
Background: #1a1b26 (deep dark blue)
Foreground: #c0caf5 (soft white)
Accents: Purple, Cyan, Green, Orange
```

---

## 🎵 Music Integration

### Available Playlists
```bash
lofi          # Lofi Girl - Study Beats
chillhop      # Chillhop Radio
synthwave     # Synthwave Radio
```

### Music Controls
```bash
sp play/pause/next/prev   # Spotify
music-play/pause          # Music.app
⌘ ⌥ M                     # Global shortcut
```

---

## 📊 System Monitoring

### Dashboard
```bash
vibe-dash     # Full vibe dashboard
btop          # System monitor
ai-monitor    # AI usage stats
ai_status     # AI tools status
```

### Features
- 🕐 Time-based mood indicator
- 💻 System info (CPU, RAM, disk, temp)
- 🤖 AI tools status
- 🌐 Network info
- 📁 Git status (if in repo)

---

## 🔐 Security & API Keys

### Bitwarden Integration
All API keys stored securely in Bitwarden vault:

1. **OpenRouter API** (for ai-ask, vibe-ai)
2. **Hugging Face Token** (for model search)
3. **OpenAI API Key** (optional)
4. **Anthropic API Key** (optional)

### Loading Keys
```bash
bw login                          # First time only
export BW_SESSION=$(bw unlock --raw)
bwload                            # Loads all keys
```

---

## 📁 What Gets Installed

### Core Tools
- Homebrew (package manager)
- Git, Node.js, Python 3, pnpm
- Docker, ngrok
- GitHub CLI (gh)

### Terminal Tools
- **eza** - Modern ls with icons
- **bat** - Modern cat with syntax highlighting
- **btop** - Beautiful system monitor
- **fastfetch** - System info display
- **fzf** - Fuzzy finder
- **ripgrep** - Fast search
- **zoxide** - Smart cd
- **starship** - Beautiful prompt

### Development
- TypeScript, ts-node, nodemon
- Prettier, ESLint
- Vercel CLI, Netlify CLI, Firebase CLI

### Python Packages
- openai, anthropic
- requests, httpx
- python-dotenv
- rich, typer

### GUI Apps
- Hammerspoon (automation)
- Docker Desktop
- JetBrains Mono Nerd Font

---

## 📍 Configuration Locations

### Main Configs
```
~/.zshrc                           # Enhanced shell
~/.config/starship.toml            # Starship prompt
~/.hammerspoon/init.lua            # Global shortcuts
~/.config/vibe-coding/             # Vibe config root
```

### Vibe Coding Structure
```
~/.config/vibe-coding/
├── settings.json                  # Shared IDE settings
├── keybindings.json              # Shared keybindings
├── ai-tools/                     # AI integrations
├── music/                        # Music scripts
├── dashboard/                    # Dashboard scripts
├── themes/                       # Theme files
└── logs/                         # AI usage logs
```

### IDE Configs (Auto-linked)
```
~/Library/Application Support/Cursor/User/
~/Library/Application Support/Code - Insiders/User/
~/Library/Application Support/Windsurf/User/
```

---

## 🎯 Quick Command Reference

### Essential Commands
| Command | Description |
|---------|-------------|
| `vibe_start` | Start vibe session |
| `vibe-help` | Show all commands |
| `vibe-dash` | Full dashboard |
| `ai_status` | AI tools status |
| `ai-ask <prompt>` | Quick AI query |
| `lofi` | Start lo-fi music |
| `ws` | Go to ~/main workspace |
| `bwload` | Load API keys |

### File Operations
| Command | Description |
|---------|-------------|
| `ls`, `ll`, `la` | Enhanced listing (eza) |
| `lt` | Tree view |
| `cat` | Enhanced cat (bat) |
| `cd` | Smart cd (zoxide) |

---

## 🆘 Need Help?

### Documentation
1. **[INDEX.md](INDEX.md)** - Complete index
2. **[README.md](README.md)** - Full docs
3. **[QUICK-START.md](QUICK-START.md)** - Quick guide
4. **[TERMINAL-COMMANDS.md](TERMINAL-COMMANDS.md)** - All commands

### In Terminal
```bash
vibe-help     # Show all commands
ai_status     # Check AI tools
vibe-dash     # System overview
```

### Common Issues

**Shortcuts not working?**
- Grant Hammerspoon Accessibility permissions
- System Preferences → Security & Privacy → Privacy → Accessibility

**API keys not loading?**
```bash
bw unlock
export BW_SESSION=$(bw unlock --raw)
bwload
ai_status
```

**Theme not applied?**
- Restart your IDE
- Import theme: Terminal Preferences → Import `~/.config/vibe-coding/themes/TokyoNight.terminal`

---

## 🔄 Keeping Up to Date

### Update Everything
```bash
cd ~/main/vibe-setup
./update.sh
```

This updates:
- Homebrew packages
- npm packages
- Python packages
- IDE extensions
- Configurations

---

## ✨ What Makes This Special

### 🎨 Vibe Elements
- **Aesthetic**: Tokyo Night theme throughout
- **Sound**: Lo-fi music integration
- **Motion**: Smooth animations & transitions
- **Typography**: Beautiful JetBrains Mono font

### 🚀 Productivity
- **One-key shortcuts**: Access everything instantly
- **AI everywhere**: Quick prompts from terminal
- **Unified config**: Share settings across IDEs
- **Smart tools**: Enhanced ls, cat, cd, etc.

### 🔐 Security First
- **Zero plaintext**: API keys in Bitwarden vault
- **One-command load**: `bwload` to activate
- **Secure by default**: Environment isolation

### 🤖 Multi-AI
- **OpenRouter**: Access 20+ models
- **Kimi K2**: Advanced reasoning
- **Copilot**: Code assistance
- **Hugging Face**: ML models

---

## 🎯 Next Steps

1. **Run the installer**
   ```bash
   cd ~/main/vibe-setup
   ./INSTALL.sh
   ```

2. **Set up Bitwarden**
   ```bash
   bw login
   bwload
   ```

3. **Test the vibe**
   ```bash
   vibe_start
   lofi
   ai-ask "Let's build something amazing!"
   ```

4. **Explore shortcuts**
   - Press ⌘ ⌥ D for dashboard
   - Press ⌘ ⌥ M for music
   - Press ⌘ ⌥ G for Copilot

5. **Customize**
   - Edit `~/.zshrc` for aliases
   - Edit `~/.hammerspoon/init.lua` for shortcuts
   - Edit `~/.config/vibe-coding/ai-tools/openrouter-config.json` for AI models

---

## 🎉 Ready to Vibe Code?

```bash
cd ~/main/vibe-setup
./INSTALL.sh
```

**Installation time: ~10-15 minutes**

Then just type:
```bash
vibe_start
```

---

**🎨 Made with 💜 for creators who demand beautiful, friction-free development**

*Code with style. Build with vibes. Create with AI.* 🚀

