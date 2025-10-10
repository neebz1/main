#!/usr/bin/env bash
# 🔍 IDE Detection & Configuration Linking
# Detects Cursor, VS Code Insiders, Windsurf and links shared configs

set -e

echo "🔍 Detecting installed IDEs..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# IDE paths
CURSOR_PATH="$HOME/Library/Application Support/Cursor"
VSCODE_INSIDERS_PATH="$HOME/Library/Application Support/Code - Insiders"
WINDSURF_PATH="$HOME/Library/Application Support/Windsurf"

# Shared config directory
SHARED_CONFIG="$HOME/.config/vibe-coding"
mkdir -p "$SHARED_CONFIG"

# Detect IDEs
IDES_FOUND=()

if [ -d "$CURSOR_PATH" ]; then
    echo "✅ Cursor detected"
    IDES_FOUND+=("cursor")
fi

if [ -d "$VSCODE_INSIDERS_PATH" ]; then
    echo "✅ VS Code Insiders detected"
    IDES_FOUND+=("vscode-insiders")
fi

if [ -d "$WINDSURF_PATH" ]; then
    echo "✅ Windsurf detected"
    IDES_FOUND+=("windsurf")
fi

if [ ${#IDES_FOUND[@]} -eq 0 ]; then
    echo "⚠️  No supported IDEs found"
    exit 0
fi

echo ""
echo "📋 Found ${#IDES_FOUND[@]} IDE(s)"

# Create shared keybindings
cat > "$SHARED_CONFIG/keybindings.json" << 'EOF'
[
  // Vibe Coding Global Shortcuts
  {
    "key": "cmd+alt+g",
    "command": "github.copilot.chat.open",
    "when": "!terminalFocus"
  },
  {
    "key": "cmd+alt+a",
    "command": "workbench.action.terminal.focus"
  },
  {
    "key": "cmd+alt+e",
    "command": "workbench.action.quickOpen"
  },
  {
    "key": "cmd+alt+w",
    "command": "workbench.action.switchWindow"
  },
  {
    "key": "cmd+alt+t",
    "command": "workbench.action.togglePanel"
  },
  {
    "key": "cmd+shift+l",
    "command": "editor.action.formatDocument"
  }
]
EOF

# Create shared settings
cat > "$SHARED_CONFIG/settings.json" << 'EOF'
{
  "workbench.colorTheme": "Tokyo Night",
  "editor.fontFamily": "'JetBrains Mono', Menlo, Monaco, 'Courier New', monospace",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "editor.lineHeight": 1.6,
  "editor.cursorBlinking": "smooth",
  "editor.cursorSmoothCaretAnimation": "on",
  "editor.smoothScrolling": true,
  "terminal.integrated.fontFamily": "'JetBrains Mono Nerd Font'",
  "terminal.integrated.fontSize": 13,
  "workbench.iconTheme": "vscode-icons",
  "workbench.productIconTheme": "fluent-icons",
  "editor.minimap.enabled": true,
  "editor.minimap.renderCharacters": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.inlineSuggest.enabled": true,
  "workbench.startupEditor": "none",
  "window.zoomLevel": 0,
  "git.autofetch": true,
  "git.confirmSync": false,
  "files.autoSave": "onFocusChange",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit"
  }
}
EOF

# Create shared extensions list
cat > "$SHARED_CONFIG/extensions.txt" << 'EOF'
# Theme & Aesthetics
enkia.tokyo-night
vscode-icons-team.vscode-icons
miguelsolorio.fluent-icons

# AI Tools
GitHub.copilot
GitHub.copilot-chat

# Productivity
eamodio.gitlens
usernamehw.errorlens
christian-kohler.path-intellisense
formulahendry.auto-rename-tag
ms-vscode.live-server

# Languages
dbaeumer.vscode-eslint
esbenp.prettier-vscode
ms-python.python
bradlc.vscode-tailwindcss
EOF

# Link configs to each IDE
for ide in "${IDES_FOUND[@]}"; do
    case $ide in
        cursor)
            IDE_CONFIG="$CURSOR_PATH/User"
            ;;
        vscode-insiders)
            IDE_CONFIG="$VSCODE_INSIDERS_PATH/User"
            ;;
        windsurf)
            IDE_CONFIG="$WINDSURF_PATH/User"
            ;;
    esac
    
    mkdir -p "$IDE_CONFIG"
    
    echo "🔗 Linking configs to $ide..."
    
    # Backup existing configs
    [ -f "$IDE_CONFIG/keybindings.json" ] && mv "$IDE_CONFIG/keybindings.json" "$IDE_CONFIG/keybindings.json.backup"
    [ -f "$IDE_CONFIG/settings.json" ] && mv "$IDE_CONFIG/settings.json" "$IDE_CONFIG/settings.json.backup"
    
    # Create symlinks
    ln -sf "$SHARED_CONFIG/keybindings.json" "$IDE_CONFIG/keybindings.json"
    ln -sf "$SHARED_CONFIG/settings.json" "$IDE_CONFIG/settings.json"
done

echo ""
echo "✅ IDE configurations linked successfully!"
echo "📁 Shared configs location: $SHARED_CONFIG"
echo ""
echo "📦 Install recommended extensions by running:"
for ide in "${IDES_FOUND[@]}"; do
    case $ide in
        cursor)
            echo "   cursor --install-extension <extension-id>"
            ;;
        vscode-insiders)
            echo "   code-insiders --install-extension <extension-id>"
            ;;
    esac
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

