# 🏗️ REST API Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATIONS                     │
│  (Web Browser, Mobile App, Python Client, curl, etc.)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      FASTAPI SERVER                          │
│                    (Port 8000)                               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    ENDPOINTS                            │ │
│  │  • /auth/register  • /auth/login  • /auth/me           │ │
│  │  • /items          • /items/{id}                        │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │              AUTHENTICATION LAYER                       │ │
│  │  • JWT Token Verification                               │ │
│  │  • Password Hashing (bcrypt)                            │ │
│  │  • OAuth2 Password Flow                                 │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │              BUSINESS LOGIC LAYER                       │ │
│  │  • Input Validation (Pydantic)                          │ │
│  │  • Authorization Checks                                 │ │
│  │  • CRUD Operations                                      │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │              DATABASE LAYER                             │ │
│  │  • In-Memory Storage (dev)                              │ │
│  │  • JSON File Persistence                                │ │
│  │  • [PostgreSQL/MySQL for production]                    │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │  Server │
└────┬────┘                                    └────┬────┘
     │                                              │
     │  1. POST /auth/register                     │
     │  {username, email, password}                │
     ├─────────────────────────────────────────────►
     │                                              │
     │                         Hash password (bcrypt)
     │                         Store user in DB    │
     │                                              │
     │  ◄─────────────────────────────────────────┤
     │  {username, email, disabled: false}         │
     │                                              │
     │  2. POST /auth/login                        │
     │  {username, password}                       │
     ├─────────────────────────────────────────────►
     │                                              │
     │                         Verify password     │
     │                         Create JWT token    │
     │                         Sign with SECRET_KEY│
     │                                              │
     │  ◄─────────────────────────────────────────┤
     │  {access_token: "eyJhbG...", type: "bearer"}│
     │                                              │
     │  3. GET /items                              │
     │  Authorization: Bearer eyJhbG...            │
     ├─────────────────────────────────────────────►
     │                                              │
     │                         Decode JWT token    │
     │                         Verify signature    │
     │                         Check expiration    │
     │                         Get user from DB    │
     │                         Return user's items │
     │                                              │
     │  ◄─────────────────────────────────────────┤
     │  [{id: 1, title: "...", ...}]               │
     │                                              │
```

---

## JWT Token Structure

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "username",           // Subject (username)
  "exp": 1697234567,           // Expiration timestamp
  "iat": 1697232767,           // Issued at timestamp
  "type": "access"             // Token type
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)

Result:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZSIsImV4cCI6MTY5NzIzNDU2N30.signature
```

---

## Request/Response Flow

```
┌───────────────────────────────────────────────────────────┐
│                     HTTP REQUEST                          │
│                                                           │
│  POST /items                                              │
│  Authorization: Bearer eyJhbG...                          │
│  Content-Type: application/json                           │
│                                                           │
│  {"title": "New Item", "description": "..."}              │
└──────────────┬────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  1. CORS Middleware                                       │
│     • Check origin                                        │
│     • Add CORS headers                                    │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  2. OAuth2 Middleware                                     │
│     • Extract token from Authorization header             │
│     • Decode JWT token                                    │
│     • Verify signature with SECRET_KEY                    │
│     • Check expiration                                    │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  3. Get Current User Dependency                           │
│     • Extract username from token                         │
│     • Query database for user                             │
│     • Check if user is active                             │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  4. Pydantic Validation                                   │
│     • Validate request body against ItemCreate model      │
│     • Check field types and constraints                   │
│     • Raise validation error if invalid                   │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  5. Business Logic                                        │
│     • Create new item                                     │
│     • Add metadata (id, owner, created_at)                │
│     • Store in database                                   │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│  6. Response Serialization                                │
│     • Convert item to JSON                                │
│     • Validate against Item response model                │
│     • Add HTTP headers                                    │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│                     HTTP RESPONSE                         │
│                                                           │
│  200 OK                                                   │
│  Content-Type: application/json                           │
│                                                           │
│  {                                                        │
│    "id": 1,                                               │
│    "title": "New Item",                                   │
│    "description": "...",                                  │
│    "owner": "username",                                   │
│    "created_at": "2025-10-13T12:34:56"                    │
│  }                                                        │
└───────────────────────────────────────────────────────────┘
```

---

## Data Models

```
User Model:
┌─────────────────────────────────────┐
│ username: str                       │
│ email: str                          │
│ hashed_password: str                │
│ full_name: Optional[str]            │
│ disabled: bool = False              │
└─────────────────────────────────────┘

Item Model:
┌─────────────────────────────────────┐
│ id: int                             │
│ title: str                          │
│ description: Optional[str]          │
│ owner: str                          │
│ created_at: str                     │
└─────────────────────────────────────┘

Token Model:
┌─────────────────────────────────────┐
│ access_token: str                   │
│ token_type: str = "bearer"          │
└─────────────────────────────────────┘
```

