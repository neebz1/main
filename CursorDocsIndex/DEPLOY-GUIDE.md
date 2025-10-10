# 🚀 Docs-Agent Cloud Deployment Guide

## ✅ What's Been Built for Cloud

Your Docs-Agent is now **cloud-ready** with:

- ✅ **FastAPI server** (`api_server.py`) - Production REST API
- ✅ **Docker support** (`Dockerfile`, `docker-compose.yml`)
- ✅ **Railway config** (`railway.json`)
- ✅ **Render config** (`render.yaml`)
- ✅ **Deployment script** (`deploy.sh`)
- ✅ **Test script** (`test-api.sh`)

---

## 🧪 Test Locally First (5 minutes)

### **Option A: Direct Python**

```bash
cd ~/CursorDocsIndex
source venv/bin/activate

# Start server
python api_server.py

# Server runs at: http://localhost:8000
# Swagger docs at: http://localhost:8000/docs
```

**In another terminal, test it:**
```bash
# Health check
curl http://localhost:8000/health

# Search
curl "http://localhost:8000/search?q=authentication"

# Lookup
curl "http://localhost:8000/lookup?q=POST%20requests"

# Stats
curl http://localhost:8000/stats
```

### **Option B: Docker (if you want to test containerized)**

```bash
cd ~/CursorDocsIndex

# Build image
docker build -t docs-agent-api .

# Run container
docker run -d -p 8000:8000 --name docs-agent-api docs-agent-api

# Test
curl http://localhost:8000/health

# Stop
docker stop docs-agent-api
docker rm docs-agent-api
```

---

## ☁️ Deploy to Cloud (Choose One)

### **🚂 Option 1: Railway (RECOMMENDED - Easiest)**

**Why Railway:**
- ✅ Free tier (500 hours/month)
- ✅ Auto HTTPS
- ✅ One-command deploy
- ✅ Built-in monitoring

**Steps:**

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Initialize project:**
   ```bash
   cd ~/CursorDocsIndex
   railway init
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

5. **Set environment variables:**
   ```bash
   # In Railway dashboard or via CLI:
   railway variables set DOCS_API_KEY=your-secret-key
   railway variables set OPENROUTER_API_KEY=your-openrouter-key
   ```

6. **Get your URL:**
   ```bash
   railway domain
   # Returns: https://your-project.railway.app
   ```

**Done!** Your API is live at: `https://your-project.railway.app`

---

### **🎨 Option 2: Render**

**Why Render:**
- ✅ Free tier
- ✅ Auto-deploy from GitHub
- ✅ Managed PostgreSQL available

**Steps:**

1. **Push to GitHub:**
   ```bash
   cd ~/CursorDocsIndex
   git init
   git add .
   git commit -m "Docs-Agent API"
   gh repo create docs-agent-api --private --source=. --push
   ```

2. **Go to Render:**
   - Visit: https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects `render.yaml`

3. **Deploy:**
   - Click "Create Web Service"
   - Wait ~5 minutes for build

4. **Set environment variables in Render dashboard:**
   - `DOCS_API_KEY`
   - `OPENROUTER_API_KEY`

**Done!** Your API is live at: `https://docs-agent-api.onrender.com`

---

### **🪁 Option 3: Fly.io**

**Why Fly.io:**
- ✅ Free allowance (3 shared-cpu VMs)
- ✅ Global deployment
- ✅ Fast edge network

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   flyctl auth login
   ```

3. **Launch:**
   ```bash
   cd ~/CursorDocsIndex
   flyctl launch
   # Answer prompts (will create fly.toml)
   ```

4. **Set secrets:**
   ```bash
   flyctl secrets set DOCS_API_KEY=your-secret-key
   flyctl secrets set OPENROUTER_API_KEY=your-openrouter-key
   ```

5. **Deploy:**
   ```bash
   flyctl deploy
   ```

**Done!** Your API is live at: `https://your-app.fly.dev`

---

### **🐳 Option 4: Your Own Server (VPS)**

**For DigitalOcean, AWS EC2, etc.:**

