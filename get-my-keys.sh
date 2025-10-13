#!/bin/bash
# Quick script to get your API keys from Bitwarden

echo "🔐 Getting your API keys from Bitwarden..."
echo ""

# Load Bitwarden
source ~/.zshrc
bwload

echo ""
echo "📋 Your API Keys:"
echo "==============================================="
echo ""
echo "MOONSHOT KEY:"
echo "$MOONSHOT_API_KEY"
echo ""
echo "GOOGLE KEY:"
echo "$GOOGLE_API_KEY"
echo ""
echo "==============================================="
echo ""
echo "✅ Copy these keys and paste them into:"
echo "   /Users/nr/Documents/GitHub/main/.vscode/settings.json"
echo ""
echo "Replace:"
echo "  - PASTE_YOUR_MOONSHOT_KEY_HERE"
echo "  - PASTE_YOUR_GOOGLE_KEY_HERE"


