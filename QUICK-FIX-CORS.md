# 🔴 CRITICAL: Fix CORS Now!

**Time Required:** 2 minutes
**Impact:** Prevents CSRF and unauthorized API access

---

## What's Wrong?

Your API currently accepts requests from **ANY website** (`allow_origins=["*"]`).

This means:
- ❌ Any malicious website can call your API
- ❌ Steal user data via CSRF attacks
- ❌ Make unauthorized requests on behalf of users

---

## Fix It Now

### Option 1: Quick Fix (Development)

**File:** `api/main.py` line 33

**Change this:**
```python
allow_origins=["*"],  # ⚠️ DANGEROUS
```

**To this:**
```python
allow_origins=["http://localhost:3000", "http://localhost:8000"],  # ✅ SAFE
```

### Option 2: Proper Fix (Production Ready)

**Step 1:** Update `api/main.py`:

```python
import os

# Load allowed origins from environment
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ Use environment variable
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**Step 2:** Add to `.env`:

```bash
# Development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Production (update when deploying)
# ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

---

## Verify the Fix

1. **Restart your API:**
   ```bash
   cd /Users/nr/Documents/GitHub/main
   python -m uvicorn api.main:app --reload
   ```

2. **Run security check:**
   ```bash
   ./security-check.sh
   ```

3. **Look for:**
   ```
   ✓ CORS configuration appears safe
   ```

---

## Test It Works

**Test 1: Allowed origin (should work)**
```bash
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://localhost:8000/items
```
Expected: `access-control-allow-origin: http://localhost:3000`

**Test 2: Blocked origin (should fail)**
```bash
curl -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://localhost:8000/items
```
Expected: No `access-control-allow-origin` header

---

## For Production

When deploying, update `.env.production`:

```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
```

**Never use `["*"]` in production!**

---

## That's It!

This 2-minute fix prevents:
- ✅ Cross-Site Request Forgery (CSRF)
- ✅ Unauthorized API access
- ✅ Data theft from other websites

**Status:** 🔴 CRITICAL → ✅ FIXED

---

*Part of Security Audit - October 13, 2025*

