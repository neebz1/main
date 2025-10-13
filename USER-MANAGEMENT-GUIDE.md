# 👥 User Management & DevOps Access Guide

## 🎯 Quick Answer

**Can DevOps create accounts?** Yes! ✅
**Can they use your Bitwarden credentials?** No! ❌

**Bitwarden credentials are for:**
- YOUR API keys (Google, OpenAI, etc.)
- YOUR personal secrets
- NOT for creating user accounts

**User accounts are created via:**
- The REST API registration endpoint
- Each user has their own username/password
- Separate from Bitwarden

---

## 🔐 Two Different Systems

### 1. Bitwarden (API Key Management) 🔑
**Purpose:** Store and manage API keys securely
**Your Setup:**
- Email: termin.turban818@passinbox.com
- Stores: GOOGLE_API_KEY, TOGETHER_API_KEY, etc.
- Access: Only YOU via `bwload`
- **NOT for user authentication!**

### 2. REST API User System (User Accounts) 👤
**Purpose:** Multi-user access to your API/apps
**How it works:**
- Users register via `/auth/register`
- Each gets their own username/password
- Login returns JWT token
- Use token to access protected endpoints

**These are separate systems!**

---

## ✅ How DevOps Can Create Accounts

### Option 1: Self-Registration (Recommended)

**Start the API:**
```bash
cd /Users/nr/Documents/GitHub/main
python -m uvicorn api.main:app --reload
```

**DevOps team registers:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_devops",
    "email": "john@company.com",
    "password": "SecurePassword123!",
    "full_name": "John Smith"
  }'
```

**Response:**
```json
{
  "username": "john_devops",
  "email": "john@company.com",
  "full_name": "John Smith",
  "disabled": false
}
```

**Then they login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=john_devops&password=SecurePassword123!"
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Use the token:**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/items
```

---

### Option 2: You Create Admin Accounts

If you want to create admin users for your DevOps team:

**Create admin user script:**
```python
# create_admin.py
from api.auth import get_password_hash
from api.database import get_db, init_db
from datetime import datetime

init_db()
db = next(get_db())

admin_user = {
    "username": "devops_admin",
    "email": "devops@company.com",
    "hashed_password": get_password_hash("AdminPass123!"),
    "full_name": "DevOps Admin",
    "disabled": False,
    "role": "admin",  # ✅ Admin role!
    "created_at": datetime.utcnow().isoformat(),
}

db["users"]["devops_admin"] = admin_user
print("✅ Admin user created!")
print(f"Username: {admin_user['username']}")
print(f"Password: AdminPass123!")
print("⚠️  Change password after first login!")
```

**Run it:**
```bash
python create_admin.py
```

---

## 🔒 Security Considerations

### Bitwarden Credentials (YOUR secrets)
- ✅ Keep private - don't share
- ✅ Only YOU should run `bwload`
- ✅ API keys loaded in YOUR environment
- ❌ Don't share .bitwarden-oauth file
- ❌ Don't give team members your master password

### API User Accounts (Team access)
- ✅ Each person gets their own account
- ✅ Each has unique username/password
- ✅ Separate from your Bitwarden
- ✅ Can be revoked individually
- ✅ Role-based access (user vs admin)

---

## 🎯 Recommended Setup for Team

### For You (System Admin):
```bash
# Your workflow
bwload                          # Load YOUR API keys
python -m uvicorn api.main:app  # Start API server
# API runs with YOUR keys in environment
```

### For DevOps Team:
```bash
# Their workflow
# 1. Register account via API (one time)
curl -X POST http://localhost:8000/auth/register -d {...}

# 2. Login to get token
curl -X POST http://localhost:8000/auth/login -d {...}

# 3. Use token for API access
curl -H "Authorization: Bearer <token>" http://localhost:8000/items
```

---

## 👥 User Roles Explained

### Current Roles:

**1. User (default)**
- Can register themselves
- Access their own data
- Cannot access admin endpoints
- Default for all new registrations

**2. Admin**
- Access admin endpoints
- Can see all users
- Manage system
- Must be manually created

### Role Assignment:

