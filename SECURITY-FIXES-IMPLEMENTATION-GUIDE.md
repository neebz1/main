# 🔒 Security Fixes Implementation Guide

This guide provides step-by-step instructions to fix all security issues identified in the audit.

---

## 🚨 CRITICAL FIXES (Do These First!)

### 1. Fix CORS Configuration

**File:** `api/main.py`

**Current (INSECURE):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ DANGEROUS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Fixed (SECURE):**
```python
import os

# Get allowed origins from environment
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ SECURE
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specify exact methods
    allow_headers=["*"],
)
```

**In .env:**
```bash
# Development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Production
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

---

### 2. Generate and Set Unique SECRET_KEY

**Step 1:** Generate a secure secret key
```bash
openssl rand -hex 32
```

**Step 2:** Add to .env
```bash
# .env
SECRET_KEY=<your-generated-key-here>
```

**Step 3:** Update config.py (already done, but verify)
```python
# api/config.py
SECRET_KEY: str = os.getenv("SECRET_KEY")  # Remove default!

# Add validation
if not SECRET_KEY or SECRET_KEY.startswith("your-secret-key"):
    raise ValueError("SECRET_KEY must be set in environment!")
```

**Step 4:** Store in Bitwarden for production
```bash
./bw-add-key.sh "API Secret Key" "<your-generated-key>"
```

---

### 3. Add Rate Limiting

**Step 1:** Install slowapi
```bash
pip install slowapi
echo "slowapi==0.1.9" >> api/requirements.txt
```

**Step 2:** Update main.py
```python
# At the top of api/main.py
from .security_fixes import (
    setup_rate_limiting,
    add_security_headers_middleware,
)

# After app initialization
limiter = setup_rate_limiting(app)

# Add security headers
app.middleware("http")(add_security_headers_middleware)

# Apply to login endpoint
@app.post("/auth/login", response_model=Token, tags=["Authentication"])
@limiter.limit("5/minute")  # ✅ Add this line
async def login(
    request: Request,  # ✅ Add this parameter
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    # ... rest of the code
```

**Step 3:** Apply to other endpoints
```python
# Registration
@app.post("/auth/register")
@limiter.limit("3/minute")  # Prevent spam registration
async def register(...):

# General API
@app.get("/items")
@limiter.limit("60/minute")  # 60 requests per minute
async def get_items(...):

# Admin endpoints
@app.get("/admin/users")
@limiter.limit("10/minute")  # Lower limit for admin
async def list_users(...):
```

---

### 4. Fix Command Injection in Cloud Builder

**File:** `cloud_ai_builder.py`

**Replace execute_command method:**
```python
# Import at top
from pathlib import Path
import re

# ALLOWED_COMMANDS whitelist
ALLOWED_COMMANDS = {
    'git_status': ['git', 'status'],
    'git_push': ['git', 'push', 'origin', 'main'],
    'git_log': ['git', 'log', '--oneline', '-10'],
    'pytest_version': ['pytest', '--version'],
    'check_processes': ['ps', 'aux'],
}

def execute_command(self, command_key: str) -> str:
    """Execute a pre-approved safe command"""

    if command_key not in ALLOWED_COMMANDS:
        return f"❌ Command '{command_key}' not allowed. Available: {', '.join(ALLOWED_COMMANDS.keys())}"

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[command_key],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,  # ✅ CRITICAL: Never use shell=True
            cwd=self.project_dir
        )

        output = result.stdout if result.returncode == 0 else result.stderr
        status = "✅" if result.returncode == 0 else "❌"

        return f"{status} Command: {command_key}\n\nOutput:\n{output}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

**Update UI button callbacks:**
```python
# In create_ui() function
git_status_btn.click(
    lambda: builder.execute_command("git_status"),  # Use key instead
    outputs=output
)
```

---

## ⚠️ HIGH PRIORITY FIXES

### 5. Add Admin Role-Based Access Control

