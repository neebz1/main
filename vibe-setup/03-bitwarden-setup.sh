#!/usr/bin/env bash
# 🔐 Bitwarden CLI Setup for Secure API Key Management

set -e

echo "🔐 Setting up Bitwarden CLI for API key management..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Bitwarden CLI is installed
if ! command -v bw &> /dev/null; then
    echo "📦 Installing Bitwarden CLI..."
    brew install bitwarden-cli
fi

echo ""
echo "✅ Bitwarden CLI installed"

echo ""
echo "📋 Bitwarden Setup Instructions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Login to Bitwarden:"
echo "   bw login"
echo ""
echo "2️⃣  Unlock vault and set session:"
echo "   export BW_SESSION=\$(bw unlock --raw)"
echo ""
echo "3️⃣  Or use the alias (after sourcing .zshrc):"
echo "   bwload"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 API Keys to Add to Bitwarden"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Create these items in your Bitwarden vault:"
echo ""
echo "• Name: 'OpenRouter API'"
echo "  Type: Login"
echo "  Password: <your-openrouter-api-key>"
echo ""
echo "• Name: 'Hugging Face Token'"
echo "  Type: Login"
echo "  Password: <your-huggingface-token>"
echo ""
echo "• Name: 'OpenAI API Key'"
echo "  Type: Login"
echo "  Password: <your-openai-api-key>"
echo ""
echo "• Name: 'Anthropic API Key'"
echo "  Type: Login"
echo "  Password: <your-anthropic-api-key>"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔧 Quick Commands:"
echo ""
echo "# Add item via CLI:"
echo "bw get template item | jq '.name=\"OpenRouter API\" | .login.password=\"YOUR_KEY\"' | bw encode | bw create item"
echo ""
echo "# Test retrieval:"
echo "bw get password 'OpenRouter API'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create helper script for adding keys
cat > "$HOME/.config/vibe-coding/add-api-key.sh" << 'EOF'
#!/usr/bin/env bash
# Helper script to add API keys to Bitwarden

if [ -z "$BW_SESSION" ]; then
    echo "❌ Please unlock Bitwarden first: export BW_SESSION=$(bw unlock --raw)"
    exit 1
fi

echo "🔐 Add API Key to Bitwarden"
echo ""
read -p "Key name (e.g., OpenRouter API): " key_name
read -sp "API Key value: " api_key
echo ""

# Create item
bw get template item | jq ".name=\"$key_name\" | .login.password=\"$api_key\"" | bw encode | bw create item > /dev/null

echo "✅ API key '$key_name' added successfully!"
EOF

chmod +x "$HOME/.config/vibe-coding/add-api-key.sh"

echo ""
echo "✅ Created helper script: ~/.config/vibe-coding/add-api-key.sh"
echo ""
echo "🚀 Next Steps:"
echo "1. Run: bw login"
echo "2. Run: bwload (to unlock and load keys)"
echo "3. Or use helper: ~/.config/vibe-coding/add-api-key.sh"
echo ""

