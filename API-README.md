# 🚀 Secure REST API with JWT Authentication

A production-ready REST API built with **FastAPI**, featuring JWT authentication, user management, and protected endpoints.

---

## ✨ Features

- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **User Registration & Login** - Complete user management
- ✅ **Password Hashing** - Bcrypt encryption
- ✅ **Protected Endpoints** - Token-based access control
- ✅ **Input Validation** - Pydantic models with validation
- ✅ **Auto Documentation** - Interactive Swagger UI & ReDoc
- ✅ **CORS Support** - Cross-origin resource sharing
- ✅ **Rate Limiting Ready** - Prepared for production scaling
- ✅ **Type Safety** - Full Python type hints

---

## 📁 Project Structure

```
api/
├── __init__.py           # Package initialization
├── main.py              # FastAPI application & endpoints
├── models.py            # Pydantic data models
├── auth.py              # Authentication & JWT utilities
├── database.py          # Database management
├── config.py            # Configuration & settings
├── requirements.txt     # Python dependencies
├── test_api.py          # Testing script
└── data/
    └── db.json          # Persistent storage (auto-created)
```

---

## 🚀 Quick Start

### 1. Start the API

```bash
# Make startup script executable
chmod +x start-api.sh

# Start the server
./start-api.sh
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### 2. Test the API

```bash
# In another terminal, run the test script
python api/test_api.py
```

---

## 📚 API Endpoints

### 🔓 Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint (health check) |
| `GET` | `/health` | Detailed health check |
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login & get JWT token |

### 🔒 Protected Endpoints (Require Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/me` | Get current user info |
| `GET` | `/items` | Get all user's items |
| `POST` | `/items` | Create new item |
| `GET` | `/items/{id}` | Get specific item |
| `DELETE` | `/items/{id}` | Delete item |
| `GET` | `/admin/users` | List all users |

---

## 🔐 Authentication Flow

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

### 2. Login & Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePass123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Token for Protected Endpoints

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

---

## 🎯 Usage Examples

### Create an Item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Item",
    "description": "This is a test item"
  }'
```

### Get All Items

```bash
curl -X GET "http://localhost:8000/items" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete an Item

```bash
curl -X DELETE "http://localhost:8000/items/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🛠️ Development

### Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r api/requirements.txt
```

### Run Development Server

```bash
uvicorn api.main:app --reload
```

### Run Tests

```bash
python api/test_api.py
```

---

## 🔒 Security Features

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

### JWT Tokens

- **Algorithm**: HS256
- **Expiration**: 30 minutes (configurable)
- **Secret Key**: Auto-generated or from environment

### Security Best Practices

✅ Passwords hashed with bcrypt
✅ JWT tokens for stateless auth
✅ Token expiration implemented
✅ CORS configured
✅ Input validation with Pydantic
✅ SQL injection prevention (when using SQL DB)

---

## 🚀 Production Deployment

### 1. Set Environment Variables

```bash
# Generate a secure secret key
export SECRET_KEY=$(openssl rand -hex 32)

# Optional: Database URL
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

### 2. Update Configuration

Edit `api/config.py`:

```python
# Set allowed origins
ALLOWED_ORIGINS = ["https://yourdomain.com"]

# Use environment secret key
SECRET_KEY = os.getenv("SECRET_KEY")
```

### 3. Migrate to SQL Database

The current implementation uses in-memory storage. For production:

1. Uncomment SQL dependencies in `requirements.txt`
2. Follow migration guide in `api/database.py`
3. Set up PostgreSQL/MySQL database
4. Run migrations with Alembic

### 4. Deploy with Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY api/ /app/api/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Deploy to Cloud

**Heroku:**
```bash
heroku create your-api-name
git push heroku main
```

**Railway:**
```bash
railway init
railway up
```

**DigitalOcean App Platform:**
- Connect GitHub repo
- Set environment variables
- Deploy!

---

## 📊 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Try endpoints directly from browser
  - Auto-generated from code

- **ReDoc**: http://localhost:8000/redoc
  - Beautiful API documentation
  - Detailed schema information

---

## 🧪 Testing

### Automated Tests

```bash
# Run full test suite
python api/test_api.py
```

Tests include:
- ✅ Health check
- ✅ User registration
- ✅ User login
- ✅ JWT token validation
- ✅ Protected endpoint access
- ✅ Item CRUD operations
- ✅ Unauthorized access blocking
- ✅ Invalid token rejection

### Manual Testing with Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `/auth/register` → Try it out
3. Register a user
4. Login via `/auth/login`
5. Copy the access token
6. Click "Authorize" button (top right)
7. Paste token and authenticate
8. Test protected endpoints!

---

## 🔄 Upgrading to Production Database

### PostgreSQL Setup

```bash
# Install dependencies
pip install sqlalchemy psycopg2-binary alembic

# Create database
createdb myapi

# Set database URL
export DATABASE_URL="postgresql://user:pass@localhost/myapi"
```

### SQLAlchemy Models

See commented code in `api/database.py` for SQL models.

### Run Migrations

```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

---

## 📝 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | Auto-generated |
| `DATABASE_URL` | Database connection string | None (uses in-memory) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `ALLOWED_ORIGINS` | CORS allowed origins | `["*"]` |

### Config File

Edit `api/config.py` for:
- Token expiration time
- CORS settings
- Database configuration
- API keys for external services

---

## 🎯 Next Steps

### Enhance Your API

1. **Add More Models**
   - Create new models in `models.py`
   - Add CRUD endpoints in `main.py`

2. **Implement Roles & Permissions**
   - Add role field to User model
   - Create permission decorators
   - Protect admin endpoints

3. **Add Rate Limiting**
   ```bash
   pip install slowapi
   ```

4. **Add Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

5. **Add Email Verification**
   - Send verification emails
   - Verify email on registration

6. **Add Refresh Tokens**
   - Longer-lived refresh tokens
   - Short-lived access tokens

7. **Add API Versioning**
   - `/api/v1/...`
   - `/api/v2/...`

---

## 🤝 Contributing

Feel free to:
- Add new features
- Fix bugs
- Improve documentation
- Optimize performance

---

## 📄 License

This project is open source and available under the MIT License.

---

## 💡 Tips & Tricks

### Generate Strong Passwords

```bash
openssl rand -base64 32
```

### Test Authentication Flow

```bash
# Register
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -d "username=john&password=SecurePass123" | jq -r '.access_token')

# Use token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth/me
```

### Monitor API Logs

```bash
tail -f logs/api.log
```

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 PID
```

### Module Not Found

```bash
# Make sure you're in the project root
cd /Users/nr/Documents/GitHub/main

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r api/requirements.txt
```

### Database Not Persisting

Check that `api/data/` directory exists and is writable.

---

## 📞 Support

For issues or questions:
1. Check the documentation
2. Run the test suite
3. Check API logs
4. Review error messages in Swagger UI

---

**Built with ❤️ using FastAPI**

🚀 **Happy Coding!**

