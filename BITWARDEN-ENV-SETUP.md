# 🔐 Bitwarden Environment Setup Guide

Complete guide to accessing your API keys from Bitwarden

---

## ✅ Current Status

You already have:
- ✅ Bitwarden CLI installed (v2025.9.0)
- ✅ `()` function configured in .zshrc
- ✅ Auto-load configured in .zshrc
- ✅ Helper scripts ready

---

## 🚀 Quick Start (3 Steps)

### Step 1: Health Check
```bash
./bw-health-check.sh
```

This will:
- Check if Bitwarden is properly configured
- Auto-fix common issues
- Show you what needs attention

### Step 2: Unlock & Load Keys
```bash
source ~/.zshrc  # Reload zsh config
bwload           # Unlock vault and load API keys
```

### Step 3: Verify Keys Loaded
```bash
ai_status        # Check which API keys are loaded
```

---

## 📝 Step-by-Step Setup

### 1. Check Bitwarden Status

```bash
bw status
```

**Expected output:**
```json
{
  "serverUrl": "https://vault.bitwarden.com",
  "lastSync": "...",
  "userEmail": "your-email@example.com",
  "userId": "...",
  "status": "unlocked"  # or "locked"
}
```

---

### 2. Login to Bitwarden (if not logged in)

```bash
# Your email is: termin.turban818@passinbox.com (from bw-add-key.sh)
bw login termin.turban818@passinbox.com
```

**Enter your master password when prompted.**

---

### 3. Create Credentials File (if not exists)

```bash
# Create the file
cat > ~/Documents/GitHub/main/.bitwarden-oauth << 'EOF'
# Bitwarden OAuth Credentials
# NEVER commit this file to git!
BW_EMAIL="termin.turban818@passinbox.com"
BW_PASSWORD="your-master-password-here"
EOF

# Secure the file
chmod 600 ~/Documents/GitHub/main/.bitwarden-oauth
```

**Important:** Replace `your-master-password-here` with your actual Bitwarden master password.

---

### 4. Reload Shell Configuration

```bash
source ~/.zshrc
```

This loads:
- The `.bitwarden-oauth` credentials
- The `bwload()` function
- Helper functions like `ai_status`

---

### 5. Load Your API Keys

```bash
bwload
```

**What this does:**
1. Unlocks your Bitwarden vault
2. Fetches all stored API keys
3. Exports them as environment variables:
   - `GOOGLE_API_KEY`
   - `TOGETHER_API_KEY`
   - `OPENROUTER_API_KEY`
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - etc.

---

## 🔑 Adding API Keys to Bitwarden

### Method 1: Using Helper Script (Recommended)

```bash
# Add Google API Key
./bw-add-key.sh "Google API Key" "AIza..."

# Add Together AI Key
./bw-add-key.sh "Together API Key" "your-key-here"

# Add OpenRouter Key
./bw-add-key.sh "OpenRouter API" "sk-or-..."

# Add Anthropic Key
./bw-add-key.sh "Anthropic API Key" "sk-ant-..."

# Add OpenAI Key
./bw-add-key.sh "OpenAI API Key" "sk-..."
```

### Method 2: Manual Entry

```bash
# Interactive mode
./setup-api-keys.sh
```

This will prompt you for each key.

### Method 3: Bitwarden Web Interface

1. Go to https://vault.bitwarden.com
2. Login with your credentials
3. Add new items as "Login" type
4. Name them exactly:
   - "Google API Key"
   - "Together API Key"
   - "OpenRouter API"
   - etc.
5. Put the API key in the "Password" field
6. Save

---

## 📋 Understanding the `bwload()` Function

Your `.zshrc` has this function configured. Here's what it does:

```bash
bwload() {
    # Check if password is set
    if [ -z "$BW_PASSWORD" ]; then
        echo "❌ BW_PASSWORD not set"
        return 1
    fi

    # Unlock vault
    export BW_SESSION=$(echo "$BW_PASSWORD" | bw unlock --raw)

    # Fetch and export API keys
    # Searches for items named "Google API Key", "OpenAI API Key", etc.
    # Exports them as GOOGLE_API_KEY, OPENAI_API_KEY, etc.

    # Example:
    # GOOGLE_API_KEY=$(bw get password "Google API Key" --session $BW_SESSION)
    # export GOOGLE_API_KEY
}
```

---

## 🔍 Checking What's Loaded

### View All Environment Variables
```bash
env | grep -E "(API_KEY|TOKEN|SECRET)" | sort
```

### Use the `ai_status` Helper
```bash
ai_status
```

**Output:**
```
🤖 AI API Keys Status
━━━━━━━━━━━━━━━━━━━━
✅ GOOGLE_API_KEY: AIza***...
✅ TOGETHER_API_KEY: ***...
✅ OPENROUTER_API_KEY: sk-or-***...
❌ OPENAI_API_KEY: Not set
❌ ANTHROPIC_API_KEY: Not set
```

---

## 🛠️ Troubleshooting

### Problem: "Not logged in to Bitwarden"

**Solution:**
```bash
bw login termin.turban818@passinbox.com
# Enter your master password
```

### Problem: "Vault is locked"

