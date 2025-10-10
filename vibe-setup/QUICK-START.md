# 🚀 Vibe Coding - Quick Start Guide

## Installation (5 minutes)

### One Command Install:
```bash
cd ~/main/vibe-setup
chmod +x INSTALL.sh
./INSTALL.sh
```

### After Installation:

1. **Reload Shell**
   ```bash
   source ~/.zshrc
   ```

2. **Setup Bitwarden**
   ```bash
   bw login
   export BW_SESSION=$(bw unlock --raw)
   ```

3. **Add API Keys to Bitwarden**
   - Open Bitwarden app/website
   - Create items: "OpenRouter API", "Hugging Face Token", "OpenAI API Key", "Anthropic API Key"
   - Store keys in Password field

4. **Load Keys**
   ```bash
   bwload
   ```

5. **Test Setup**
   ```bash
   vibe_start
   ai-ask "Hello world!"
   ```

---

## Essential Commands (Cheat Sheet)

### 🎨 Vibe Commands
| Command | Description |
|---------|-------------|
| `vibe_start` | Start vibe session |
| `vibe-dash` | Show dashboard |
| `vibe-help` | Show all commands |
| `ai_status` | AI tools status |

### 🤖 AI Tools
| Command | Description |
|---------|-------------|
| `ai-ask <prompt>` | Quick AI query |
| `ai-code <prompt>` | Code-focused AI |
| `ai-review` | Review git diff |
| `copilot explain <cmd>` | Explain command |

### 🎵 Music
| Command | Description |
|---------|-------------|
| `lofi` | Start lo-fi beats |
| `sp play/pause` | Spotify control |

### ⌨️ Global Shortcuts
| Shortcut | Action |
|----------|--------|
| `⌘ ⌥ G` | GitHub Copilot |
| `⌘ ⌥ A` | Terminal |
| `⌘ ⌥ C` | Cursor |
| `⌘ ⌥ M` | Music |
| `⌘ ⌥ D` | Dashboard |

---

## Daily Workflow

### Morning Setup
```bash
# 1. Load API keys
bwload

# 2. Start vibe session
vibe_start

# 3. Open workspace
ws

# 4. Start music
lofi
```

### Coding Session
```bash
# Ask AI for help
ai-ask "How do I use React hooks?"

# Get code suggestions
ai-code "Write a function to debounce API calls"

# Review your changes
ai-review

# Show system stats
vibe-dash
```

### End of Day
```bash
# Check AI usage
ai-monitor

# Lock Bitwarden
bw lock
```

---

## Troubleshooting

### API keys not working?
```bash
# Unlock Bitwarden
export BW_SESSION=$(bw unlock --raw)
bwload
ai_status  # Check if keys loaded
```

### Shortcuts not working?
1. Open System Preferences → Security & Privacy
2. Privacy → Accessibility
3. Add Hammerspoon
4. Restart Hammerspoon

### Theme not applied?
```bash
# Restart IDE
# Or manually:
cursor --install-extension enkia.tokyo-night
```

---

## Update Your Setup

```bash
cd ~/main/vibe-setup
git pull  # If using git
./INSTALL.sh  # Re-run installer
```

---

**Happy Vibe Coding! 🎨**