1. **SSH into your server:**
   ```bash
   ssh user@your-server.com
   ```

2. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

3. **Clone and deploy:**
   ```bash
   git clone https://github.com/your-username/docs-agent-api
   cd docs-agent-api
   
   # Set environment variables
   export DOCS_API_KEY=your-secret-key
   export OPENROUTER_API_KEY=your-key
   
   # Run with docker-compose
   docker-compose up -d
   ```

4. **Setup nginx reverse proxy (optional):**
   ```nginx
   server {
       listen 80;
       server_name docs.yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
       }
   }
   ```

---

## 🔐 Security Setup

### **Set API Key (Required for production):**

```bash
# Generate secure key
openssl rand -hex 32

# Set in deployment:
export DOCS_API_KEY=your-generated-key

# Or in .env file:
echo "DOCS_API_KEY=your-generated-key" > .env
```

### **Using the API with authentication:**

```bash
# Without auth (fails):
curl http://your-api.com/ingest

# With auth (works):
curl -H "X-API-Key: your-key" \
     -X POST http://your-api.com/ingest \
     -d '{"sources": ["https://docs.com/"]}'
```

---

## 📊 Using Your Cloud API

### **From Command Line:**

```bash
# Search
curl "https://your-api.railway.app/search?q=authentication&top_k=5"

# Lookup
curl "https://your-api.railway.app/lookup?q=OAuth2"

# Stats
curl "https://your-api.railway.app/stats"

# Ingest (requires API key)
curl -H "X-API-Key: your-key" \
     -X POST "https://your-api.railway.app/ingest" \
     -H "Content-Type: application/json" \
     -d '{"sources": ["https://fastapi.tiangolo.com/"]}'
```

### **From Python:**

```python
import requests

API_URL = "https://your-api.railway.app"

# Search
response = requests.get(f"{API_URL}/search", params={"q": "authentication"})
results = response.json()

# Lookup
response = requests.get(f"{API_URL}/lookup", params={"q": "OAuth2"})
result = response.json()
print(result['excerpt'])
```

### **From JavaScript/Browser:**

```javascript
// Search
const response = await fetch('https://your-api.railway.app/search?q=authentication');
const data = await response.json();
console.log(data.results);

// Lookup
const result = await fetch('https://your-api.railway.app/lookup?q=OAuth2');
const doc = await result.json();
console.log(doc.excerpt);
```

### **In Cursor AI (Manual):**

```
1. Lookup: curl "https://your-api.railway.app/lookup?q=topic"
2. Copy excerpt
3. Paste in Cursor: "Based on this doc: [excerpt]... write code"
```

---

## 🎯 Quick Deploy Commands

### **Railway (Fastest):**
```bash
cd ~/CursorDocsIndex
chmod +x deploy.sh
./deploy.sh
# Choose option 1
```

### **Render:**
```bash
cd ~/CursorDocsIndex
chmod +x deploy.sh
./deploy.sh
# Choose option 2
```

### **Docker Local:**
```bash
cd ~/CursorDocsIndex
chmod +x deploy.sh
./deploy.sh
# Choose option 3
```

---

## 📈 After Deployment

### **Your API endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/search` | GET | Search docs |
| `/lookup` | GET | Quick lookup |
| `/stats` | GET | Index statistics |
| `/documents` | GET | List all docs |
| `/ingest` | POST | Ingest new docs (requires auth) |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc UI |

### **Swagger Documentation:**
```
https://your-api.railway.app/docs
```

Interactive API documentation with "Try it out" buttons!

---

## 🔧 Configuration

### **Environment Variables:**

```bash
# Required
PORT=8000                     # Server port
INDEX_DIR=/app/index          # Index directory

# Optional
DOCS_API_KEY=your-secret-key  # API authentication
OPENROUTER_API_KEY=your-key   # For semantic search
OPENAI_API_KEY=your-key       # Alternative for semantic search
```

### **Railway:**
Set in dashboard or via CLI:
```bash
railway variables set DOCS_API_KEY=your-key
```

