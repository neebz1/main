#!/bin/bash
# 🚀 ONE-CLICK SETUP - Run this to set up everything!

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          🎹 AI MUSIC STUDIO - ONE-CLICK SETUP 🎹            ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Setting up your complete AI music production environment..."
echo ""

cd /Users/nr/Documents/GitHub/main

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "ℹ️  Creating .env file..."
    cat > .env << 'EOF'
# AI API Keys (add your keys here)
TOGETHER_API_KEY=your_together_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Gradio Password (set a secure password)
GRADIO_PASSWORD=music2025

# API Secret Key (generate with: openssl rand -hex 32)
SECRET_KEY=your_secret_key_here

# Allowed Origins for API
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
EOF
    echo "✅ Created .env file - PLEASE ADD YOUR API KEYS!"
else
    echo "✅ .env file exists"
fi

# Create Desktop Shortcuts file
echo ""
echo "ℹ️  Creating shortcuts reference..."
./create_wallpaper.sh > Desktop-Shortcuts.txt 2>&1
echo "✅ Created Desktop-Shortcuts.txt"

# Create dock app
echo ""
echo "ℹ️  Creating Dock launcher..."
mkdir -p ~/Applications/"AI Music Studio.app"/Contents/MacOS
mkdir -p ~/Applications/"AI Music Studio.app"/Contents/Resources

cat > ~/Applications/"AI Music Studio.app"/Contents/MacOS/launch << 'EOFAPP'
#!/bin/bash
cd /Users/nr/Documents/GitHub/main
python3 setup_wizard.py &
EOFAPP

chmod +x ~/Applications/"AI Music Studio.app"/Contents/MacOS/launch

cat > ~/Applications/"AI Music Studio.app"/Contents/Info.plist << 'EOFPLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch</string>
    <key>CFBundleName</key>
    <string>AI Music Studio</string>
    <key>CFBundleIdentifier</key>
    <string>com.noah.aimusicstudio</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>
EOFPLIST

echo "✅ Created AI Music Studio.app in ~/Applications"

# Create keyboard shortcuts file
echo ""
echo "ℹ️  Creating keyboard shortcuts..."
cat > SHORTCUTS.md << 'EOFSHORT'
# 🎯 AI Music Studio - Keyboard Shortcuts

## 🎹 Application Shortcuts

| App | Shortcut | Port |
|-----|----------|------|
| 🎹 Logic Pro Copilot | `Ctrl+Opt+M` | 7860 |
| 🎚️ AI Mixing Engineer | `Ctrl+Opt+E` | 7861 |
| ☁️ Cloud AI Builder | `Ctrl+Opt+C` | 7862 |
| 🔌 REST API | `Ctrl+Opt+A` | 8000 |
| 🧙 Setup Wizard | `Ctrl+Opt+W` | 7777 |

## 📁 Terminal Commands

```bash
cd /Users/nr/Documents/GitHub/main

./start-music-ai.sh           # Start Logic Pro Copilot
./start-ai-mixing-engineer.sh # Start AI Mixing Engineer
./start-cloud-builder.sh      # Start Cloud Builder
./start-api.sh                # Start REST API
python3 setup_wizard.py       # Launch Setup Wizard
./security-check.sh           # Run Security Audit
```

## 🎛️ Logitech MX Keys Mini

- `F1` - Launch Music AI
- `F2` - Launch Mixing AI
- `F3` - Launch Cloud Builder
- `F4` - Open Logic Pro
- `F5` - Record
- `F6` - Play/Pause

## 🖱️ Logitech MX Mouse

- `Button 4` - Next Track
- `Button 5` - Previous Track
- `Middle Click` - Terminal

EOFSHORT
echo "✅ Created SHORTCUTS.md"

# Test all apps
echo ""
echo "ℹ️  Testing applications..."
apps_ok=true

test_app() {
    if [ -f "$1" ]; then
        echo "  ✅ $2"
    else
        echo "  ❌ $2 not found"
        apps_ok=false
    fi
}

test_app "logic_copilot_lite.py" "Logic Pro Copilot"
test_app "ai_mixing_engineer.py" "AI Mixing Engineer"
test_app "cloud_ai_builder.py" "Cloud AI Builder"
test_app "api/main.py" "REST API"
test_app "setup_wizard.py" "Setup Wizard"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║                    ✅ SETUP COMPLETE! ✅                     ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 NEXT STEPS:"
echo ""
echo "1. ✏️  Edit .env file and add your API keys:"
echo "   open .env"
echo ""
echo "2. 🖱️  Add to Dock:"
echo "   - Open Finder → Applications"
echo "   - Drag 'AI Music Studio' to your Dock"
echo ""
echo "3. 🖼️  Set wallpaper (optional):"
echo "   - Open Desktop-Shortcuts.txt"
echo "   - Take a screenshot (Cmd+Shift+4)"
echo "   - Set as desktop wallpaper"
echo ""
echo "4. 🚀 Launch apps:"
echo "   ./start-music-ai.sh"
echo "   ./start-ai-mixing-engineer.sh"
echo "   ./start-cloud-builder.sh"
echo ""
echo "5. 🧙 Or use the Setup Wizard:"
echo "   python3 setup_wizard.py"
echo "   (Opens at http://localhost:7777)"
echo ""
echo "📚 Read YOUR-ORGANIZED-ENVIRONMENT.md for complete guide!"
echo ""
echo "🎵 Ready to make music! 🎵"
echo ""

