# 🎨 Vibe Coding Environment

> The ultimate macOS setup for multi-AI, multi-tool creators who demand friction-free development with aesthetic vibes.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🛠️ Development Tools
- **IDEs**: Auto-configuration for Cursor, VS Code Insiders, and Windsurf
- **Package Managers**: Homebrew, npm, pnpm, pip
- **Runtimes**: Node.js, Python 3
- **Infrastructure**: Docker, ngrok
- **Terminal Tools**: eza, bat, btop, fastfetch, fzf, ripgrep, zoxide

### 🤖 AI Integrations
- **OpenRouter**: Access to Claude, GPT-4, Gemini, and more
- **Kimi K2**: Advanced AI reasoning
- **GitHub Copilot**: Code completion and chat
- **Hugging Face Hub**: ML model search and deployment
- **Unified Interface**: Single command to query multiple AI tools

### 🎨 Aesthetic & Vibe
- **Theme**: Tokyo Night color palette throughout
- **Font**: JetBrains Mono Nerd Font with ligatures
- **Icons**: VSCode Icons + Fluent Icons
- **Prompt**: Starship with custom vibe-coding configuration
- **Dashboard**: Beautiful terminal dashboard with system stats

### 🔐 Security
- **Bitwarden CLI**: Secure API key management
- **Environment Isolation**: API keys never stored in plaintext
- **Vault Integration**: One-command key loading from Bitwarden

### ⌨️ Global Shortcuts (Hammerspoon)
- `⌘ ⌥ G` - Launch GitHub Copilot Chat
- `⌘ ⌥ A` - AI Console (Terminal)
- `⌘ ⌥ C` - Open Cursor
- `⌘ ⌥ V` - Open VS Code Insiders
- `⌘ ⌥ W` - Open Windsurf
- `⌘ ⌥ L` - Open Logic Pro
- `⌘ ⌥ M` - Start Lo-fi Music
- `⌘ ⌥ D` - Show Dashboard
- `⌘ ⌥ S` - AI Status
- `⌘ ⌥ ←/→/↑/↓` - Window management

### 🎵 Music Integration
- Auto-play lo-fi on workspace open
- Spotify CLI controls
- Music.app integration
- Pre-configured playlists (Lofi Girl, Chillhop, Synthwave)

### 📊 Monitoring
- System resource dashboard
- AI usage tracking
- Network monitoring
- Git status display

---

## 🚀 Quick Start

### One-Command Installation

```bash
cd ~/main/vibe-setup
chmod +x INSTALL.sh
./INSTALL.sh
```

### Manual Step-by-Step Installation

#### 1. Core Tools Setup

```bash
chmod +x 00-main-setup.sh
./00-main-setup.sh
```

This installs:
- Homebrew
- Git, Node.js, Python 3, pnpm
- Docker, ngrok
- Terminal tools (eza, bat, btop, fastfetch, fzf, ripgrep, zoxide)
- JetBrains Mono Nerd Font

#### 2. IDE Detection & Configuration

```bash
./01-detect-ides.sh
```

Detects and configures:
- Cursor
- VS Code Insiders  
- Windsurf

Creates shared keybindings and settings with Tokyo Night theme.

#### 3. Shell Environment

```bash
./02-zshrc-config.sh
```

Configures `.zshrc` with:
- AI tool environment variables
- Enhanced aliases (ls → eza, cat → bat)
- Starship prompt
- Vibe coding functions
- Auto-startup dashboard

**Then reload:**
```bash
source ~/.zshrc
```

#### 4. Bitwarden Setup

```bash
./03-bitwarden-setup.sh
```

Sets up Bitwarden CLI for secure API key management.

**Login and load keys:**
```bash
bw login
export BW_SESSION=$(bw unlock --raw)
bwload  # Loads API keys into environment
```

#### 5. Theme & Aesthetics

```bash
./04-theme-setup.sh
```

Applies:
- Tokyo Night terminal theme
- Starship prompt configuration
- IDE theme extensions

**Manual step:** Import `~/.config/vibe-coding/themes/TokyoNight.terminal` in Terminal.app Preferences.

#### 6. Global Shortcuts

```bash
./05-global-shortcuts.sh
```

Installs and configures Hammerspoon for global shortcuts.

**Manual step:** Grant Accessibility permissions to Hammerspoon in System Preferences → Security & Privacy → Privacy → Accessibility.

#### 7. Music Integration

```bash
./06-music-integration.sh
```

Sets up lo-fi music integration with workspace triggers.

#### 8. AI Tool Integrations

```bash
./07-ai-integrations.sh
```

Configures:
- OpenRouter CLI
- Kimi K2 integration
- Hugging Face Hub CLI
- GitHub Copilot
- Unified AI interface

#### 9. Terminal Dashboard

```bash
./08-terminal-dashboard.sh
```

Creates vibe dashboard with system monitoring and AI status.

---

## 📋 Post-Installation

### 1. Add API Keys to Bitwarden

Create these items in your Bitwarden vault:

| Item Name | Type | Field |
|-----------|------|-------|
| OpenRouter API | Login | Password: `<your-api-key>` |
| Hugging Face Token | Login | Password: `<your-token>` |
| OpenAI API Key | Login | Password: `<your-api-key>` |
| Anthropic API Key | Login | Password: `<your-api-key>` |

**Or use the helper script:**
```bash
~/.config/vibe-coding/add-api-key.sh
```

### 2. GitHub CLI Login

