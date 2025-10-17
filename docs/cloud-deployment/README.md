# ☁️ Cloud Deployment Guide

Deploy your AI applications to various cloud platforms with automated setup.

---

## 🎯 What This Does

The Cloud AI Builder toolkit helps you:
- Deploy AI models to cloud platforms
- Automate infrastructure setup
- Manage deployments
- Scale applications
- Monitor performance

---

## 🚀 Quick Start

### Using Cloud AI Builder

```bash
# Launch the Cloud AI Builder
./start-cloud-builder.sh

# Opens web interface at localhost:7863
```

The builder provides:
- **Platform selection** (AWS, Azure, GCP, Railway, Render, Fly.io)
- **Automated deployment** (one-click deploy)
- **Configuration management** (environment variables, secrets)
- **Resource monitoring** (usage, costs, performance)

---

## 🌐 Supported Platforms

### 1. 🚂 Railway (Recommended for Beginners)

**Pros:**
- ✅ Very easy setup
- ✅ Free $5 credit
- ✅ Auto-deploy from GitHub
- ✅ Built-in databases
- ✅ Zero config needed

**Cons:**
- ❌ Limited free tier
- ❌ Can get expensive at scale

**Deploy:**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Deploy
railway up
```

**Or use web interface:**
1. Go to https://railway.app
2. Connect GitHub repo
3. Select repository
4. Auto-deploy!

### 2. 🎨 Render

**Pros:**
- ✅ Free tier (good limits)
- ✅ Auto-deploy from GitHub
- ✅ Managed databases available
- ✅ SSL certificates included

**Cons:**
- ❌ Slower cold starts on free tier
- ❌ Limited regions

**Deploy:**
1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service
4. Connect GitHub repo
5. Render auto-detects configuration
6. Deploy!

### 3. 🪁 Fly.io

**Pros:**
- ✅ Free allowance (3 VMs)
- ✅ Global deployment
- ✅ Fast edge network
- ✅ Good for production

**Cons:**
- ❌ More complex setup
- ❌ Command-line focused

**Deploy:**
```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
flyctl auth login

# 3. Launch app
flyctl launch

# 4. Set secrets
flyctl secrets set OPENROUTER_API_KEY=your-key

# 5. Deploy
flyctl deploy
```

### 4. ☁️ AWS (Advanced)

**Pros:**
- ✅ Most features
- ✅ Global infrastructure
- ✅ Highly scalable
- ✅ Extensive services

**Cons:**
- ❌ Complex pricing
- ❌ Steep learning curve
- ❌ Can be expensive

**Deploy with Elastic Beanstalk:**
```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize
eb init -p python-3.10 my-app

# 3. Create environment
eb create production

# 4. Deploy
eb deploy
```

### 5. ☁️ Google Cloud (Advanced)

**Pros:**
- ✅ Good AI/ML services
- ✅ Free tier
- ✅ Global network
- ✅ Kubernetes support

**Cons:**
- ❌ Complex pricing
- ❌ Learning curve

**Deploy with Cloud Run:**
```bash
# 1. Install gcloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. Deploy
gcloud run deploy my-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 6. ☁️ Azure (Advanced)

**Pros:**
- ✅ Enterprise features
- ✅ Good Windows support
- ✅ Integrated services

**Cons:**
- ❌ Complex interface
- ❌ Pricing can be confusing

**Deploy with App Service:**
```bash
# 1. Install Azure CLI
# Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# 2. Login
az login

# 3. Create app
az webapp up --name my-app --runtime "PYTHON:3.10"
```

---

## 📦 Deployment Configurations

### For Gradio Apps (Music AI, ChatGPT, etc.)

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

**requirements.txt:**
```txt
gradio==4.0.0
# Add your other dependencies
```

**app.py adjustments:**
```python
import gradio as gr

# Your app code...

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,        # Standard port
        share=False              # Don't create ngrok tunnel
    )
```

### Environment Variables

**Railway/Render:** Set in web dashboard  
**Fly.io:** `flyctl secrets set KEY=value`  
**Heroku:** `heroku config:set KEY=value`  
**Docker:** Use `.env` file or `-e` flag

---

## 🔧 Using Cloud AI Builder

The `cloud_ai_builder.py` tool provides a GUI for cloud deployment:

```bash
# Launch the builder
./start-cloud-builder.sh
```

### Features:

1. **Platform Selection**
   - Choose from 6+ platforms
   - See pros/cons for each
   - Get cost estimates

2. **Configuration Builder**
   - Set environment variables
   - Configure resources (CPU, RAM, GPU)
   - Set scaling rules

3. **Deployment Automation**
   - One-click deployment
   - Automated setup scripts
   - Progress monitoring

4. **Management Tools**
   - View logs
   - Monitor resources
   - Update deployments
   - Roll back changes

