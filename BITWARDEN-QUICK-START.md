# 🚀 Bitwarden Quick Start

**Status:** ✅ Already configured and ready to use!

---

## ⚡ 3-Step Quick Start

```bash
# 1. Reload shell
source ~/.zshrc

# 2. Unlock vault and load keys
bwload

# 3. Verify
ai_status
```

**That's it!** Your API keys are now loaded.

---

## 📋 Common Commands

| Command | What It Does |
|---------|--------------|
| `bwload` | Unlock vault & load all API keys |
| `ai_status` | Check which keys are loaded |
| `bw sync` | Sync with Bitwarden cloud |
| `bw lock` | Lock vault (for security) |
| `bw status` | Check vault status |
| `./bw-health-check.sh` | Run health check |

---

## 🔑 Add API Keys

### Method 1: Quick Add
```bash
./bw-add-key.sh "Google API Key" "AIza..."
./bw-add-key.sh "Together API Key" "your-key-here"
```

### Method 2: Web Interface
1. Go to https://vault.bitwarden.com
2. Login with: termin.turban818@passinbox.com
3. Add item → Login type
4. Name: "Google API Key"
5. Password: (paste your API key)
6. Save

---

## 📄 Generate .env File

**From Bitwarden:**
```bash
./.env-from-bitwarden.sh
```

This will:
- Generate unique SECRET_KEY
- Generate random GRADIO_PASSWORD
- Pull all API keys from Bitwarden
- Create .env with 600 permissions

---

## 🔍 Troubleshooting

### "Vault is locked"
```bash
bwload  # This unlocks it
```

### "Not logged in"
```bash
bw login termin.turban818@passinbox.com
```

### "BW_PASSWORD not set"
```bash
source ~/.zshrc
```

### Keys not loading
```bash
# Check vault has items
bw list items --session $BW_SESSION | jq '.[].name'

# Check specific key
bw get item "Google API Key" --session $BW_SESSION
```

---

## 📚 Full Documentation

For complete guide: **`BITWARDEN-ENV-SETUP.md`**

For health check: **`./bw-health-check.sh`**

---

## 🎯 Daily Workflow

**Every new terminal:**
```bash
bwload     # Load keys
ai_status  # Verify
```

**Add new key:**
```bash
./bw-add-key.sh "Service Name" "api-key"
bwload  # Reload
```

**Use in apps:**
```bash
python cloud_ai_builder.py  # Keys auto-loaded
python app.py               # Keys auto-loaded
python live_ai_assistant.py # Keys auto-loaded
```

---

## 🎓 How It Works

1. **Storage**: API keys stored encrypted in Bitwarden vault
2. **Unlock**: `bwload` unlocks vault with your master password
3. **Export**: Keys exported as environment variables
4. **Use**: All Python apps access keys via `os.getenv()`

**Example Flow:**
```bash
# You run
bwload

# Behind the scenes
# 1. Unlocks Bitwarden vault
# 2. export GOOGLE_API_KEY="AIza..."
# 3. export TOGETHER_API_KEY="..."
# etc.

# Your apps use
import os
api_key = os.getenv('GOOGLE_API_KEY')
```

---

## 📊 Your Current Status

Based on health check:

- ✅ Bitwarden CLI installed (v2025.9.0)
- ✅ Logged in as: termin.turban818@passinbox.com
- ✅ Credentials file exists and secure (600 perms)
- ✅ Auto-load configured in .zshrc
- ✅ Helper functions ready
- ⚠️  Vault is locked (normal - just run `bwload`)

---

## 🔐 Security Notes

**Your Setup is Secure:**
- ✅ Credentials file has 600 permissions
- ✅ File is in .gitignore (won't be committed)
- ✅ Master password never stored in plain text
- ✅ Keys encrypted in Bitwarden vault
- ✅ Session tokens are temporary

**Best Practices:**
- Lock vault when done: `bw lock`
- Sync regularly: `bw sync`
- Rotate API keys every 90 days
- Enable 2FA on Bitwarden account

---

## 💡 Pro Tips

1. **Auto-load on startup**: Already configured in .zshrc!
2. **Quick status**: Just run `ai_status`
3. **Generate .env**: Use `./.env-from-bitwarden.sh`
4. **Update key**: Just run `bw-add-key.sh` again with same name
5. **Backup vault**: Run `bw sync` before making changes

---

## 📞 Need Help?

**Quick Checks:**
```bash
./bw-health-check.sh  # Full diagnostic
bw status             # Vault status
ai_status             # Loaded keys
```

**Common Issues:**
- Vault locked → `bwload`
- Not logged in → `bw login termin.turban818@passinbox.com`
- Keys not found → Check names in Bitwarden match exactly

**Documentation:**
- Full guide: `BITWARDEN-ENV-SETUP.md`
- Security audit: `SECURITY-AUDIT-REPORT.md`
- All scripts: `./bw-*.sh`

---

**Current Status:** ✅ Ready to use | ⚠️ Vault locked

**Next Step:** Run `bwload && ai_status` to get started! 🚀

---

*Part of your security-hardened development environment*
create env file for bw

## 🔧 Creating Environment Files from Bitwarden

### For Development
