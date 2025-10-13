# 🛡️ ERROR PREVENTION GUIDE

**Never have issues again. Follow these rules.**

---

## 🎯 The Golden Rules (Follow These = Zero Issues)

### Rule #1: Restart Cursor Weekly
```bash
# Every Monday morning:
⌘Q → Wait 5 seconds → Reopen Cursor
```
**Why?** Prevents memory leaks, cache issues, extension conflicts.

### Rule #2: Update Cursor Immediately
```bash
# When you see update notification:
Menu → Check for Updates → Install NOW
```
**Why?** Bug fixes, security patches, new features.

### Rule #3: Keep Extensions Minimal
```bash
# Only install what you NEED:
✅ Cline (AI agent)
✅ Language support (Python, JS, etc.)
❌ Everything else (unless essential)
```
**Why?** Extensions cause 80% of Cursor crashes.

### Rule #4: Never Commit .env to Git
```bash
# Always in .gitignore:
.env
*.env
```
**Why?** API keys exposed = security breach = disabled keys.

### Rule #5: Use ⌘K for Everything
```bash
# Don't fight the editor - let AI do it:
⌘K → "add error handling"
⌘K → "fix this bug"
⌘K → "make this faster"
```
**Why?** Fewer manual errors = fewer bugs.

---

## 🚫 Things That WILL Break Cursor

### ❌ DON'T: Install Random Extensions
- Every extension = potential crash
- Stick to essentials only
- Remove unused extensions monthly

### ❌ DON'T: Use Outdated Cursor
- Old versions have bugs
- Update notifications exist for a reason
- Auto-update is your friend

### ❌ DON'T: Keep Cursor Running for Weeks
- Restart every few days
- Or at least once a week
- Fresh start = fewer issues

### ❌ DON'T: Ignore Error Messages
- Read the error
- Search for it
- Fix it immediately
- Don't "just ignore it"

### ❌ DON'T: Modify Cursor Settings Randomly
- Know what you're changing
- Take screenshots before changes
- Can always reset: `rm ~/.cursor/settings.json`

---

## ✅ Things That PREVENT Issues

### ✅ DO: Keep Git Configured
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### ✅ DO: Keep API Keys in .env
```bash
# In your project root:
cat > .env << EOF
OPENROUTER_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
EOF
```

### ✅ DO: Use Version Control
```bash
git init
git add .
git commit -m "Initial commit"
```
**Why?** Can always roll back if something breaks.

### ✅ DO: Run Verification Monthly
```bash
./verify-setup.sh
```
**Why?** Catches issues before they become problems.

### ✅ DO: Keep a Settings Backup
```bash
# Backup your Cursor settings:
cp ~/.cursor/settings.json ~/cursor-settings-backup.json
```
**Why?** Can restore if settings get corrupted.

---

## 🔄 Weekly Maintenance Routine (5 Minutes)

### Every Monday:
```bash
# 1. Update Cursor
Menu → Check for Updates

# 2. Restart Cursor
⌘Q → Reopen

# 3. Test AI
⌘K → Type "hello" → Verify response

# 4. Check subscription
cursor.sh/settings → Verify active

# 5. Review extensions
⌘⇧X → Remove unused
```

**That's it. 5 minutes = Zero issues all week.**

---

## 🎯 Before Starting Any Project

### Pre-Flight Checklist:
```bash
[ ] Cursor is updated to latest version
[ ] Restarted Cursor fresh (⌘Q → reopen)
[ ] ⌘K works (tested it)
[ ] Git is configured (run: git config --list)
[ ] .env file exists (if using APIs)
[ ] Subscription/trial is active
[ ] No weird error messages
```

**All checked? You're good to code!**

---

## 🆘 Emergency Recovery Procedures

### If Cursor Won't Start:
```bash
# 1. Force quit
⌘⌥⎋ → Select Cursor → Force Quit

# 2. Clear cache
rm -rf ~/.cursor/CachedData

# 3. Restart Mac
🍎 → Restart

# 4. Reinstall Cursor (nuclear option)
rm -rf /Applications/Cursor.app
# Download fresh from cursor.sh
```

### If AI Stops Working:
```bash
# 1. Sign out and back in
⌘, → Account → Sign Out → Sign In

# 2. Check subscription
cursor.sh/settings → Verify payment

# 3. Reset AI settings
⌘, → Search "AI" → Reset to defaults

# 4. Restart Cursor
⌘Q → Reopen
```

### If Extensions Break Everything:
```bash
# 1. Disable all extensions
⌘⇧X → Disable All

# 2. Restart Cursor
⌘Q → Reopen

# 3. Enable one by one
⌘⇧X → Enable one → Test → Repeat
# Find the broken one

# 4. Remove broken extension
⌘⇧X → Uninstall problematic extension
```

### If Settings Are Corrupted:
```bash
# 1. Backup current (broken) settings
cp ~/.cursor/settings.json ~/broken-settings.json

# 2. Delete settings
rm ~/.cursor/settings.json

# 3. Restart Cursor
⌘Q → Reopen
# Cursor creates fresh default settings

# 4. Reconfigure manually
⌘, → Adjust settings as needed
```

---

## 📊 Issue Frequency Chart

**If you follow the Golden Rules:**
- 🟢 99% uptime, smooth experience
- 🟢 Minimal disruptions
- 🟢 Fast, reliable AI

**If you ignore prevention:**
- 🔴 Weekly crashes
- 🔴 Frequent errors
- 🔴 Frustration and wasted time

**Your choice is clear.**

---

## 💡 Pro Prevention Tips

### Tip #1: Keyboard Shortcuts = Fewer Errors
```
Use:      ⌘K, ⌘L, ⌘⇧P
Not:      Mouse clicking random buttons
```

### Tip #2: Let AI Do the Heavy Lifting
```
Use:      ⌘K → "refactor this function"
Not:      Manual editing (more typos)
```

### Tip #3: Keep Projects Organized
```
Good:     ~/projects/my-app/
Bad:      ~/Desktop/untitled folder 1/test.js
```

### Tip #4: One Project, One Window
```
Good:     Each project in separate Cursor window
Bad:      15 projects in one window (chaos)
```

### Tip #5: Close Files You're Not Using
```
Good:     ⌘W to close unused tabs
Bad:      50 tabs open (memory leak)
```

---

## 🎯 The Ultimate Prevention Formula

```
Update Weekly + Restart Weekly + Minimal Extensions = Zero Issues
```

**It's that simple.**

---

## 📚 Quick Reference

**Prevent issues:**
- Follow Golden Rules above
- Run weekly maintenance
- Use pre-flight checklist

**If issues happen:**
- Check TROUBLESHOOTING-FLOWCHART.txt
- Run ./verify-setup.sh
- Read ZERO-ISSUES-SETUP.md

**Emergency:**
- Force quit → Restart
- Disable extensions
- Reset settings
- Reinstall Cursor

---

## ✅ Success Story

**Before prevention:**
- "Cursor crashes all the time"
- "AI stopped working again"
- "Why is this so buggy?"
- Wasted hours fixing issues

**After prevention:**
- Cursor just works
- AI always available
- Zero interruptions
- 100% productive

**Choose your experience.**

---

**Remember:** 5 minutes of prevention > 1 hour of fixing.

Follow this guide. Never have issues again. 🚀
