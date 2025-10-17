# 🤗 Hugging Face Deployment Guide

Deploy your AI models to Hugging Face for free cloud hosting and sharing.

---

## 🎯 What This Does

This toolkit allows you to:
- Deploy AI models to Hugging Face Spaces
- Host web interfaces for your models
- Share your AI tools publicly or privately
- Get free GPU inference
- No server management required

---

## 🚀 Quick Start

### Prerequisites
- Hugging Face account (free at https://huggingface.co)
- Hugging Face API token
- Git installed
- Python 3.8+

### 1. Get Your Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it (e.g., "deployment-token")
4. Select "write" permission
5. Copy the token
6. Add to your .env file:
   ```
   HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxx
   ```

### 2. Choose What to Deploy

You can deploy:
- **Music AI tools** (Logic Copilot, AI Mixing Engineer)
- **ChatGPT-trained models** (your custom chatbot)
- **Cloud AI Builder apps**
- **Any Gradio/Streamlit app**

### 3. Deploy Your First App

```bash
# Example: Deploy Music Copilot
python3 app.py --deploy

# Or use the deployment script
# (Create one based on the templates below)
```

---

## 📋 Deployment Methods

### Method 1: Hugging Face CLI (Recommended)

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login
# Enter your token

# Create a new Space
huggingface-cli repo create --type=space --space_sdk=gradio my-music-ai

# Clone the Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/my-music-ai
cd my-music-ai

# Add your files
cp /path/to/logic_copilot_lite.py app.py
cp /path/to/requirements_lite.txt requirements.txt

# Create README.md with Space metadata
cat > README.md << 'EOF'
---
title: My Music AI
emoji: 🎵
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# My Music AI

AI-powered music production assistant.
EOF

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Method 2: Web Interface

1. Go to https://huggingface.co/new-space
2. Choose Space name
3. Select SDK (Gradio or Streamlit)
4. Create Space
5. Upload files via web interface
6. Space will automatically deploy

### Method 3: GitHub Integration

1. Push your code to GitHub
2. Go to Hugging Face → New Space
3. Select "Import from GitHub"
4. Connect your repository
5. Automatic deployment on every push

---

## 🎵 Deploying Music AI Tools

### Deploy Logic Pro Copilot

1. **Prepare the app:**
   ```bash
   # Create deployment directory
   mkdir hf-music-copilot
   cd hf-music-copilot
   
   # Copy files
   cp /path/to/logic_copilot_lite.py app.py
   cp /path/to/requirements_lite.txt requirements.txt
   ```

2. **Create Space config:**
   ```yaml
   # README.md
   ---
   title: Logic Pro Copilot
   emoji: 🎵
   colorFrom: blue
   colorTo: purple
   sdk: gradio
   sdk_version: 4.0.0
   app_file: app.py
   pinned: false
   ---
   
   # Logic Pro Copilot
   AI music production assistant for Logic Pro.
   ```

3. **Add secrets:**
   - Go to Space Settings → Variables and secrets
   - Add your API keys:
     - `OPENROUTER_API_KEY`
     - `MOONSHOT_API_KEY`
   - These will be available as environment variables

4. **Deploy:**
   ```bash
   huggingface-cli repo create --type=space --space_sdk=gradio logic-copilot
   git clone https://huggingface.co/spaces/YOUR_USERNAME/logic-copilot
   cd logic-copilot
   # Copy files here
   git add .
   git commit -m "Deploy Logic Pro Copilot"
   git push
   ```

### Deploy AI Mixing Engineer

Same process, but use:
- `ai_mixing_engineer.py` → `app.py`
- `requirements_mixing.txt` → `requirements.txt`

---

## 🤖 Deploying ChatGPT-Trained Models

### Option A: Model + Interface

```bash
# 1. Upload your trained model to Hugging Face Models
huggingface-cli repo create my-chatbot --type=model

# 2. Upload model files
cd trained_model
git clone https://huggingface.co/YOUR_USERNAME/my-chatbot
cd my-chatbot
cp -r ../model_files/* .
git add .
git commit -m "Upload trained model"
git push

# 3. Create Space with chat interface
huggingface-cli repo create --type=space --space_sdk=gradio my-chatbot-demo
cd ../
git clone https://huggingface.co/spaces/YOUR_USERNAME/my-chatbot-demo
cd my-chatbot-demo

# 4. Create app.py that loads your model
cat > app.py << 'EOF'
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "YOUR_USERNAME/my-chatbot"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def chat(message, history):
    # Your chat logic here
    inputs = tokenizer(message, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

demo = gr.ChatInterface(chat)
demo.launch()
EOF

git add .
git commit -m "Deploy chatbot"
git push
```

### Option B: API-Based (No Model Upload)

If your model is too large or you want to run it locally:

```python
# app.py for Hugging Face Space
import gradio as gr
import requests
import os

# Your local API endpoint
API_URL = os.getenv("API_URL")  # Set in Space secrets

def chat(message, history):
    response = requests.post(API_URL, json={"message": message})
    return response.json()["response"]

demo = gr.ChatInterface(chat)
demo.launch()
```

Then run your model locally and expose via ngrok/tunneling.

---

## ☁️ Deploying Cloud AI Builder

```bash
# Deploy the cloud builder interface
mkdir hf-cloud-builder
cd hf-cloud-builder

cp /path/to/cloud_ai_builder.py app.py
cp /path/to/requirements.txt requirements.txt

# Create README.md
cat > README.md << 'EOF'
---
title: Cloud AI Builder
emoji: ☁️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
---

# Cloud AI Builder
Build and deploy AI models to the cloud.
EOF

# Deploy
huggingface-cli repo create --type=space --space_sdk=gradio cloud-ai-builder
git clone https://huggingface.co/spaces/YOUR_USERNAME/cloud-ai-builder
cd cloud-ai-builder
# Copy files
git add .
git commit -m "Deploy Cloud AI Builder"
git push
```

---

## 🔧 Configuration & Best Practices

### Space Configuration (README.md metadata)

```yaml
---
title: Your App Name              # Display name
emoji: 🎵                         # Icon
colorFrom: blue                   # Gradient start color
colorTo: purple                   # Gradient end color
sdk: gradio                       # gradio or streamlit
sdk_version: 4.0.0                # SDK version
app_file: app.py                  # Entry point
pinned: false                     # Pin to profile
license: mit                      # License type
python_version: 3.10              # Python version
---
```

### Hardware Selection

Free tiers:
- **CPU Basic:** Default, good for most apps
- **CPU Upgrade:** 4 cores, more RAM

Paid tiers (billed by hour):
- **GPU T4:** $0.60/hour - Good for inference
- **GPU A10G:** $3.15/hour - Better performance
- **GPU A100:** $4.13/hour - Best performance

Set in Space Settings → Hardware

### Requirements.txt Best Practices

```txt
# Pin versions for reproducibility
gradio==4.0.0
transformers==4.35.0
torch==2.1.0
numpy==1.24.0

# Avoid unnecessary dependencies
# Only include what you actually use
```

### Environment Variables & Secrets

Go to Space Settings → Variables and secrets:
- Use secrets for API keys
- Use variables for configuration
- Never commit secrets to git

---

## 💡 Optimization Tips

### 1. Reduce Loading Time
- Use model caching
- Load models on Space startup
- Use smaller models when possible
- Enable model sharding for large models

### 2. Improve Performance
- Use GPU Spaces for ML inference
- Implement request batching
- Cache frequent queries
- Optimize model quantization

### 3. Better UX
- Add loading indicators
- Show example inputs
- Include clear instructions
- Handle errors gracefully

### 4. Cost Optimization
- Use CPU for simple apps
- Implement auto-sleep for paid GPUs
- Cache static resources
- Optimize model size

---

## 🔒 Privacy & Security

### Public vs Private Spaces

**Public Spaces:**
- Free forever
- Visible to everyone
- Good for demos and sharing

**Private Spaces:**
- Requires paid plan ($9/month)
- Only you can access
- Good for personal tools with sensitive data

### Security Best Practices

1. **Never commit secrets**
   - Use Space secrets for API keys
   - Add `.env` to `.gitignore`

2. **Validate user input**
   - Sanitize all inputs
   - Rate limit requests
   - Handle malicious queries

3. **Protect API endpoints**
   - Add authentication if needed
   - Use HTTPS only
   - Monitor usage

---

## 📊 Monitoring & Analytics

### Built-in Metrics
- View count
- User interactions
- Error logs

Access in Space → Analytics

### Custom Analytics

```python
# Add to your app.py
import gradio as gr

def analytics_callback(data):
    # Log interactions
    print(f"User input: {data}")
    
demo = gr.Interface(...)
demo.launch(analytics_enabled=True)
```

---

## 🆘 Troubleshooting

### "Build failed" Error
- Check requirements.txt for typos
- Ensure all dependencies are available on PyPI
- Verify Python version compatibility
- Check Space logs for details

### "Out of memory" Error
- Use smaller models
- Reduce batch size
- Upgrade to larger hardware tier
- Implement model quantization

### App Not Loading
- Check app.py for syntax errors
- Verify all imports are in requirements.txt
- Check Space logs
- Test locally first

### Slow Performance
- Upgrade to GPU Space
- Optimize model loading
- Use model caching
- Reduce model size

---

## 📁 Example Deployment Structure

```
my-huggingface-space/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── README.md                 # Space config + description
├── .gitignore               # Ignore .env, cache, etc.
├── examples/                # Example inputs
│   ├── example1.txt
│   └── example2.txt
└── models/                  # Optional: local models
    └── model.pkl
```

---

## 🎯 Success Checklist

Before deploying:
- [ ] Test locally thoroughly
- [ ] Create requirements.txt with pinned versions
- [ ] Add proper README.md with metadata
- [ ] Set up secrets for API keys
- [ ] Add .gitignore for sensitive files
- [ ] Test with example inputs
- [ ] Add error handling
- [ ] Optimize for performance

After deploying:
- [ ] Verify Space loaded successfully
- [ ] Test all functionality
- [ ] Check logs for errors
- [ ] Monitor usage
- [ ] Share with others!

---

## 🚀 Next Steps

1. **Deploy your first Space** (start with something simple)
2. **Monitor and iterate** (watch logs, fix issues)
3. **Add features** (improve based on feedback)
4. **Share** (post on Twitter, HN, Reddit)
5. **Scale** (upgrade hardware if needed)

---

## 📚 Additional Resources

- **Hugging Face Spaces:** https://huggingface.co/spaces
- **Gradio Docs:** https://gradio.app/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Example Spaces:** https://huggingface.co/spaces/gradio

---

**Made with ❤️ for AI builders who want to share their creations!**
