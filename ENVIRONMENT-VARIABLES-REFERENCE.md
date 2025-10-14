# 🔐 Environment Variables Quick Reference

**Quick lookup for all environment variables used in this project**

---

## 🚨 Critical Security Variables (Required)

| Variable | Purpose | How to Generate | Example |
|----------|---------|-----------------|---------|
| `SECRET_KEY` | JWT token signing | `openssl rand -hex 32` | `a1b2c3d4...` (64 chars) |
| `GRADIO_USER` | Gradio auth username | Manual | `admin` |
| `GRADIO_PASSWORD` | Gradio auth password | `openssl rand -base64 24` | `xY7zQ2...` |

---

## 🌐 API Configuration

| Variable | Purpose | Default | Production Example |
|----------|---------|---------|-------------------|
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:8000` | `https://yourdomain.com` |
| `ENVIRONMENT` | Deployment mode | `development` | `production` |
| `PORT` | Server port | `8000` | `8000` |

---

## 🤖 AI Provider API Keys

### OpenAI
```bash
OPENAI_API_KEY=sk-...
```
- Get key: https://platform.openai.com/api-keys
- Models: GPT-4, GPT-3.5-turbo, DALL-E

### Anthropic (Claude)
```bash
ANTHROPIC_API_KEY=sk-ant-...
```
- Get key: https://console.anthropic.com/
- Models: Claude 3 Opus, Sonnet, Haiku

### Google AI (Gemini)
```bash
GOOGLE_API_KEY=AIza...
```
- Get key: https://makersuite.google.com/app/apikey
- Models: Gemini Pro, Gemini Ultra

### Together AI
```bash
TOGETHER_API_KEY=...
```
- Get key: https://api.together.xyz/settings/api-keys
- Models: Llama 2, Mistral, Kimi K2

### OpenRouter
```bash
OPENROUTER_API_KEY=sk-or-...
```
- Get key: https://openrouter.ai/keys
- Access to 100+ models

### Moonshot AI
```bash
MOONSHOT_API_KEY=sk-...
```
- Get key: https://platform.moonshot.cn/
- Models: Moonshot-v1

### Hugging Face
```bash
HF_TOKEN=hf_...
```
- Get key: https://huggingface.co/settings/tokens
- For model downloads and API access

---

## 🗄️ Database Configuration

### Development (SQLite - Default)
```bash
# No configuration needed - uses local file
```

### Production (PostgreSQL)
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Example:
```bash
DATABASE_URL=postgresql://myuser:mypass@localhost:5432/myapp
```

---

## 🚀 Deployment Platforms

### Railway
```bash
RAILWAY_TOKEN=...
```
- Get from: Railway dashboard

### Heroku
```bash
HEROKU_API_KEY=...
```
- Get from: Account settings → API Key

### Vercel
```bash
VERCEL_TOKEN=...
```
- Get from: Account settings → Tokens

---

## 🔧 GitHub Codespaces (Auto-set)

These are automatically configured in Codespaces:

| Variable | Purpose | Example |
|----------|---------|---------|
| `CODESPACES` | Indicates Codespace | `true` |
| `CODESPACE_NAME` | Codespace identifier | `fuzzy-space-disco` |
| `GITHUB_TOKEN` | Auto auth token | `ghu_...` |
| `GITHUB_USER` | Your username | `yourusername` |
| `GIT_ASKPASS` | Git credential helper | `/vscode/...` |

---

## 🎨 VSCode Integration (Auto-set)

These are set by VSCode for Git integration:

| Variable | Purpose |
|----------|---------|
| `VSCODE_GIT_ASKPASS_NODE` | Node path for Git auth |
| `VSCODE_GIT_ASKPASS_MAIN` | Git auth script |
| `GIT_EDITOR` | Default editor for Git |
| `VSCODE_CWD` | Current working directory |

---

## 📝 Optional Configuration

### Monitoring
```bash
SENTRY_DSN=https://...@sentry.io/...
```

### Analytics
```bash
ANALYTICS_KEY=...
```

### Email (for notifications)
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 🔍 Checking Your Environment

