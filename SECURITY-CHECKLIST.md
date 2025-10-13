# 🔒 Security Checklist - Quick Reference Card

**Print this and check off as you fix each item!**

---

## 🚨 CRITICAL - Fix Before Production

- [ ] **1. Fix CORS in API** (2 minutes)
  - File: `api/main.py` line 33
  - Change: `allow_origins=["*"]` → `allow_origins=["http://localhost:3000"]`
  - Production: Set `ALLOWED_ORIGINS` in .env

- [ ] **2. SECRET_KEY Already Set** ✅
  - Verified: Your .env has a custom SECRET_KEY
  - Store in Bitwarden for production

- [ ] **3. Install Rate Limiting** (10 minutes)
  - Run: `pip install slowapi`
  - Add to `api/main.py` (see implementation guide)

- [ ] **4. Fix Command Injection** (15 minutes)
  - File: `cloud_ai_builder.py`
  - Replace `execute_command()` with whitelist version
  - See: `SECURITY-FIXES-IMPLEMENTATION-GUIDE.md` section 4

---

## ⚠️ HIGH PRIORITY - This Week

- [ ] **5. Add Gradio Authentication**
  - Files: `cloud_ai_builder.py`, `app.py`, others with Gradio
  - Add: `auth=(os.getenv("GRADIO_USER"), os.getenv("GRADIO_PASSWORD"))`
  - Set `GRADIO_PASSWORD` in .env

- [ ] **6. Add Admin RBAC**
  - Update `api/models.py` - add role field
  - Update `api/main.py` - protect admin endpoints
  - See: `SECURITY-FIXES-IMPLEMENTATION-GUIDE.md` section 5

- [ ] **7. Add Security Logging**
  - Use: `setup_security_logger()` from `api/security_fixes.py`
  - Log failed logins, admin access
  - See: Implementation guide section 10

---

## 📋 MEDIUM - This Month

- [ ] **8. Implement Refresh Tokens**
  - Update `api/auth.py`
  - See: Implementation guide section 9

- [ ] **9. Add Git Operation Guards**
  - Check for secrets before commit
  - See: `SECURITY-AUDIT-REPORT.md` issue #12

- [ ] **10. Install Dependency Scanner**
  - Run: `pip install safety pip-audit`
  - Run monthly: `safety check`

---

## ℹ️ LOW - Best Practices

- [ ] **11. Set up Pre-commit Hooks**
  - Scan for secrets before commit
  - Install pre-commit framework

- [ ] **12. Configure Database Backups**
  - Use backup function from `api/database.py`

- [ ] **13. Remove Hardcoded Paths**
  - Use `PROJECT_ROOT` environment variable

---

## ✅ Already Secure (Nice Work!)

- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ Input validation (Pydantic)
- ✅ Secrets in Bitwarden
- ✅ .env excluded from git
- ✅ No hardcoded API keys
- ✅ Docker health checks
- ✅ Rate limiting library detected

---

## 🧪 Test Your Fixes

After each fix, run:
```bash
./security-check.sh
```

**Current Status:**
- ✓ Passed: 6
- ⚠ Warnings: 4
- ✗ Critical: 1 (CORS)

**Target:**
- ✓ Passed: 8+
- ⚠ Warnings: 2 or less
- ✗ Critical: 0

---

## 📦 Quick Commands

### Generate Secrets
```bash
# SECRET_KEY
openssl rand -hex 32

# Password
openssl rand -base64 24
```

### Install Security Tools
```bash
pip install slowapi safety pip-audit
```

### Run Security Scan
```bash
./security-check.sh
```

### Check Dependencies
```bash
safety check
pip-audit
```

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] All CRITICAL issues fixed
- [ ] All HIGH priority issues addressed
- [ ] `./security-check.sh` shows 0 critical
- [ ] .env.production created with unique values
- [ ] HTTPS certificate configured
- [ ] Database migrated to PostgreSQL
- [ ] Monitoring/logging enabled
- [ ] Backups configured

---

## 📞 Quick Help

**Problem** → **Solution**

CORS error → Fix `api/main.py:33`
Failed login brute force → Add rate limiting
Gradio public access → Add authentication
Command injection risk → Use command whitelist

---

## 🎯 Time Estimates

| Task | Time | Impact |
|------|------|--------|
| Fix CORS | 2 min | CRITICAL |
| Add rate limiting | 10 min | CRITICAL |
| Fix command injection | 15 min | CRITICAL |
| Add Gradio auth | 10 min | HIGH |
| Add admin RBAC | 30 min | HIGH |
| Security logging | 20 min | HIGH |
| **TOTAL for Critical+High** | **~90 min** | **Production Ready** |

---

**Print this checklist and mark off items as you complete them!**

*Last updated: October 13, 2025*