```bash
gh auth login
```

### 3. Test the Setup

```bash
vibe_start              # Initialize vibe session
vibe-dash               # Show full dashboard  
vibe-help               # Show all commands
ai-ask 'Hello world!'   # Test AI integration
lofi                    # Start lo-fi music
```

---

## 🎯 Command Reference

### Vibe Commands

```bash
vibe_start        # Start vibe coding session
vibe-dash         # Show dashboard
vibe-help         # Show help
vibe-music        # Music player
ai_status         # Show AI tools status
```

### AI Tools

```bash
# Unified interface
vibe-ai or <prompt>      # OpenRouter
vibe-ai kimi <prompt>    # Kimi K2
vibe-ai gh <prompt>      # GitHub Copilot

# Direct commands
ai-ask <prompt>          # OpenRouter (default)
ai-fast <prompt>         # Fast model (Haiku)
ai-code <prompt>         # Code model
ai-powerful <prompt>     # Powerful model (Opus)
kimi <prompt>            # Kimi K2
hf-search <query>        # Search HuggingFace

# Copilot
copilot explain <cmd>    # Explain command
copilot suggest          # Suggest command

# Workflows
ai-review                # Review git diff
ai-docs <file>           # Generate docs
```

### Music Controls

```bash
# Quick start
lofi                     # Lofi Girl
chillhop                 # Chillhop radio
synthwave                # Synthwave radio

# Spotify
sp play/pause/next/prev  # Controls
sp status                # Current track

# Music.app
music-play/pause/next/prev
```

### File Operations

```bash
ls / ll / la             # Enhanced listing (eza)
lt                       # Tree view
cat                      # Enhanced cat (bat)
cd                       # Smart cd (zoxide)
```

### Workspace

```bash
ws                       # Go to ~/main
cursor                   # Open Cursor
logic                    # Open Logic Pro
```

### Security

```bash
bw login                 # Login to Bitwarden
bw unlock                # Unlock vault
bwload                   # Load API keys
```

### System

```bash
btop                     # System monitor
fastfetch                # System info
ports                    # Show listening ports
myip                     # Show public IP
```

---

## 🎨 Customization

### Change Theme Colors

Edit `~/.config/starship.toml` to customize the prompt.

### Add Custom Shortcuts

Edit `~/.hammerspoon/init.lua` to add or modify global shortcuts.

### Configure AI Models

Edit `~/.config/vibe-coding/ai-tools/openrouter-config.json`:

```json
{
  "default_model": "anthropic/claude-3.5-sonnet",
  "models": {
    "fast": "anthropic/claude-3-haiku",
    "custom": "your-preferred-model"
  }
}
```

### Add More Playlists

Edit `~/.config/vibe-coding/music/vibe-player.sh`:

```bash
PLAYLISTS=(
    "https://your-playlist-url|Custom Playlist"
)
```

---

## 📁 Directory Structure

```
~/.config/vibe-coding/
├── settings.json              # Shared IDE settings
├── keybindings.json           # Shared keybindings
├── extensions.txt             # Recommended extensions
├── themes/
│   ├── TokyoNight.terminal   # Terminal theme
│   └── tokyo-night.itermcolors
├── ai-tools/
│   ├── openrouter-config.json
│   ├── openrouter-cli.py
│   ├── kimi-config.sh
│   ├── huggingface-cli.py
│   ├── vibe-ai.sh
│   └── aliases.sh
├── music/
│   ├── vibe-player.sh
│   ├── spotify-control.sh
│   └── aliases.sh
├── dashboard/
│   ├── vibe-dashboard.sh
│   ├── ai-monitor.sh
│   ├── vibe-help.sh
│   └── aliases.sh
└── logs/
    └── ai-usage.log
```

---

## 🔧 Troubleshooting

### Hammerspoon shortcuts not working
- Grant Accessibility permissions in System Preferences
- Restart Hammerspoon: `open -a Hammerspoon`

### API keys not loading
- Ensure Bitwarden is unlocked: `bw unlock`
- Set session: `export BW_SESSION=$(bw unlock --raw)`
- Run: `bwload`

### Starship prompt not showing
- Ensure Starship is installed: `brew install starship`
- Add to `.zshrc`: `eval "$(starship init zsh)"`
- Reload: `source ~/.zshrc`

### Theme not applied in IDE
- Restart IDE
- Manually install: `cursor --install-extension enkia.tokyo-night`
- Set in settings: `"workbench.colorTheme": "Tokyo Night"`

### Font not showing ligatures
- Ensure font is installed: `brew install --cask font-jetbrains-mono-nerd-font`
- Set in IDE: `"editor.fontFamily": "'JetBrains Mono'"`
- Enable ligatures: `"editor.fontLigatures": true`

---

## 🤝 Contributing

This is a personal setup, but feel free to fork and customize for your needs!

---

## 📝 License

MIT License - Do whatever you want with this!

---

## 🙏 Credits

- **Themes**: [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme)
- **Fonts**: [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- **Tools**: Homebrew, Starship, Hammerspoon, and the amazing open-source community

---

## 🚀 What's Next?

- [ ] Add support for more AI providers
- [ ] Create update script for easy maintenance
- [ ] Add preset workspaces for different project types
- [ ] Integrate with Raycast for additional shortcuts
- [ ] Add voice control for hands-free coding

---

**Made with 💜 for vibe coders everywhere**

🎨 *Code with style. Build with vibes.* 🚀

