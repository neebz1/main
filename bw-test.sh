#!/bin/bash

echo "🧪 Testing Bitwarden Configuration"
echo "===================================="
echo ""

# Load OAuth credentials
if [ -f "$HOME/Documents/GitHub/main/.bitwarden-oauth" ]; then
    source "$HOME/Documents/GitHub/main/.bitwarden-oauth"
    echo "✅ OAuth credentials: Loaded"
    echo "   Client ID: ${BW_CLIENT_ID:0:40}..."
else
    echo "❌ OAuth credentials not found"
fi

echo ""

# Check Bitwarden CLI
if ! command -v bw &> /dev/null; then
    echo "❌ Bitwarden CLI not installed"
    echo "   Install with: brew install bitwarden-cli"
    exit 1
else
    echo "✅ Bitwarden CLI: Installed"
fi

echo ""

# Check status
BW_STATUS=$(bw status 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "📊 Bitwarden Status:"
    echo "$BW_STATUS" | jq .

    STATUS_TYPE=$(echo "$BW_STATUS" | jq -r '.status')
    USER_EMAIL=$(echo "$BW_STATUS" | jq -r '.userEmail')

    echo ""
    if [ "$USER_EMAIL" != "null" ] && [ -n "$USER_EMAIL" ]; then
        echo "✅ Logged in as: $USER_EMAIL"
    else
        echo "❌ Not logged in"
        echo "   Run: bw login"
    fi

    echo ""
    if [ "$STATUS_TYPE" = "locked" ]; then
        echo "🔒 Vault is locked"
        echo "   Run: bwload (to unlock and load API keys)"
    elif [ "$STATUS_TYPE" = "unlocked" ]; then
        echo "✅ Vault is unlocked"
    fi
else
    echo "❌ Failed to check Bitwarden status"
    exit 1
fi

echo ""
echo "🎯 Quick Commands:"
echo "   bwload        - Unlock vault and load all API keys"
echo "   ai_status     - Check which API keys are loaded"
echo "   bw sync       - Sync vault with server"
echo "   bw lock       - Lock vault"