**Solution:**
```bash
bwload  # This unlocks and loads keys
```

### Problem: "BW_PASSWORD not set"

**Solution:**
```bash
# Make sure .bitwarden-oauth exists and is loaded
ls -la ~/Documents/GitHub/main/.bitwarden-oauth

# Reload it
source ~/Documents/GitHub/main/.bitwarden-oauth
source ~/.zshrc
```

### Problem: "API keys not found"

**Solution:**
```bash
# List all items in vault
bw list items --session $BW_SESSION | jq '.[].name'

# Check exact name
bw get item "Google API Key" --session $BW_SESSION
```

**Names must match exactly!**

---

## 🔄 Workflow

### Every Time You Open a New Terminal:

```bash
# Option 1: Auto-load (if configured in .zshrc)
# Just open terminal - keys load automatically

# Option 2: Manual load
bwload

# Verify
ai_status
```

### When Adding a New Key:

```bash
# Add to Bitwarden
./bw-add-key.sh "Service Name" "api-key-value"

# Reload keys
bwload

# Verify
ai_status
```

### When Using Keys in Your Apps:

Keys are available as environment variables:
```bash
python cloud_ai_builder.py  # Uses TOGETHER_API_KEY automatically
python live_ai_assistant.py # Uses GOOGLE_API_KEY automatically
python app.py               # Uses TOGETHER_API_KEY automatically
```

---

## 🔐 Security Best Practices

### ✅ DO:
- Keep `.bitwarden-oauth` with 600 permissions
- Use a strong Bitwarden master password
- Enable 2FA on Bitwarden account
- Sync regularly: `bw sync`
- Rotate API keys every 90 days

### ❌ DON'T:
- Commit `.bitwarden-oauth` to git (it's in .gitignore)
- Share your BW_SESSION token
- Store API keys in plain text files
- Use the same password for everything

---

## 📊 Integration with .env Files

For applications that need `.env` files, you can generate them:

```bash
# Create .env from Bitwarden
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
GOOGLE_API_KEY=$(bw get password "Google API Key" --session $BW_SESSION)
TOGETHER_API_KEY=$(bw get password "Together API Key" --session $BW_SESSION)
OPENROUTER_API_KEY=$(bw get password "OpenRouter API" --session $BW_SESSION)
GRADIO_PASSWORD=$(openssl rand -base64 24)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
EOF

# Secure it
chmod 600 .env
```

---

## 🎯 Common Use Cases

### 1. Load Keys for Development Session
```bash
# Morning routine
source ~/.zshrc
bwload
ai_status
```

### 2. Add New API Key
```bash
# Get your new API key from service
# Then:
./bw-add-key.sh "New Service API" "key-value-here"
bwload
```

### 3. Update Existing Key
```bash
# Keys rotate? Update in Bitwarden
./bw-add-key.sh "Google API Key" "new-key-value"
bwload
```

### 4. Share Environment with VS Code/Cursor
```bash
# Load keys
bwload

# Open VS Code/Cursor from same terminal
code .
# or
cursor .
```

The environment variables will be available in the editor!

---

## 🧪 Testing Your Setup

### Test 1: Basic Health Check
```bash
./bw-health-check.sh
```

**Expected:** All checks pass or only warnings

### Test 2: Load and Verify
```bash
bwload
echo $GOOGLE_API_KEY | head -c 20
```

**Expected:** Shows first 20 chars of your key

### Test 3: Run an App
```bash
python app.py
```

**Expected:** App starts without API key errors

---

## 📚 Helper Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `bw-health-check.sh` | Check Bitwarden setup | `./bw-health-check.sh` |
| `bw-add-key.sh` | Add/update API key | `./bw-add-key.sh "Name" "key"` |
| `setup-api-keys.sh` | Interactive key setup | `./setup-api-keys.sh` |
| `bw-test.sh` | Test Bitwarden access | `./bw-test.sh` |
| `bwload` | Load all keys | `bwload` (zsh function) |
| `ai_status` | Check loaded keys | `ai_status` (zsh function) |

---

## 🚀 Quick Reference Card

```bash
# Check status
bw status
ai_status
./bw-health-check.sh

# Login
bw login termin.turban818@passinbox.com

# Load keys
bwload

# Add key
./bw-add-key.sh "Service Name" "api-key-value"

# Sync
bw sync

# Logout (when done)
bw lock
```

---

## ❓ FAQ

**Q: Do I need to run `bwload` every time?**
A: If configured for auto-load in .zshrc, it runs automatically. Otherwise, yes.

**Q: How often should I sync?**
A: Run `bw sync` after adding/updating keys, or weekly.

**Q: What if I forget my master password?**
A: Bitwarden cannot recover it. Keep it safe!

**Q: Can I use this in scripts?**
A: Yes! Just ensure `bwload` runs first, or source it in the script.

**Q: Are my keys safe?**
A: Yes! They're encrypted by Bitwarden and never stored in plain text.

---

## 🎉 You're All Set!

Run this now:
```bash
./bw-health-check.sh && bwload && ai_status
```

**Next:** Start using your apps with secure API keys! 🚀

---

*For more help, check: `bw --help` or visit https://bitwarden.com/help/*