**Step 1:** Update models.py
```python
# api/models.py

class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: Optional[str] = Field(None)
    role: str = Field(default="user")  # ✅ Add this

class UserCreate(UserBase):
    password: str = Field(...)

    @validator("role")
    def validate_role(cls, v):
        """Only allow user role during registration"""
        if v != "user":
            return "user"  # Force user role for registration
        return v
```

**Step 2:** Update main.py registration
```python
@app.post("/auth/register")
async def register(user: UserCreate, db=Depends(get_db)):
    # ... existing code ...

    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "disabled": False,
        "role": "user",  # ✅ Always user for registration
        "created_at": datetime.utcnow().isoformat(),
    }
```

**Step 3:** Protect admin endpoints
```python
from .security_fixes import get_current_admin_user

@app.get("/admin/users", tags=["Admin"])
async def list_users(
    current_user: User = Depends(get_current_admin_user),  # ✅ Changed
    db=Depends(get_db)
):
```

**Step 4:** Create first admin user manually
```python
# Run this once to create admin:
# python -c "from api.main import *; create_admin_user()"

def create_admin_user():
    """Utility to create admin user"""
    init_db()
    db = next(get_db())

    admin = {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("ChangeThisPassword123!"),
        "full_name": "Admin User",
        "disabled": False,
        "role": "admin",  # ✅ Admin role
        "created_at": datetime.utcnow().isoformat(),
    }

    db["users"]["admin"] = admin
    print("✅ Admin user created: username=admin, password=ChangeThisPassword123!")
    print("⚠️  CHANGE THE PASSWORD IMMEDIATELY!")
```

---

### 6. Migrate to PostgreSQL (Production)

**Step 1:** Install dependencies
```bash
pip install sqlalchemy psycopg2-binary alembic
```

**Step 2:** Create database models
```python
# api/database_models.py (new file)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="user", nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("ItemDB", back_populates="owner")

class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("UserDB", back_populates="items")
```

**Step 3:** Update database.py
```python
# api/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database_models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./api.db"  # Default to SQLite for development
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Step 4:** Setup PostgreSQL
```bash
# Install PostgreSQL
brew install postgresql  # macOS
# or
sudo apt-get install postgresql  # Linux

# Create database
createdb api_db

# Set DATABASE_URL
export DATABASE_URL="postgresql://username:password@localhost:5432/api_db"
```

---

### 7. Enable HTTPS Enforcement

**In main.py:**
```python
import os
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Only in production
if os.getenv("ENVIRONMENT") == "production":
    # Force HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )
```

---

## 🔶 MEDIUM PRIORITY FIXES

### 8. Add Gradio Authentication

**Update all Gradio apps:**

```python
# cloud_ai_builder.py, app.py, etc.
import os

gradio_auth = None
if os.getenv("GRADIO_PASSWORD"):
    gradio_auth = (
        os.getenv("GRADIO_USER", "admin"),
        os.getenv("GRADIO_PASSWORD")
    )

app.launch(
    server_name="127.0.0.1",  # Local only
    share=False,  # Disable public sharing
    auth=gradio_auth,  # Add authentication
    auth_message="Enter credentials to access"
)
```

**In .env:**
```bash
GRADIO_USER=admin
GRADIO_PASSWORD=<generate-strong-password>
```

---

### 9. Implement Refresh Tokens

**Add to auth.py:**
```python
def create_refresh_token(data: dict) -> str:
    """Create a refresh token (valid for 7 days)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def verify_refresh_token(token: str) -> Optional[str]:
    """Verify refresh token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            return None
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None
```

**Add endpoint in main.py:**
```python
@app.post("/auth/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db=Depends(get_db)
):
    """Get new access token using refresh token"""
    username = verify_refresh_token(refresh_token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Verify user still exists and is active
    users = db.get("users", {})
    user = users.get(username)

    if not user or user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled"
        )

    # Create new access token
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