### Quick Check Script
```bash
#!/bin/bash
# Save as check-env.sh

echo "🔍 Environment Variables Check"
echo "================================"

# Check critical variables
for var in SECRET_KEY GRADIO_PASSWORD ALLOWED_ORIGINS; do
    if [ -n "${!var}" ]; then
        echo "✅ $var is set"
    else
        echo "❌ $var is NOT set"
    fi
done

# Check AI API keys
echo ""
echo "🤖 AI API Keys:"
for var in OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY TOGETHER_API_KEY; do
    if [ -n "${!var}" ]; then
        echo "✅ $var is set"
    else
        echo "⚠️  $var is NOT set"
    fi
done
```

### Python Check
```python
import os
from dotenv import load_dotenv

load_dotenv()

critical_vars = ["SECRET_KEY", "GRADIO_PASSWORD", "ALLOWED_ORIGINS"]
ai_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]

print("🔍 Environment Variables Check")
print("=" * 40)

for var in critical_vars:
    value = os.getenv(var)
    status = "✅" if value else "❌"
    print(f"{status} {var}: {'Set' if value else 'NOT SET'}")

print("\n🤖 AI API Keys:")
for var in ai_keys:
    value = os.getenv(var)
    status = "✅" if value else "⚠️"
    print(f"{status} {var}: {'Set' if value else 'NOT SET'}")
```

---

## 🔐 Security Checklist

- [ ] `.env` file exists and is not committed to Git
- [ ] `SECRET_KEY` is unique (not default value)
- [ ] `GRADIO_PASSWORD` is strong and secure
- [ ] `ALLOWED_ORIGINS` is set to specific domains (not `*`)
- [ ] File permissions: `chmod 600 .env`
- [ ] API keys are stored securely (e.g., Bitwarden)
- [ ] Different keys used for dev/staging/production
- [ ] Regular key rotation schedule established

---

## 📋 Environment File Template

Copy this to create your `.env` file:

```bash
# ==============================================
# Environment Configuration
# ==============================================

# ========== CRITICAL SECURITY ==========
SECRET_KEY=                          # Generate: openssl rand -hex 32
GRADIO_USER=admin
GRADIO_PASSWORD=                     # Generate: openssl rand -base64 24

# ========== API CONFIGURATION ==========
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ENVIRONMENT=development

# ========== AI API KEYS ==========
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
TOGETHER_API_KEY=
OPENROUTER_API_KEY=
MOONSHOT_API_KEY=
HF_TOKEN=

# ========== DATABASE (Optional) ==========
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# ========== DEPLOYMENT (Optional) ==========
# RAILWAY_TOKEN=
# HEROKU_API_KEY=
# VERCEL_TOKEN=
```

---

## 🚀 Quick Setup Commands

### Generate All Keys at Once
```bash
#!/bin/bash
# Save as generate-keys.sh

echo "# Generated Keys - $(date)" > .env.generated
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env.generated
echo "GRADIO_PASSWORD=$(openssl rand -base64 24)" >> .env.generated
echo "" >> .env.generated
echo "✅ Keys generated in .env.generated"
echo "Copy these to your .env file"
```

### Load from Bitwarden
```bash
# Use the provided script
./.env-from-bitwarden.sh
```

### Validate Environment
```bash
# Run security check
./security-check.sh
```

---

## ❓ Common Issues

### "Environment variable not found"
```bash
# Check if .env exists
ls -la .env

# Check if loaded
echo $SECRET_KEY

# Load manually
export $(cat .env | grep -v '^#' | xargs)
```

### "Invalid SECRET_KEY length"
```bash
# Regenerate with correct length
openssl rand -hex 32
```

### "CORS error in browser"
```bash
# Check ALLOWED_ORIGINS includes your domain
echo $ALLOWED_ORIGINS

# Update in .env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## 📚 Related Documentation

- Full setup guide: `ENVIRONMENT-CONFIGURATION-GUIDE.md`
- Security guide: `SECURITY-FIXES-IMPLEMENTATION-GUIDE.md`
- API documentation: `API-README.md`
- Start here: `START-HERE.md`

---

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete reference available  
**Maintainer:** Project team

---

*Keep this file updated when adding new environment variables. Always document the purpose and how to obtain values.*
