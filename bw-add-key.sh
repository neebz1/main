#!/bin/bash

# Helper script to add API keys to Bitwarden
# Usage: ./bw-add-key.sh "Key Name" "api-key-value"

if [ $# -ne 2 ]; then
    echo "Usage: $0 \"Key Name\" \"api-key-value\""
    echo ""
    echo "Examples:"
    echo "  $0 \"Moonshot API Key\" \"sk-xxx...\""
    echo "  $0 \"Google API Key\" \"AIza...\""
    echo "  $0 \"OpenRouter API\" \"sk-or-...\""
    echo "  $0 \"Hugging Face Token\" \"hf_...\""
    echo "  $0 \"OpenAI API Key\" \"sk-...\""
    echo "  $0 \"Anthropic API Key\" \"sk-ant-...\""
    exit 1
fi

KEY_NAME="$1"
KEY_VALUE="$2"

# Check if logged in
if ! bw status | grep -q "userEmail"; then
    echo "❌ Not logged in to Bitwarden"
    echo "   Run: bw login termin.turban818@passinbox.com"
    exit 1
fi

# Check if unlocked
if [ -z "$BW_SESSION" ]; then
    echo "🔓 Unlocking vault..."
    export BW_SESSION=$(bw unlock --raw)
fi

if [ -z "$BW_SESSION" ]; then
    echo "❌ Failed to unlock vault"
    exit 1
fi

# Check if item already exists
if bw get item "$KEY_NAME" --session "$BW_SESSION" &> /dev/null; then
    echo "⚠️  '$KEY_NAME' already exists in Bitwarden"
    echo "   Updating..."
    ITEM_ID=$(bw get item "$KEY_NAME" --session "$BW_SESSION" | jq -r '.id')
    bw get item "$ITEM_ID" --session "$BW_SESSION" | jq ".login.password = \"$KEY_VALUE\"" | bw encode | bw edit item "$ITEM_ID" --session "$BW_SESSION" > /dev/null
    echo "✅ Updated: $KEY_NAME"
else
    echo "📝 Adding: $KEY_NAME"
    echo "{\"organizationId\":null,\"folderId\":null,\"type\":1,\"name\":\"$KEY_NAME\",\"notes\":null,\"favorite\":false,\"login\":{\"username\":\"\",\"password\":\"$KEY_VALUE\",\"totp\":null}}" | bw encode | bw create item --session "$BW_SESSION" > /dev/null
    echo "✅ Added: $KEY_NAME"
fi

# Sync to server
bw sync --session "$BW_SESSION" > /dev/null
echo "🔄 Synced to server"