---

## Database Structure (Current)

```json
{
  "users": {
    "john_doe": {
      "username": "john_doe",
      "email": "john@example.com",
      "hashed_password": "$2b$12$...",
      "full_name": "John Doe",
      "disabled": false,
      "created_at": "2025-10-13T12:00:00"
    }
  },
  "items": {
    "john_doe": [
      {
        "id": 1,
        "title": "First Item",
        "description": "My first item",
        "owner": "john_doe",
        "created_at": "2025-10-13T12:30:00"
      }
    ]
  }
}
```

---

## Security Layers

```
Layer 1: CORS Protection
  ↓ Only allow requests from trusted origins

Layer 2: HTTPS (Production)
  ↓ Encrypt all data in transit

Layer 3: JWT Token Authentication
  ↓ Verify token signature and expiration

Layer 4: User Authorization
  ↓ Check if user owns the resource

Layer 5: Input Validation
  ↓ Validate all inputs with Pydantic

Layer 6: SQL Injection Prevention
  ↓ Use parameterized queries (with SQL DB)

Layer 7: Rate Limiting (Production)
  ↓ Limit requests per IP/user
```

---

## Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │   Internet   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  CDN / WAF   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ API #1  │      │ API #2  │      │ API #3  │
    │(FastAPI)│      │(FastAPI)│      │(FastAPI)│
    └────┬────┘      └────┬────┘      └────┬────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼───────┐
                    │   Database   │
                    │ (PostgreSQL) │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │    Redis     │
                    │   (Cache)    │
                    └──────────────┘
```

---

## File Organization

```
api/
├── __init__.py              # Package marker
│
├── main.py                  # Application entry point
│   ├── FastAPI app instance
│   ├── CORS middleware
│   ├── All endpoints
│   └── Startup events
│
├── models.py                # Data models
│   ├── User models (Base, Create, Response)
│   ├── Token models
│   ├── Item models
│   └── Validators
│
├── auth.py                  # Authentication
│   ├── Password hashing
│   ├── JWT creation/verification
│   ├── OAuth2 scheme
│   └── Dependency functions
│
├── database.py              # Data persistence
│   ├── In-memory storage
│   ├── JSON file persistence
│   ├── Database session
│   └── SQL migration guide
│
├── config.py                # Configuration
│   ├── Settings class
│   ├── Environment variables
│   └── Security settings
│
└── data/                    # Runtime data
    └── db.json              # Persistent storage
```

---

## Technology Stack

```
Core Framework:
  FastAPI 0.104.1
    ↓
  Uvicorn (ASGI server)
    ↓
  Python 3.9+

Authentication:
  python-jose (JWT)
  passlib + bcrypt (password hashing)
  python-multipart (form data)

Validation:
  Pydantic 2.5.0 (data validation)

Middleware:
  FastAPI CORS middleware
  OAuth2 password bearer

Development:
  Auto-reload server
  Interactive docs (Swagger UI)
  Type checking (mypy compatible)
```

---

## API Versioning Strategy (Future)

```
Current:
  /auth/register
  /items

Recommended for v2:
  /api/v1/auth/register
  /api/v1/items

  /api/v2/auth/register  (with new features)
  /api/v2/items          (backward incompatible changes)

Router setup:
  app.include_router(v1_router, prefix="/api/v1")
  app.include_router(v2_router, prefix="/api/v2")
```

---

## Monitoring & Observability (Production)

```
Logging:
  Python logging module
  → File logs
  → Centralized logging (ELK, Datadog)

Metrics:
  Request count
  Response times
  Error rates
  Active users

Monitoring:
  Prometheus + Grafana
  Application Performance Monitoring (APM)
  Uptime monitoring
  Error tracking (Sentry)

Health Checks:
  /health endpoint
  Database connectivity
  External service checks
```

---

## Performance Characteristics

```
Current Setup:
  Storage:      In-memory (microsecond latency)
  Auth:         Stateless JWT (no DB lookup)
  Validation:   Pydantic (fast C bindings)
  Framework:    FastAPI (async-capable)

Expected Performance:
  Requests/sec: 1,000+ (single instance)
  Latency:      <10ms (local)
  Concurrent:   100+ (with async DB)

Production Setup:
  Requests/sec: 10,000+ (3 instances)
  Latency:      <50ms (with cache)
  Concurrent:   1,000+ (with Redis cache)
```

---

**Architecture designed for scalability, security, and maintainability** 🚀

