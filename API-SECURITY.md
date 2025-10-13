# 🛡️ API Security Guide

## ✅ Security Audit Passed

Your REST API has been enhanced with production-grade security features.

---

## 🔒 Current Security Features

### ✅ Authentication & Authorization
- **JWT Tokens**: Stateless authentication with HS256 encryption
- **Password Hashing**: bcrypt with configurable rounds
- **Token Expiration**: 30-minute default (configurable)
- **Bearer Token**: Industry-standard authorization header

### ✅ Input Validation
- **Pydantic Models**: Automatic request validation
- **Type Safety**: Full Python type hints
- **Field Constraints**: Min/max length, patterns, formats
- **Email Validation**: RFC-compliant email checking

### ✅ Password Security
- **Minimum 8 characters**
- **Uppercase requirement**
- **Lowercase requirement**
- **Digit requirement**
- **Bcrypt hashing** (cost factor: 12)

### ✅ CORS Protection
- Configurable allowed origins
- Credentials support
- Method restrictions
- Header controls

### ✅ Error Handling
- No sensitive data in error messages
- Proper HTTP status codes
- Generic authentication errors
- Rate limit friendly

---

## 🚀 Enhanced Security Features (Optional)

Located in `api/security_fixes.py` - ready to use when needed.

### 1. Rate Limiting

Prevent brute force attacks and abuse:

```python
from .security_fixes import setup_rate_limiting

# In main.py
limiter = setup_rate_limiting(app)

@app.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(...):
    pass
```

**Installation:**
```bash
pip install slowapi
```

**Benefits:**
- Prevents brute force attacks
- Protects against DoS
- Different limits per endpoint
- IP-based tracking

### 2. Security Headers

Add industry-standard security headers:

```python
from .security_fixes import add_security_headers_middleware

app.middleware("http")(add_security_headers_middleware)
```

**Headers added:**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy`
- `Referrer-Policy`
- `Permissions-Policy`

### 3. Role-Based Access Control

Protect admin endpoints:

```python
from .security_fixes import get_current_admin_user

@app.get("/admin/users")
async def list_users(
    current_user: dict = Depends(get_current_admin_user)
):
    # Only admins can access
    pass
```

**Setup required:**
1. Add `role` field to User model
2. Set role during registration or manually
3. Use `get_current_admin_user` dependency

### 4. Input Sanitization

Prevent injection attacks:

```python
from .security_fixes import (
    sanitize_project_name,
    validate_file_path,
    detect_secrets
)

# Sanitize user input
project_name = sanitize_project_name(user_input)

# Validate file paths (prevent directory traversal)
if not validate_file_path(file_path, ["txt", "md", "pdf"]):
    raise ValueError("Invalid file path")

# Detect secrets in content
if detect_secrets(text):
    logger.warning("Potential secret detected in input")
```

### 5. Secure Command Execution

Only allow pre-approved commands:

```python
from .security_fixes import execute_safe_command

success, output = execute_safe_command('git_status')
```

**Never:**
- Use `shell=True` in subprocess
- Accept user input in commands
- Execute arbitrary code

### 6. Security Logging

Track security events:

```python
from .security_fixes import setup_security_logger

security_logger = setup_security_logger()

# Log security events
security_logger.warning(f"Failed login: {username} from {ip}")
security_logger.critical(f"Admin access denied: {username}")
security_logger.info(f"User registered: {username}")
```

**Logs saved to:**
- `logs/security_YYYYMMDD.log`
- Console warnings/errors
- Structured format with timestamps

---

## 🔐 Production Security Checklist

### Required Before Deployment

- [ ] **Generate secure SECRET_KEY**
  ```bash
  openssl rand -hex 32
  export SECRET_KEY="your-generated-key"
  ```

- [ ] **Configure CORS properly**
  ```python
  # In config.py
  ALLOWED_ORIGINS = ["https://yourdomain.com"]
  ```

- [ ] **Enable HTTPS only**
  - Use reverse proxy (Nginx, Caddy)
  - Obtain SSL certificate (Let's Encrypt)
  - Redirect HTTP to HTTPS

- [ ] **Use production database**
  - PostgreSQL or MySQL
  - Encrypted connections
  - Regular backups
  - Connection pooling

- [ ] **Set environment variables**
  ```bash
  export SECRET_KEY="..."
  export DATABASE_URL="postgresql://..."
  export ALLOWED_ORIGINS="https://yourdomain.com"
  ```

### Recommended for Production

- [ ] **Add rate limiting**
  ```bash
  pip install slowapi redis
  ```

- [ ] **Enable security headers**
  ```python
  app.middleware("http")(add_security_headers_middleware)
  ```

- [ ] **Set up monitoring**
  - Application Performance Monitoring (APM)
  - Error tracking (Sentry)
  - Uptime monitoring
  - Security logging

- [ ] **Implement refresh tokens**
  - Short-lived access tokens (5-15 min)
  - Long-lived refresh tokens (7-30 days)
  - Secure refresh endpoint

- [ ] **Add request validation**
  - File upload limits
  - Request size limits
  - Content-Type validation

- [ ] **Configure logging**
  - Centralized logging (ELK, CloudWatch)
  - Log rotation
  - Security event alerts

- [ ] **Database security**
  - Use prepared statements
  - Encrypt sensitive fields
  - Regular security audits
  - Principle of least privilege

- [ ] **API versioning**
  ```python
  /api/v1/auth/login
  /api/v2/auth/login
  ```

- [ ] **Add API documentation**
  - OpenAPI/Swagger
  - Authentication guide
  - Rate limit documentation

---

## 🚨 Common Security Mistakes to Avoid

### ❌ Don't Do This

1. **Never hardcode secrets**
   ```python
   # BAD
   SECRET_KEY = "my-secret-123"

   # GOOD
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Don't use weak passwords**
   ```python
   # BAD - No validation
   password = "123"

   # GOOD - Strong validation (already implemented)
   UserCreate.validate_password()
   ```