### **Render:**
Set in dashboard under "Environment" tab

### **Fly.io:**
```bash
flyctl secrets set DOCS_API_KEY=your-key
```

---

## 💡 Pro Tips

### **Pre-populate Index Before Deploy:**

```bash
# Index docs locally
source venv/bin/activate
python docs_cli.py ingest "https://fastapi.tiangolo.com/"
python docs_cli.py ingest "https://docs.python-requests.org/"

# The index/ directory will be included in deployment
```

### **Keep Index Updated:**

```bash
# From anywhere:
curl -H "X-API-Key: your-key" \
     -X POST "https://your-api.railway.app/ingest" \
     -H "Content-Type: application/json" \
     -d '{"sources": ["https://new-docs.com/"]}'
```

### **Monitor Usage:**

```bash
# Check stats
curl https://your-api.railway.app/stats

# List indexed docs
curl https://your-api.railway.app/documents
```

---

## 🎨 Integration Examples

### **Cursor Extension (Future):**

```typescript
// Custom Cursor extension
const docsAgent = {
  lookup: async (query: string) => {
    const response = await fetch(`https://your-api.com/lookup?q=${query}`);
    return await response.json();
  }
};

// Use in AI prompts
const context = await docsAgent.lookup("React hooks");
const prompt = `Using this documentation:\n${context.excerpt}\n\nWrite a custom hook...`;
```

### **CLI Wrapper:**

Add to `~/.zshrc`:
```bash
docs-cloud() {
    local query="$*"
    curl -s "https://your-api.railway.app/lookup?q=$query" | jq -r '.excerpt'
}
```

Usage:
```bash
docs-cloud "authentication patterns"
```

---

## 🐛 Troubleshooting

### **Server won't start:**
```bash
# Check logs
tail -f /tmp/docs-api-server.log

# Or with Docker:
docker logs docs-agent-api
```

### **401 Unauthorized:**
```bash
# Make sure to include API key:
curl -H "X-API-Key: your-key" http://your-api.com/ingest
```

### **No results found:**
```bash
# Check if docs are indexed:
curl http://your-api.com/stats

# Re-ingest if needed:
curl -H "X-API-Key: your-key" \
     -X POST http://your-api.com/ingest \
     -d '{"sources": ["https://docs.com/"]}'
```

---

## 📊 Deployment Comparison

| Platform | Setup Time | Free Tier | Auto-deploy | Monitoring |
|----------|-----------|-----------|-------------|------------|
| **Railway** | 5 min | ✅ 500h/mo | ✅ | ✅ |
| **Render** | 10 min | ✅ 750h/mo | ✅ | ✅ |
| **Fly.io** | 10 min | ✅ 3 VMs | ⚠️ Manual | ✅ |
| **Docker VPS** | 30 min | ❌ Paid | ❌ Manual | ⚠️ DIY |

**Recommendation: Railway** (easiest, auto-deploy, great free tier)

---

## 🎯 Next Steps

### **Immediate (Local Test):**

```bash
cd ~/CursorDocsIndex
chmod +x test-api.sh deploy.sh
./test-api.sh
```

Visit http://localhost:8000/docs to see Swagger UI!

### **Deploy to Cloud:**

```bash
./deploy.sh
# Choose platform (Railway recommended)
```

### **Use Your API:**

```bash
# Replace with your deployed URL
curl "https://your-api.railway.app/lookup?q=FastAPI+authentication"
```

---

## 🎉 You Now Have

**Local Mode:**
- ✅ Fast CLI (`python docs_cli.py`)
- ✅ Private & secure
- ✅ Instant search

**Cloud Mode:**
- ✅ REST API accessible anywhere
- ✅ Team can share
- ✅ Browser access
- ✅ CI/CD integration ready
- ✅ Beautiful Swagger docs

**Best of both worlds!** 🚀

---

**Ready to deploy? Run:**
```bash
cd ~/CursorDocsIndex
./deploy.sh
```

Choose Railway (option 1) for fastest setup! 🚂