**Default Registration:**
```python
# In api/main.py
new_user = {
    ...
    "role": "user",  # Always "user" for self-registration
}
```

**Manual Admin Creation:**
```python
# You must manually create admins
admin_user = {
    ...
    "role": "admin",  # You set this
}
```

---

## 🚀 Production Deployment Scenarios

### Scenario 1: You Run Everything
- You: Have Bitwarden access, admin account
- Team: Regular user accounts via registration
- API keys: Loaded from YOUR Bitwarden
- User data: Stored in database

### Scenario 2: Shared Infrastructure
- Server: Has API keys in .env file
- You: Admin account + Bitwarden access
- Team: User/admin accounts in API
- Deployment: API keys in .env, users in DB

### Scenario 3: Multi-Admin Setup
- You: Create multiple admin accounts
- DevOps leads: Get admin role manually
- Developers: Get user role via registration
- API keys: Loaded from .env or secrets manager

---

## 📋 Quick Commands

### Check Current Users
```bash
# Login as admin first
TOKEN="your-admin-token"

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/admin/users
```

### Create User Programmatically
```python
import requests

response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "username": "new_user",
        "email": "user@example.com",
        "password": "SecurePass123!",
        "full_name": "New User"
    }
)
print(response.json())
```

### Test Authentication
```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test123!","full_name":"Test User"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -d "username=test&password=Test123!" | jq -r '.access_token')

# 3. Access protected endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/auth/me
```

---

## 🔍 Common Questions

**Q: Can my team access my Bitwarden vault?**
A: No! Bitwarden is your personal API key storage. Don't share credentials.

**Q: How do team members get API access?**
A: They register via `/auth/register`, get their own account and JWT token.

**Q: Do they need separate API keys?**
A: No! The API runs with YOUR keys (from Bitwarden/env). Their accounts just authenticate to the API.

**Q: How do I make someone admin?**
A: Manually create their account with `"role": "admin"` in the database.

**Q: Can I revoke someone's access?**
A: Yes! Set their `"disabled": true` in the database.

---

## 🎓 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│ YOUR Environment                                    │
│ ┌─────────────────┐                                │
│ │   Bitwarden     │  ← Your API Keys               │
│ │  (Your Vault)   │    (GOOGLE_API_KEY, etc.)     │
│ └────────┬────────┘                                │
│          │ bwload                                   │
│          ↓                                          │
│ ┌─────────────────┐                                │
│ │  .env file      │  ← Exported Keys              │
│ └────────┬────────┘                                │
│          │                                          │
│          ↓                                          │
│ ┌─────────────────────────────────────────┐        │
│ │          REST API Server                │        │
│ │  (Runs with YOUR API keys loaded)       │        │
│ └────────┬────────────────────────────────┘        │
│          │                                          │
└──────────┼──────────────────────────────────────────┘
           │
           ↓
    ┌──────────────────────────────────┐
    │   User Authentication Database    │
    │                                   │
    │   User 1: john@company.com       │
    │   User 2: jane@company.com       │
    │   User 3: devops@company.com     │
    │   (Each has own password)        │
    └──────────────────────────────────┘
           │
           ↓
    DevOps Team Members
    - Register via API
    - Get JWT tokens
    - Access protected endpoints
    - Use YOUR API keys (via API)
```

---

## ✅ Summary

**What Bitwarden Does:**
- Stores YOUR API keys securely
- You access with `bwload`
- Loads keys into environment
- Personal use only

**What API Authentication Does:**
- Creates user accounts
- Each user has username/password
- Issues JWT tokens
- Controls access to API

**Your DevOps Team:**
- ✅ Can register accounts via API
- ✅ Can login and get JWT tokens
- ✅ Can access API with tokens
- ❌ Cannot use your Bitwarden
- ❌ Don't need separate API keys (they use yours via API)

---

**Next Steps:**
1. Start the API: `python -m uvicorn api.main:app --reload`
2. Test registration: Use curl commands above
3. Create admin accounts if needed: Use create_admin.py
4. Share API URL with team: `http://your-server:8000`

**Your Bitwarden stays private!** 🔒