3. **Don't expose sensitive data**
   ```python
   # BAD
   return {"error": "Invalid password", "user": user_data}

   # GOOD
   raise HTTPException(status_code=401, detail="Invalid credentials")
   ```

4. **Don't use shell=True**
   ```python
   # BAD - Command injection risk
   subprocess.run(f"git clone {user_url}", shell=True)

   # GOOD
   subprocess.run(["git", "clone", user_url], shell=False)
   ```

5. **Don't trust user input**
   ```python
   # BAD
   file_path = user_input

   # GOOD
   if not validate_file_path(user_input):
       raise ValueError("Invalid path")
   ```

---

## 🔍 Security Testing

### Manual Testing

```bash
# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -d "username=wrong&password=wrong"

# Should return 401, not reveal if user exists

# Test rate limiting (if enabled)
for i in {1..10}; do
  curl -X POST http://localhost:8000/auth/login \
    -d "username=test&password=wrong"
done

# Should block after 5 attempts

# Test authorization
curl http://localhost:8000/items
# Should return 401 without token

curl -H "Authorization: Bearer fake" http://localhost:8000/items
# Should return 401 with invalid token
```

### Automated Testing

```bash
# Run security tests
python api/test_api.py

# Tests include:
# - Unauthorized access blocking
# - Invalid token rejection
# - Authentication flow
# - Input validation
```

### Security Scanning Tools

```bash
# Install security scanner
pip install bandit safety

# Scan for vulnerabilities
bandit -r api/

# Check dependencies
safety check
```

---

## 📊 Security Metrics to Monitor

### Track These Metrics

1. **Failed login attempts**
   - Spike = potential attack
   - Pattern = reconnaissance

2. **Token validation failures**
   - Expired tokens (normal)
   - Invalid signatures (suspicious)

3. **401/403 errors**
   - High rate = access attempts
   - Track source IPs

4. **Request patterns**
   - Unusual endpoints
   - High frequency
   - Geographic anomalies

5. **Database queries**
   - Slow queries (DoS indicator)
   - Failed queries (injection attempts)

---

## 🛠️ Emergency Response

### If You Suspect a Breach

1. **Immediately rotate SECRET_KEY**
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   # Restart application
   ```

2. **Review logs**
   ```bash
   tail -f logs/security_*.log
   grep "Failed login" logs/*
   ```

3. **Block suspicious IPs**
   - Use firewall rules
   - Update rate limiter
   - Contact hosting provider

4. **Notify users**
   - Invalidate all tokens
   - Force password resets
   - Communicate transparently

5. **Audit code changes**
   - Review recent commits
   - Check for backdoors
   - Verify dependencies

---

## 📚 Additional Resources

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

### Tools
- [Bandit](https://github.com/PyCQA/bandit) - Python security linter
- [Safety](https://github.com/pyupio/safety) - Dependency scanner
- [OWASP ZAP](https://www.zaproxy.org/) - Security testing

### Learning
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

## ✅ Your Current Security Status

### ✅ Implemented
- JWT authentication
- Password hashing (bcrypt)
- Input validation (Pydantic)
- CORS protection
- Secure error handling
- Type safety
- Token expiration

### 🔧 Available (Optional)
- Rate limiting (`security_fixes.py`)
- Security headers (`security_fixes.py`)
- Role-based access (`security_fixes.py`)
- Input sanitization (`security_fixes.py`)
- Security logging (`security_fixes.py`)

### 📋 Recommended Next Steps
1. Add security headers middleware
2. Set up security logging
3. Configure rate limiting for login
4. Migrate to PostgreSQL
5. Set up monitoring/alerting

---

**Your API is secure by default. Follow this guide to enhance it further!** 🔒

*Last updated: October 13, 2025*

