# 🆘 TROUBLESHOOTING GUIDE - "You're My Only Hope"

**Last Updated:** October 13, 2025  
**When nothing else works, try this!**

---

## 🚨 EMERGENCY FIX - Run This First!

If everything seems broken, run the emergency fix script:

```bash
cd /home/runner/work/main/main
./fix-everything.sh
```

This will:
✅ Check and install all Python dependencies  
✅ Verify API keys are configured  
✅ Test all three AI tools  
✅ Generate a status report  
✅ Create missing directories  

---

## 🎯 Common Issues & Solutions

### Issue 1: "No API key found" Error

**Problem:** Apps start but AI features don't work

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If missing, create it:
cp config_example.txt .env

# Add your API keys to .env:
nano .env
# or
vim .env
```

**What to add to .env:**
```
TOGETHER_API_KEY=your_kimi_k2_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here
GEMINI_API_KEY=your_google_key_here
```

---

### Issue 2: "Module not found" Errors

**Problem:** Python can't find required packages

**Solution:**
```bash
# Install ALL dependencies at once
pip3 install gradio together python-dotenv anthropic openai librosa matplotlib numpy pillow soundfile

# Or use requirements file
pip3 install -r requirements.txt
```

---

### Issue 3: Logic Pro Copilot Won't Start

**Problem:** Running `./start-music-ai.sh` gives errors

**Solution:**
```bash
# Try running directly (bypasses venv issues)
python3 logic_copilot_lite.py

# If that fails, reinstall dependencies
pip3 install --upgrade gradio together python-dotenv
python3 logic_copilot_lite.py
```

---

### Issue 4: AI Mixing Engineer Won't Start

**Problem:** Running `./start-ai-mixing-engineer.sh` gives errors

**Solution:**
```bash
# Install audio processing dependencies
pip3 install librosa soundfile matplotlib numpy pillow

# Then try running directly
python3 ai_mixing_engineer.py
```

---

### Issue 5: Port Already in Use

**Problem:** "Address already in use" error

**Solution:**
```bash
# Check what's using the ports
lsof -i :7860
lsof -i :7861

# Kill the process (replace PID with actual number)
kill -9 PID

# Or use different ports by editing the script
```

---

### Issue 6: Virtual Environment Issues

**Problem:** Can't activate venv or venv is broken

**Solution:**
```bash
# Remove broken venv
rm -rf venv

# Create new one
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Issue 7: "Cannot connect to localhost"

**Problem:** Browser opens but page won't load

**Solution:**
1. Check if the app is actually running (look for "Running on local URL" in terminal)
2. Try accessing directly: http://127.0.0.1:7860
3. Check if firewall is blocking the connection
4. Try a different browser

---

### Issue 8: AI Responses Are Slow or Timing Out

**Problem:** AI takes forever to respond or gives timeout errors

**Solution:**
1. **Check your API credits:**
   - Kimi K2: Check balance at https://platform.moonshot.cn
   - OpenAI: Check at https://platform.openai.com/usage
   - Anthropic: Check at https://console.anthropic.com

2. **Try switching providers** in .env:
   ```
   # Comment out one, uncomment another
   # TOGETHER_API_KEY=...
   OPENAI_API_KEY=your_key
   ```

---

### Issue 9: Permission Denied on Scripts

**Problem:** Can't run .sh scripts

**Solution:**
```bash
# Make all scripts executable
chmod +x start-*.sh
chmod +x fix-everything.sh

# Then run them
./start-music-ai.sh
```

---

### Issue 10: "I have no idea what's wrong!"

**Solution:**
```bash
# Run the diagnostic tool
python3 help.py

# This will:
# - Check all dependencies
# - Verify API keys
# - Test each tool
# - Give you a full report
```

---

## 🎵 Quick Test Commands

**Test Logic Pro Copilot:**
```bash
python3 -c "import gradio; import together; print('✅ Logic Pro Copilot dependencies OK')"
python3 logic_copilot_lite.py
```

**Test AI Mixing Engineer:**
```bash
python3 -c "import librosa; import matplotlib; print('✅ Mixing Engineer dependencies OK')"
python3 ai_mixing_engineer.py
```

**Test Live AI Assistant:**
```bash
python3 -c "import google.generativeai; print('✅ Live Assistant dependencies OK')"
python3 live_ai_assistant.py
```

---

## 🔍 Debug Mode

Run any script with verbose output:
```bash
python3 -u logic_copilot_lite.py 2>&1 | tee debug.log
```

This saves all output to `debug.log` for troubleshooting.

---

## 🚀 Fresh Start (Nuclear Option)

If nothing works, start completely fresh:

```bash
# 1. Backup your .env file
cp .env .env.backup

# 2. Remove everything
rm -rf venv
pip3 uninstall -y gradio together anthropic openai librosa matplotlib numpy pillow soundfile

# 3. Reinstall from scratch
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Restore .env
cp .env.backup .env

# 5. Test
python3 logic_copilot_lite.py
```

---

## 💡 Still Stuck?

1. **Check the logs:** Look for error messages in the terminal output
2. **Run diagnostics:** `python3 help.py`
3. **Emergency fix:** `./fix-everything.sh`
4. **Start simple:** Try running just `python3 logic_copilot_lite.py` without the shell script

---

## 🎯 Success Checklist

When everything is working, you should see:

✅ Logic Pro Copilot: http://localhost:7860  
✅ AI Mixing Engineer: http://localhost:7861  
✅ Live AI Assistant: Running in terminal  
✅ No "API key not found" warnings  
✅ AI responses working  
✅ File uploads working (Mixing Engineer)  

---

## 📞 Common Error Messages Decoded

| Error Message | What It Means | Solution |
|---------------|---------------|----------|
| "No module named 'gradio'" | Gradio not installed | `pip3 install gradio` |
| "No API key found" | Missing .env file or empty keys | Create/edit .env file |
| "Address already in use" | Port is occupied | Kill existing process or change port |
| "Connection refused" | App isn't running | Check terminal for startup errors |
| "Rate limit exceeded" | Out of API credits | Check API usage/credits |
| "Invalid API key" | Wrong or expired key | Verify key in .env file |

---

**Remember:** You're not alone! This suite has three powerful tools that all work independently. If one fails, the others still work! 🎵✨

**Pro Tip:** Always run `python3 help.py` first to get a full system status report.
