#!/bin/bash

echo "🔐 Setting up API keys in Bitwarden"
echo "===================================="
echo ""

# Check if logged in
if ! bw status | grep -q "userEmail"; then
    echo "❌ Not logged in to Bitwarden"
    echo "Run: bw login"
    exit 1
fi

# Unlock vault
echo "🔓 Unlocking Bitwarden vault..."
export BW_SESSION=$(bw unlock --raw)

if [ -z "$BW_SESSION" ]; then
    echo "❌ Failed to unlock vault"
    exit 1
fi

echo "✅ Vault unlocked"
echo ""

# Add Moonshot API Key
echo "📝 Enter your Moonshot API key:"
read -r MOONSHOT_KEY

if [ -n "$MOONSHOT_KEY" ]; then
    # Check if item exists
    if bw get item "Moonshot API Key" &> /dev/null; then
        echo "⚠️  Moonshot API Key already exists in Bitwarden"
        echo "   Use the Bitwarden app to update it manually"
    else
        echo "{\"organizationId\":null,\"folderId\":null,\"type\":1,\"name\":\"Moonshot API Key\",\"notes\":null,\"favorite\":false,\"login\":{\"username\":\"\",\"password\":\"$MOONSHOT_KEY\",\"totp\":null}}" | bw encode | bw create item > /dev/null
        echo "✅ Moonshot API key added to Bitwarden"
    fi
fi

echo ""

# Add Google API Key  
echo "📝 Enter your Google API key:"
read -r GOOGLE_KEY

if [ -n "$GOOGLE_KEY" ]; then
    # Check if item exists
    if bw get item "Google API Key" &> /dev/null; then
        echo "⚠️  Google API Key already exists in Bitwarden"
        echo "   Use the Bitwarden app to update it manually"
    else
        echo "{\"organizationId\":null,\"folderId\":null,\"type\":1,\"name\":\"Google API Key\",\"notes\":null,\"favorite\":false,\"login\":{\"username\":\"\",\"password\":\"$GOOGLE_KEY\",\"totp\":null}}" | bw encode | bw create item > /dev/null
        echo "✅ Google API key added to Bitwarden"
    fi
fi

echo ""
echo "🎉 Done! Now run: bwload"
echo "   This will load your API keys into the shell"
echo ""
echo "   Then reload VS Code for Cline to pick them up"

