# ⚡ REST API - Quick Start Guide

## 🚀 Start the API (One Command!)

```bash
./start-api.sh
```

That's it! Your API is now running at:
- 🌐 **API**: http://localhost:8000
- 📚 **Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Test the API (One Command!)

In another terminal:

```bash
python api/test_api.py
```

This runs a complete test suite that:
1. ✅ Checks API health
2. ✅ Registers a test user
3. ✅ Logs in and gets JWT token
4. ✅ Creates items
5. ✅ Tests authentication
6. ✅ Verifies security

---

## 📝 Try It Yourself (Interactive UI)

1. Open http://localhost:8000/docs in your browser
2. Click on `/auth/register` → "Try it out"
3. Enter user details:
   ```json
   {
     "username": "yourname",
     "email": "you@example.com",
     "password": "SecurePass123",
     "full_name": "Your Name"
   }
   ```
4. Click "Execute"
5. Go to `/auth/login` → "Try it out"
6. Enter username and password
7. Copy the `access_token` from response
8. Click 🔓 "Authorize" button (top right)
9. Paste token, click "Authorize"
10. Now test any protected endpoint!

---

## 🎯 Common Commands

### Register a User (curl)

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

### Login & Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=john_doe&password=SecurePass123"
```

### Use Token (Get User Info)

```bash
# Replace YOUR_TOKEN with actual token from login
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create an Item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Item",
    "description": "Item description"
  }'
```

---

## 🔒 Authentication Flow

```
1. Register User → /auth/register
2. Login → /auth/login → Get JWT Token
3. Use Token → Authorization: Bearer <token>
4. Access Protected Endpoints → /items, /auth/me, etc.
```

---

## 📊 What You Can Do

✅ Register users with validation
✅ Login with JWT authentication
✅ Create items (authenticated)
✅ View items (authenticated)
✅ Delete items (authenticated)
✅ View current user info
✅ List all users (admin)

---

## 🛠️ Project Structure

```
api/
├── main.py              # Main FastAPI app with all endpoints
├── models.py            # Data models (User, Item, Token)
├── auth.py              # JWT authentication logic
├── database.py          # Database management
├── config.py            # Configuration settings
├── requirements.txt     # Dependencies
├── test_api.py          # Test suite
└── data/
    └── db.json          # Auto-created database
```

---

## 🔥 Next Steps

1. **Customize the API**
   - Add your own models in `models.py`
   - Create endpoints in `main.py`

2. **Add Features**
   - Email verification
   - Password reset
   - User roles/permissions
   - File uploads

3. **Deploy to Production**
   - Set `SECRET_KEY` environment variable
   - Use PostgreSQL/MySQL
   - Deploy to Heroku/Railway/DigitalOcean

4. **Secure for Production**
   - Update CORS origins
   - Add rate limiting
   - Enable HTTPS only
   - Add logging

---

## 🆘 Troubleshooting

**Port already in use?**
```bash
lsof -ti:8000 | xargs kill -9
```

**Dependencies missing?**
```bash
source venv/bin/activate
pip install -r api/requirements.txt
```

**Can't connect?**
Make sure the API is running: `./start-api.sh`

---

## 📖 Full Documentation

See `API-README.md` for complete documentation.

---

**Built with FastAPI + JWT Authentication** 🚀

