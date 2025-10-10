#!/usr/bin/env bash
# 🎨 Vibe System Master Launcher
# Unified access to all your dev tools

clear

cat << 'BANNER'
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║                     🎨 VIBE-CODING CONTROL CENTER 🎨                           ║
║                                                                                 ║
║              Everything you built today, in one place                           ║
║                                                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
BANNER

echo ""
echo "Select what you want to do:"
echo ""
echo "1) 📖 Show Quick Reference (all commands)"
echo "2) 🚀 Start Vibe Coding Session"
echo "3) 📚 Search Documentation (Docs-Agent)"
echo "4) 🤖 Ask AI a Question"
echo "5) 🎵 Start Lo-Fi Music"
echo "6) 📊 System Status (all systems)"
echo "7) 🌐 Deploy Docs-Agent to Cloud"
echo "8) 💻 Open Cursor"
echo "9) 🎹 Open Logic Pro"
echo "10) ⚙️  System Settings & Guides"
echo "0) Exit"
echo ""
read -p "Enter choice (0-10): " choice

case $choice in
    1)
        cat "$HOME/main/.vibe-system/QUICK-REFERENCE.txt"
        ;;
    2)
        vibe_start
        ;;
    3)
        cd ~/main/CursorDocsIndex && source venv/bin/activate
        read -p "Search query: " query
        python docs_cli.py search "$query"
        ;;
    4)
        read -p "Ask AI: " question
        ai-ask "$question"
        ;;
    5)
        lofi
        ;;
    6)
        echo ""
        echo "🎨 VIBE ENVIRONMENT STATUS:"
        ai_status
        echo ""
        echo "📚 DOCS-AGENT STATUS:"
        cd ~/main/CursorDocsIndex && source venv/bin/activate && python docs_cli.py stats
        echo ""
        echo "⌨️  HAMMERSPOON:"
        pgrep -x "Hammerspoon" > /dev/null && echo "✅ Running (shortcuts active)" || echo "❌ Not running"
        ;;
    7)
        cd ~/main/CursorDocsIndex
        ./deploy.sh
        ;;
    8)
        open -a Cursor
        ;;
    9)
        open -a "Logic Pro"
        ;;
    10)
        echo ""
        echo "📚 Available Guides:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        ls -1 "$HOME/main/.vibe-system/"
        echo ""
        read -p "Enter filename to read (or press Enter to skip): " file
        if [ -n "$file" ]; then
            cat "$HOME/main/.vibe-system/$file" | less
        fi
        ;;
    0)
        echo "👋 Happy coding!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac

echo ""
read -p "Press Enter to continue..."
exec "$0"