---

## 💡 Deployment Best Practices

### 1. Start Small
- Deploy to free tier first
- Test thoroughly
- Monitor costs
- Scale gradually

### 2. Use Environment Variables
- Never hardcode secrets
- Use platform secret management
- Rotate keys regularly
- Keep .env in .gitignore

### 3. Implement Health Checks
```python
@app.route("/health")
def health():
    return {"status": "healthy"}
```

### 4. Add Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("App started")
```

### 5. Monitor Performance
- Set up alerts
- Track response times
- Monitor error rates
- Check resource usage

### 6. Plan for Scaling
- Use auto-scaling when available
- Implement caching
- Optimize database queries
- Use CDN for static assets

---

## 💰 Cost Comparison

### Free Tiers (Good for Personal Projects)

| Platform | Free Tier | Limits |
|----------|-----------|--------|
| **Railway** | $5 credit/month | 500 hours |
| **Render** | Unlimited | 750 hours/month |
| **Fly.io** | 3 VMs | Shared CPU |
| **Heroku** | 1000 hours | Sleeps after 30min |
| **Vercel** | Unlimited | Fair use |

### Paid Plans (For Production)

| Platform | Starting Price | Good For |
|----------|---------------|----------|
| **Railway** | Pay-as-you-go | Small apps |
| **Render** | $7/month | Side projects |
| **Fly.io** | ~$10/month | Production apps |
| **AWS** | ~$15/month | Enterprise |
| **GCP** | ~$15/month | ML workloads |

---

## 🚀 Deployment Checklist

Before deploying:
- [ ] Test locally thoroughly
- [ ] Create requirements.txt
- [ ] Add health check endpoint
- [ ] Set up logging
- [ ] Configure environment variables
- [ ] Add error handling
- [ ] Create Dockerfile (if needed)
- [ ] Set up .gitignore
- [ ] Test with production data
- [ ] Plan for database (if needed)

After deploying:
- [ ] Verify app loads
- [ ] Test all features
- [ ] Check logs for errors
- [ ] Set up monitoring
- [ ] Configure auto-scaling (if available)
- [ ] Set up backups
- [ ] Document deployment process
- [ ] Share URL with users

---

## 🔒 Security Considerations

### 1. API Keys & Secrets
- Use platform secret management
- Never commit to Git
- Rotate regularly
- Use separate keys for dev/prod

### 2. HTTPS
- Enable SSL/TLS
- Most platforms provide this free
- Redirect HTTP to HTTPS

### 3. Authentication
```python
# Add basic auth to Gradio
demo.launch(auth=("username", "password"))
```

### 4. Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.route("/api")
@limiter.limit("10/minute")
def api():
    return {"data": "..."}
```

### 5. Input Validation
```python
def process_input(user_input):
    # Sanitize and validate
    if not user_input or len(user_input) > 1000:
        raise ValueError("Invalid input")
    return sanitize(user_input)
```

---

## 🆘 Troubleshooting

### Build Failures
- Check requirements.txt
- Verify Python version
- Check for missing dependencies
- Review build logs

### Runtime Errors
- Check application logs
- Verify environment variables
- Test locally first
- Check resource limits

### Performance Issues
- Monitor resource usage
- Implement caching
- Optimize code
- Upgrade plan if needed

### Connection Issues
- Verify port configuration
- Check firewall rules
- Ensure health checks pass
- Review network settings

---

## 📚 Platform-Specific Guides

### Railway Deployment
See: `CursorDocsIndex/DEPLOY-GUIDE.md` section on Railway

### Render Deployment
See: `CursorDocsIndex/DEPLOY-GUIDE.md` section on Render

### Fly.io Deployment
See: `CursorDocsIndex/DEPLOY-GUIDE.md` section on Fly.io

### Heroku Alternative (2024+)
Heroku removed free tier. Use Railway or Render instead.

---

## 🎯 Recommended Platform by Use Case

| Use Case | Recommended Platform | Why |
|----------|---------------------|-----|
| **Personal project** | Railway or Render | Easy + free tier |
| **Demo/Portfolio** | Render or Fly.io | Free + reliable |
| **Production app** | Fly.io or Railway | Good performance |
| **Enterprise** | AWS or GCP | Features + scale |
| **ML inference** | GCP or AWS | GPU support |
| **Quick test** | Hugging Face Spaces | Fastest to deploy |

---

## 🚀 Quick Deploy Commands

### Railway
```bash
railway init && railway up
```

### Render
```bash
# Push to GitHub, then deploy via web UI
git push origin main
```

### Fly.io
```bash
flyctl launch && flyctl deploy
```

### Docker (Local)
```bash
docker build -t my-app .
docker run -p 7860:7860 my-app
```

---

**Made with ❤️ for developers who want hassle-free cloud deployment!**
