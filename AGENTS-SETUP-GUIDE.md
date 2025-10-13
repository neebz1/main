# 🤖 Autonomous Agents Setup Guide

## ✅ What's Been Created

You now have **3 autonomous agents** that automatically deploy and manage all your AI services using Bitwarden credentials:

### 1. **Deployment Agent** (`agents/deployment_agent.py`)
- Loads API keys from Bitwarden
- Deploys all local AI services
- Monitors and auto-restarts failed services

### 2. **Cloud Agent** (`agents/cloud_agent.py`)
- Deploys services to Railway
- Manages cloud infrastructure
- Handles environment variables

### 3. **Monitoring Agent** (`agents/monitoring_agent.py`)
- Health checks every 30 seconds
- Auto-heals crashed services
- Logs all events

---

## 🚀 How to Launch Agents

### **Method 1: Using Cursor Tasks (EASIEST)**

1. Open this project in Cursor
2. Press `Cmd+Shift+P`
3. Type: "Tasks: Run Task"
4. Select: **🚀 Launch ALL Agents**

This will open 3 terminals with all agents running!

### **Method 2: Using Terminal Profiles**

1. Open new terminal in Cursor
2. Click the dropdown arrow next to "+"
3. Select terminal profile:
   - `deployment-agent` 🤖
   - `cloud-agent` ☁️
   - `monitoring-agent` 👁️

### **Method 3: Manual Launch**

```bash
# Terminal 1 - Deployment Agent
source ~/.zshrc && bwload
python3 agents/deployment_agent.py

# Terminal 2 - Cloud Agent (new terminal)
source ~/.zshrc && bwload
python3 agents/cloud_agent.py

# Terminal 3 - Monitoring Agent (new terminal)
source ~/.zshrc && bwload
python3 agents/monitoring_agent.py
```

### **Method 4: One-Click Script**

```bash
./launch-agents.sh
```

---

## 🎯 What Each Agent Does

### **Deployment Agent**

Automatically:
1. Loads API keys from Bitwarden
2. Starts AI Mixing Engineer (port 7861)
3. Starts Music Copilot (port 7860)
4. Starts Live AI Assistant
5. Starts Logic AI Plugin
6. Monitors all services
7. Restarts any that crash

### **Cloud Agent**

Automatically:
1. Installs Railway CLI if needed
2. Deploys CursorDocsIndex to Railway
3. Sets up environment variables
4. Returns deployment URLs

### **Monitoring Agent**

Automatically:
1. Checks service health every 30 seconds
2. Detects down services
3. Auto-restarts failed services
4. Logs all events to `agents/monitoring.log`

---

## 📊 What You'll See

### Deployment Agent Output:
```
🤖 AUTONOMOUS DEPLOYMENT AGENT
Deploying all AI services...
============================================================

🔐 Loading credentials from Bitwarden...
✅ Loaded 6 API keys

🚀 Deploying AI Mixing Engineer...
✅ AI Mixing Engineer started (PID: 12345)
   URL: http://localhost:7861

🚀 Deploying Music Copilot...
✅ Music Copilot started (PID: 12346)
   URL: http://localhost:7860

============================================================
✅ Deployment complete!
============================================================

📊 Service Status:
------------------------------------------------------------
🟢 Running AI Mixing Engineer
         → http://localhost:7861
🟢 Running Music Copilot
         → http://localhost:7860
------------------------------------------------------------

👁️ Monitoring services...
Press Ctrl+C to stop
```

### Monitoring Agent Output:
```
👁️ AUTONOMOUS MONITORING AGENT
Monitoring all services...
============================================================

Press Ctrl+C to stop

🔍 Checking services... [14:30:15]
  🟢 AI Mixing Engineer: OK
  🟢 Music Copilot: OK

⏳ Next check in 30 seconds...
```

---

## 🔧 Configuration

All configured in `.vscode/settings.json` and `.vscode/tasks.json`:

- ✅ Terminal automation enabled
- ✅ Custom terminal profiles for each agent
- ✅ Cursor tasks for one-click launch
- ✅ Background execution
- ✅ Dedicated panels

---

## 🎮 Commands Reference

### Start All Agents:
```bash
# In Cursor
Cmd+Shift+P → Tasks: Run Task → 🚀 Launch ALL Agents
```

### Start Individual Agent:
```bash
# Deployment Agent
python3 agents/deployment_agent.py

# Cloud Agent
python3 agents/cloud_agent.py

# Monitoring Agent
python3 agents/monitoring_agent.py
```

### Stop All Services:
```
Press Ctrl+C in the Deployment Agent terminal
```

### View Logs:
```bash
tail -f agents/monitoring.log
```

---

## 🔄 How Auto-Recovery Works

1. **Monitoring Agent** checks services every 30 seconds
2. If service is down (HTTP check fails):
   - Logs the event
   - Runs the service's start script
   - Waits 5 seconds
   - Confirms service is back up
3. If restart fails:
   - Logs failure
   - Continues monitoring
   - Will retry on next check

---

## 💡 Pro Tips

### Keep Agents Running 24/7:
Use `tmux` or `screen` to run agents in background:
```bash
tmux new -s agents
python3 agents/deployment_agent.py
# Detach with Ctrl+B then D
```

### Check Service Status:
```bash
curl http://localhost:7861/health  # AI Mixing Engineer
curl http://localhost:7860/health  # Music Copilot
```

### Add More Services:
Edit `agents/deployment_agent.py`:
```python
services_to_deploy = [
    ("My New Service", "start-my-service.sh", 8000),
]
```

---

## 🛠 Troubleshooting

### Agents won't start:
```bash
# Make sure Bitwarden is unlocked
source ~/.zshrc
bwload

# Check if agents are executable
chmod +x agents/*.py
```

### Services not deploying:
```bash
# Check start scripts exist
ls -la start-*.sh

# Make them executable
chmod +x start-*.sh
```

### Bitwarden credentials not loading:
```bash
# Test manually
source ~/.zshrc
bwload
echo $GOOGLE_API_KEY  # Should show your key
```

---

## 🎉 You're All Set!

Your autonomous agents are ready to:
- ✅ Automatically load credentials from Bitwarden
- ✅ Deploy all services with one command
- ✅ Monitor services 24/7
- ✅ Auto-heal crashed services
- ✅ Run in Cursor terminals

**To start:** Press `Cmd+Shift+P` → Tasks: Run Task → 🚀 Launch ALL Agents

---

**Made with 🤖 for Noah**
Your AI services are now fully autonomous!

