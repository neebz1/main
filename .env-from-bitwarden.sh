#!/bin/bash

# Generate .env file from Bitwarden
# This script creates a .env file with all your API keys from Bitwarden

echo "🔐 Generating .env from Bitwarden..."
echo ""

# Check if BW_SESSION is set
if [ -z "$BW_SESSION" ]; then
    echo "Vault needs to be unlocked first"
    echo "Loading credentials..."
    
    if [ -f "$HOME/Documents/GitHub/main/.bitwarden-oauth" ]; then
        source "$HOME/Documents/GitHub/main/.bitwarden-oauth"
        export BW_SESSION=$(echo "$BW_PASSWORD" | bw unlock --raw 2>&1 | tail -1)
    else
        echo "❌ Credentials file not found"
        echo "Run: ./setup-bitwarden-env.sh"
        exit 1
    fi
fi

# Check if .env exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists"
    echo "Backup? (y/n)"
    read -r BACKUP
    if [ "$BACKUP" = "y" ]; then
        cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
        echo "✅ Backed up to .env.backup.$(date +%Y%m%d_%H%M%S)"
    fi
fi

# Generate .env file
cat > .env << 'ENVEOF'
# ==============================================
# Environment Configuration
# Generated from Bitwarden
# ==============================================

# CRITICAL SECURITY SETTINGS
ENVEOF

# Add SECRET_KEY
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Add Gradio auth
echo "" >> .env
echo "# Gradio Authentication" >> .env
echo "GRADIO_USER=admin" >> .env
echo "GRADIO_PASSWORD=$(openssl rand -base64 24)" >> .env

# Add CORS
echo "" >> .env
echo "# API Configuration" >> .env
echo "ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000" >> .env

# Add AI API Keys from Bitwarden
echo "" >> .env
echo "# AI API Keys (from Bitwarden)" >> .env

# Define key mappings
declare -A KEY_MAP=(
    ["Google API Key"]="GOOGLE_API_KEY"
    ["Together API Key"]="TOGETHER_API_KEY"
    ["OpenRouter API"]="OPENROUTER_API_KEY"
    ["OpenAI API Key"]="OPENAI_API_KEY"
    ["Anthropic API Key"]="ANTHROPIC_API_KEY"
    ["Moonshot API Key"]="MOONSHOT_API_KEY"
    ["Hugging Face Token"]="HF_TOKEN"
)

# Fetch keys from Bitwarden
for key_name in "${!KEY_MAP[@]}"; do
    env_var="${KEY_MAP[$key_name]}"
    key_value=$(bw get password "$key_name" --session "$BW_SESSION" 2>/dev/null)
    
    if [ -n "$key_value" ]; then
        echo "$env_var=$key_value" >> .env
        echo "✅ Added $env_var"
    else
        echo "$env_var=" >> .env
        echo "⚠️  $env_var not found in Bitwarden"
    fi
done

# Secure the file
chmod 600 .env

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ .env file generated!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Generated:"
echo "  • SECRET_KEY (32 bytes random)"
echo "  • GRADIO_PASSWORD (random)"
echo "  • All API keys from Bitwarden"
echo ""
echo "File secured with 600 permissions"
echo ""
echo "To use:"
echo "  source .env"
echo "Or your apps will auto-load it!"

