#!/usr/bin/env bash
# 🔗 Integrate Docs-Agent with Vibe Environment

set -e

echo "🔗 Integrating Docs-Agent with vibe-coding environment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Add Docs-Agent aliases to .zshrc if not already there
if ! grep -q "# Docs-Agent Integration" ~/.zshrc; then
    cat >> ~/.zshrc << 'EOF'

# ━━━ Docs-Agent Integration ━━━
export DOCS_AGENT_PATH="$HOME/main/CursorDocsIndex"

# Quick docs access
alias docs='cd $DOCS_AGENT_PATH && source venv/bin/activate && python docs_cli.py'
alias docs-search='cd $DOCS_AGENT_PATH && source venv/bin/activate && python docs_cli.py search'
alias docs-lookup='cd $DOCS_AGENT_PATH && source venv/bin/activate && python docs_cli.py lookup'
alias docs-stats='cd $DOCS_AGENT_PATH && source venv/bin/activate && python docs_cli.py stats'
alias docs-ingest='cd $DOCS_AGENT_PATH && source venv/bin/activate && python docs_cli.py ingest'

# API server controls
alias docs-api-start='cd $DOCS_AGENT_PATH && source venv/bin/activate && python api_server.py'
alias docs-api-test='cd $DOCS_AGENT_PATH && source venv/bin/activate && ./test-api.sh'

# Quick doc lookup for AI prompts
ai-with-docs() {
    local topic="$1"
    shift
    local question="$*"
    
    echo "📚 Looking up documentation for: $topic"
    cd "$DOCS_AGENT_PATH" && source venv/bin/activate
    local docs=$(python docs_cli.py lookup "$topic" 2>/dev/null | grep -A 20 "excerpt" | tail -15)
    
    if [ -n "$docs" ]; then
        echo "✅ Found documentation!"
        echo ""
        echo "Using with AI..."
        ai-ask "Based on this documentation: $docs

Question: $question"
    else
        echo "❌ No docs found for $topic"
        ai-ask "$question"
    fi
}
EOF

    echo "✅ Docs-Agent aliases added to .zshrc"
else
    echo "✅ Docs-Agent aliases already in .zshrc"
fi

# Create unified vibe command
cat > "$HOME/.config/vibe-coding/vibe-command.sh" << 'EOF'
#!/usr/bin/env bash
# 🎨 Unified Vibe Command - Access all features

COMMAND="${1:-help}"

case "$COMMAND" in
    start)
        vibe_start
        ;;
    dash|dashboard)
        vibe-dash
        ;;
    music|lofi)
        lofi
        ;;
    docs)
        shift
        cd ~/main/CursorDocsIndex && source venv/bin/activate && python docs_cli.py "$@"
        ;;
    ai)
        shift
        ai-ask "$@"
        ;;
    status)
        echo "🎨 Vibe-Coding Environment Status"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ai_status
        echo ""
        echo "📚 Docs-Agent Status:"
        cd ~/main/CursorDocsIndex && source venv/bin/activate && python docs_cli.py stats
        ;;
    help|*)
        cat << 'HELP'
🎨 Vibe Command - Unified Interface

Usage: vibe <command> [args]

Commands:
  start              Start vibe coding session
  dash, dashboard    Show system dashboard
  music, lofi        Start lo-fi music
  docs <query>       Search documentation
  ai <question>      Ask AI a question
  status             Show complete system status
  help               Show this help

Examples:
  vibe start
  vibe music
  vibe docs search "authentication"
  vibe ai "Explain React hooks"
  vibe status
HELP
        ;;
esac
EOF

chmod +x "$HOME/.config/vibe-coding/vibe-command.sh"

# Add vibe command alias
if ! grep -q "alias vibe=" ~/.zshrc; then
    echo "alias vibe='$HOME/.config/vibe-coding/vibe-command.sh'" >> ~/.zshrc
    echo "✅ 'vibe' command added"
else
    echo "✅ 'vibe' command already exists"
fi

echo ""
echo "✅ Integration complete!"
echo ""
echo "🎨 New Unified Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Quick Docs Access:"
echo "  docs search \"query\"       - Search documentation"
echo "  docs lookup \"topic\"       - Quick lookup"
echo "  docs stats               - Show stats"
echo "  docs ingest \"url\"         - Add documentation"
echo ""
echo "Unified Vibe Command:"
echo "  vibe start               - Start vibe session"
echo "  vibe music               - Play lo-fi"
echo "  vibe docs search \"q\"     - Search docs"
echo "  vibe ai \"question\"       - Ask AI"
echo "  vibe status              - Complete status"
echo ""
echo "AI with Documentation:"
echo "  ai-with-docs \"topic\" \"question\""
echo "  Example: ai-with-docs \"React hooks\" \"How do I use useState?\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔄 Reload shell to use new commands:"
echo "   source ~/.zshrc"
echo ""

