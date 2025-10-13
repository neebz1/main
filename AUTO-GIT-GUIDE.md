# 🤖 Autonomous Git - Automatic Commit & Push

Make your git repository fully autonomous! Changes are automatically committed and pushed without manual intervention.

---

## 🎯 What It Does

The Autonomous Git Watcher:
- ✅ **Monitors** your repository for changes
- ✅ **Auto-commits** changes with timestamps
- ✅ **Auto-pushes** to remote (GitHub)
- ✅ **Configurable** check intervals
- ✅ **Works with any branch** automatically

---

## 🚀 Quick Start

### Option 1: Command Line

```bash
# Start watching (checks every 5 minutes by default)
./start-auto-git.sh

# Custom interval (e.g., check every 2 minutes)
./start-auto-git.sh --interval 120

# Run once without continuous watching
./start-auto-git.sh --once

# Commit but don't push automatically
./start-auto-git.sh --no-push
```

### Option 2: Web Interface

1. Start the Cloud AI Builder:
   ```bash
   ./start-cloud-builder.sh
   ```

2. Open the web interface at http://localhost:7862

3. Go to **⚡ Quick Actions** tab

4. Find the **🤖 Autonomous Git** section

5. Click **🚀 Start Auto-Git**

---

## ⚙️ Configuration

The watcher creates a `.auto_git_config.json` file with these settings:

```json
{
  "enabled": true,
  "interval": 300,
  "auto_push": true,
  "commit_message_template": "Auto-commit: {timestamp}",
  "ignore_patterns": [
    "*.pyc",
    "__pycache__",
    ".DS_Store",
    "*.log",
    ".env",
    "venv/",
    ".cursor/",
    ".git/"
  ]
}
```

You can edit this file to customize behavior.

---

## 🎮 Usage Examples

### Development Mode (Fast Updates)
```bash
# Check every 1 minute
./start-auto-git.sh --interval 60
```

### Production Mode (Slower Updates)
```bash
# Check every 30 minutes
./start-auto-git.sh --interval 1800
```

### Local Development (No Push)
```bash
# Commit locally but don't push to remote
./start-auto-git.sh --no-push
```

### Manual Trigger
```bash
# Run once to commit current changes
python3 auto_git_watcher.py --once
```

---

## 📊 How It Works

1. **Watches** for file changes using `git status`
2. **Commits** changes with timestamp: `Auto-commit: 2025-10-13 18:22:40`
3. **Pushes** to the current branch automatically
4. **Repeats** at the configured interval

---

## 🔧 Advanced Usage

### Python API

```python
from auto_git_watcher import AutoGitWatcher

# Create watcher
watcher = AutoGitWatcher(
    project_dir="/path/to/repo",
    interval=300  # 5 minutes
)

# Start watching
watcher.watch()

# Or run once
if watcher.has_changes():
    watcher.commit_and_push()
```

### Custom Commit Messages

Edit `.auto_git_config.json`:

```json
{
  "commit_message_template": "🤖 Auto-update: {timestamp}"
}
```

---

## 🛡️ Safety Features

- ✅ Respects `.gitignore` patterns
- ✅ Additional ignore patterns in config
- ✅ Handles commit failures gracefully
- ✅ Automatic branch detection
- ✅ Timeout protection (30s max)

---

## 🎯 Use Cases

### 1. Development Workspace
Auto-sync changes across machines without manual commits.

### 2. Documentation Updates
Automatically push documentation changes as you write.

### 3. Configuration Management
Keep config files synced automatically.

### 4. Rapid Prototyping
Focus on coding, not git commands.

### 5. Team Collaboration
Ensure changes are always backed up and shared.

---

## 💡 Tips

1. **Set appropriate intervals**: Too frequent = lots of commits, too slow = risk of losing work
2. **Use descriptive config**: Customize commit message templates
3. **Test first**: Use `--once` to test before continuous watching
4. **Review commits**: Check `git log` periodically to ensure proper operation

---

## 🐛 Troubleshooting

### "Authentication failed"
- Set up SSH keys for GitHub: https://docs.github.com/en/authentication
- Or use a personal access token

### "Nothing to commit"
- Normal! Means no changes were detected

### Watcher not starting
```bash
# Check if Python dependencies are installed
pip3 install python-dotenv

# Verify git is configured
git config --list
```

---

## 🚨 Important Notes

⚠️ **Automatic commits** mean less control over commit messages. Use when:
- Working on personal projects
- Rapid prototyping
- Documentation
- Configuration files

❌ **Not recommended for**:
- Production code reviews
- Projects requiring detailed commit messages
- Collaborative work needing PR workflows

---

## 📝 Examples

### Example 1: Auto-backup Development Work
```bash
# Start watcher with 10-minute intervals
./start-auto-git.sh --interval 600
```

Result:
```
Auto-commit: 2025-10-13 10:00:00
Auto-commit: 2025-10-13 10:10:00
Auto-commit: 2025-10-13 10:20:00
```

### Example 2: Integration with Cloud AI Builder

The Cloud AI Builder can now:
1. Make changes to your code via AI
2. Automatically commit and push them
3. No manual intervention needed!

---

## 🎉 Summary

✅ **Fully autonomous git operations**  
✅ **Works from command line or web UI**  
✅ **Configurable intervals and behavior**  
✅ **Safe and reliable**  
✅ **Perfect for rapid development**

**Your git is now fully autonomous! 🚀**