**Update login to return both tokens:**
```python
@app.post("/auth/login", response_model=Token)
async def login(...):
    # ... existing code ...

    access_token = create_access_token(...)
    refresh_token = create_refresh_token(data={"sub": username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # ✅ Add this
        "token_type": "bearer"
    }
```

**Update Token model:**
```python
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None  # ✅ Add this
    token_type: str = "bearer"
```

---

### 10. Add Security Logging

**Update main.py:**
```python
from .security_fixes import setup_security_logger

# At startup
security_logger = setup_security_logger()

# In login endpoint
@app.post("/auth/login")
async def login(request: Request, ...):
    # ... existing code ...

    # Log failed attempts
    if not verify_password(...):
        security_logger.warning(
            f"Failed login attempt - "
            f"Username: {form_data.username} - "
            f"IP: {request.client.host}"
        )
        raise HTTPException(...)

    # Log successful login
    security_logger.info(
        f"Successful login - "
        f"Username: {form_data.username} - "
        f"IP: {request.client.host}"
    )
```

---

## ℹ️ LOW PRIORITY / BEST PRACTICES

### 11. Run Dependency Scan

```bash
# Install safety
pip install safety pip-audit

# Check for vulnerabilities
safety check --json > security_scan.json
pip-audit --format json > audit_results.json

# Review results
cat security_scan.json
cat audit_results.json
```

**Add to requirements:**
```bash
echo "safety==2.3.5" >> requirements.txt
echo "pip-audit==2.6.1" >> requirements.txt
```

**Create scan script:**
```bash
# create: security-scan.sh
#!/bin/bash
echo "🔍 Running security scans..."
safety check
pip-audit
echo "✅ Scan complete"
```

---

### 12. Add Database Backups

**Add to database.py:**
```python
import shutil
from datetime import datetime
from pathlib import Path

def backup_db():
    """Backup database file"""
    if DB_FILE.exists():
        backup_dir = Path(__file__).parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"db_backup_{timestamp}.json"

        shutil.copy2(DB_FILE, backup_file)
        print(f"✅ Database backed up to: {backup_file}")

        # Keep only last 10 backups
        backups = sorted(backup_dir.glob("db_backup_*.json"))
        for old_backup in backups[:-10]:
            old_backup.unlink()

        return backup_file
    return None

# Call on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    backup_db()
    print("👋 API shutting down")
```

---

## 📋 VERIFICATION CHECKLIST

After implementing fixes, verify:

- [ ] SECRET_KEY is unique and set in .env
- [ ] CORS only allows specific origins
- [ ] Rate limiting works on login endpoint
- [ ] Command execution uses whitelist
- [ ] Admin endpoints require admin role
- [ ] Gradio apps have authentication
- [ ] Security headers are present
- [ ] Failed logins are logged
- [ ] No secrets in git history
- [ ] Dependencies scanned for vulnerabilities

---

## 🧪 TESTING

**Test rate limiting:**
```bash
# Should block after 5 attempts
for i in {1..10}; do
  curl -X POST http://localhost:8000/auth/login \
    -d "username=test&password=wrong"
  sleep 1
done
```

**Test CORS:**
```bash
# Should be rejected
curl -H "Origin: https://evil.com" \
  http://localhost:8000/items
```

**Test admin access:**
```bash
# Get token as regular user
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -d "username=user&password=pass" | jq -r '.access_token')

# Should be rejected
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/admin/users
```

---

## 🚀 DEPLOYMENT CHECKLIST

Before deploying to production:

1. [ ] All CRITICAL fixes implemented
2. [ ] All HIGH priority fixes implemented
3. [ ] .env.production created with secure values
4. [ ] SECRET_KEY generated and stored in Bitwarden
5. [ ] PostgreSQL database setup
6. [ ] HTTPS certificate configured
7. [ ] Rate limiting tested
8. [ ] Security logging enabled
9. [ ] Backups configured
10. [ ] Monitoring setup (Sentry/logging)

---

**Questions? Review the SECURITY-AUDIT-REPORT.md for detailed explanations.**

