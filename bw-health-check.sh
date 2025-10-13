#!/bin/bash

# Bitwarden Health Check & Auto-Heal
# Run this to verify and fix your Bitwarden setup

echo "🏥 Bitwarden Health Check"
echo "=========================="
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Bitwarden CLI installed
if ! command -v bw &> /dev/null; then
    echo "❌ Bitwarden CLI not installed"
    echo "   Fix: brew install bitwarden-cli"
    ((ERRORS++))
else
    echo "✅ Bitwarden CLI installed"
fi

# Check 2: Credentials file exists
if [ ! -f "$HOME/Documents/GitHub/main/.bitwarden-oauth" ]; then
    echo "❌ Credentials file missing"
    echo "   Expected: $HOME/Documents/GitHub/main/.bitwarden-oauth"
    ((ERRORS++))
else
    echo "✅ Credentials file exists"

    # Check 3: Credentials are loaded
    source "$HOME/Documents/GitHub/main/.bitwarden-oauth"
    if [ -z "$BW_EMAIL" ] || [ -z "$BW_PASSWORD" ]; then
        echo "❌ Credentials not properly set in file"
        ((ERRORS++))
    else
        echo "✅ Credentials loaded (email: $BW_EMAIL)"
    fi
fi

# Check 4: Login status
BW_STATUS=$(bw status 2>/dev/null)
if [ $? -eq 0 ]; then
    STATUS_TYPE=$(echo "$BW_STATUS" | jq -r '.status')
    USER_EMAIL=$(echo "$BW_STATUS" | jq -r '.userEmail')

    if [ "$USER_EMAIL" = "null" ] || [ -z "$USER_EMAIL" ]; then
        echo "⚠️  Not logged in to Bitwarden"
        ((WARNINGS++))

        # Auto-fix: Try to log in
        if [ -n "$BW_EMAIL" ] && [ -n "$BW_PASSWORD" ]; then
            echo "   🔧 Attempting auto-login..."
            echo "$BW_PASSWORD" | bw login "$BW_EMAIL" --raw > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "   ✅ Auto-login successful!"
            else
                echo "   ❌ Auto-login failed"
                ((ERRORS++))
            fi
        fi
    else
        echo "✅ Logged in as: $USER_EMAIL"

        # Check vault status
        if [ "$STATUS_TYPE" = "locked" ]; then
            echo "⚠️  Vault is locked"
            ((WARNINGS++))
        elif [ "$STATUS_TYPE" = "unlocked" ]; then
            echo "✅ Vault is unlocked"
        fi
    fi
else
    echo "❌ Failed to check Bitwarden status"
    ((ERRORS++))
fi

# Check 5: .zshrc integration
if grep -q "bwload()" "$HOME/.zshrc" 2>/dev/null; then
    echo "✅ bwload() function configured in .zshrc"
else
    echo "❌ bwload() function not found in .zshrc"
    ((ERRORS++))
fi

# Check 6: Auto-load on startup
if grep -q ".bitwarden-oauth" "$HOME/.zshrc" 2>/dev/null; then
    echo "✅ Auto-load credentials configured"
else
    echo "⚠️  Auto-load not configured (credentials won't auto-load)"
    ((WARNINGS++))
fi

# Check 7: Vault has items
if [ -n "$BW_SESSION" ] || [ "$STATUS_TYPE" = "unlocked" ]; then
    # Try to get session if not already unlocked
    if [ -z "$BW_SESSION" ]; then
        export BW_SESSION=$(echo "$BW_PASSWORD" | bw unlock --raw 2>&1 | tail -1)
    fi

    ITEM_COUNT=$(bw list items --session "$BW_SESSION" 2>/dev/null | jq length 2>/dev/null)
    if [ -n "$ITEM_COUNT" ] && [ "$ITEM_COUNT" -gt 0 ]; then
        echo "✅ Vault has $ITEM_COUNT item(s)"
    else
        echo "⚠️  Vault is empty (no API keys stored yet)"
        ((WARNINGS++))
    fi
fi

# Check 8: Git ignore protection
if [ -f "$HOME/Documents/GitHub/main/.gitignore" ]; then
    if grep -q ".bitwarden-oauth" "$HOME/Documents/GitHub/main/.gitignore"; then
        echo "✅ Credentials protected in .gitignore"
    else
        echo "⚠️  Credentials not in .gitignore (security risk!)"
        ((WARNINGS++))
    fi
fi

# Check 9: File permissions
if [ -f "$HOME/Documents/GitHub/main/.bitwarden-oauth" ]; then
    PERMS=$(stat -f "%Lp" "$HOME/Documents/GitHub/main/.bitwarden-oauth" 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        echo "✅ Credentials file has secure permissions (600)"
    else
        echo "⚠️  Insecure file permissions ($PERMS), should be 600"
        echo "   🔧 Fixing..."
        chmod 600 "$HOME/Documents/GitHub/main/.bitwarden-oauth"
        echo "   ✅ Fixed!"
    fi
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "🎉 Perfect! All checks passed!"
elif [ $ERRORS -eq 0 ]; then
    echo "✅ Healthy (with $WARNINGS warning(s))"
else
    echo "⚠️  Found $ERRORS error(s) and $WARNINGS warning(s)"
    echo ""
    echo "Run 'bwload' to load your API keys"
fi

echo ""
echo "💡 Quick commands:"
echo "   bwload        - Unlock and load API keys"
echo "   ai_status     - Check loaded keys"
echo "   bw sync       - Sync with server"

