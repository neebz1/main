#!/bin/bash

# Quick test of Bitwarden setup

echo "🧪 Testing Bitwarden Setup"
echo "=========================="
echo ""

# Test 1: Check scripts exist
echo "1. Checking scripts..."
SCRIPTS=(
    "bw-health-check.sh"
    "bw-add-key.sh"
    ".env-from-bitwarden.sh"
    "setup-bitwarden-env.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "  ✅ $script (executable)"
        else
            echo "  ⚠️  $script (exists but not executable)"
            chmod +x "$script"
            echo "     Fixed: made executable"
        fi
    else
        echo "  ❌ $script (missing)"
    fi
done

echo ""

# Test 2: Check documentation
echo "2. Checking documentation..."
DOCS=(
    "BITWARDEN-QUICK-START.md"
    "BITWARDEN-ENV-SETUP.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        lines=$(wc -l < "$doc")
        echo "  ✅ $doc ($lines lines)"
    else
        echo "  ❌ $doc (missing)"
    fi
done

echo ""

# Test 3: Check Bitwarden CLI
echo "3. Checking Bitwarden CLI..."
if command -v bw &> /dev/null; then
    echo "  ✅ Bitwarden CLI: $(bw --version)"
else
    echo "  ❌ Bitwarden CLI not installed"
fi

echo ""

# Test 4: Check login status
echo "4. Checking Bitwarden login..."
BW_STATUS=$(bw status 2>/dev/null)
if [ $? -eq 0 ]; then
    USER_EMAIL=$(echo "$BW_STATUS" | jq -r '.userEmail' 2>/dev/null)
    VAULT_STATUS=$(echo "$BW_STATUS" | jq -r '.status' 2>/dev/null)
    
    if [ "$USER_EMAIL" != "null" ] && [ -n "$USER_EMAIL" ]; then
        echo "  ✅ Logged in as: $USER_EMAIL"
        echo "  📊 Vault status: $VAULT_STATUS"
    else
        echo "  ⚠️  Not logged in"
    fi
else
    echo "  ❌ Cannot check status"
fi

echo ""

# Test 5: Check credentials file
echo "5. Checking credentials file..."
CREDS_FILE="$HOME/Documents/GitHub/main/.bitwarden-oauth"
if [ -f "$CREDS_FILE" ]; then
    PERMS=$(stat -f "%Lp" "$CREDS_FILE" 2>/dev/null)
    echo "  ✅ Credentials file exists"
    echo "  🔒 Permissions: $PERMS"
    if [ "$PERMS" != "600" ]; then
        echo "  ⚠️  Should be 600 for security"
    fi
else
    echo "  ⚠️  Credentials file not found"
fi

echo ""

# Test 6: Check .zshrc integration
echo "6. Checking .zshrc integration..."
if grep -q "bwload()" "$HOME/.zshrc" 2>/dev/null; then
    echo "  ✅ bwload() function configured"
else
    echo "  ❌ bwload() function not found"
fi

echo ""

# Test 7: Preview .env generation (without actually creating it)
echo "7. Testing .env generation capability..."
if [ -f ".env-from-bitwarden.sh" ]; then
    echo "  ✅ Script exists"
    if [ -x ".env-from-bitwarden.sh" ]; then
        echo "  ✅ Script is executable"
        echo ""
        echo "  To generate .env file, run:"
        echo "    ./.env-from-bitwarden.sh"
    else
        echo "  ⚠️  Script needs to be executable"
        echo "  Run: chmod +x .env-from-bitwarden.sh"
    fi
else
    echo "  ❌ Script not found"
fi

echo ""
echo "=========================="
echo "✅ Setup test complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Run: bwload"
echo "  2. Run: ai_status"
echo "  3. Run: ./.env-from-bitwarden.sh (to create .env)"
echo ""

