# 🚀 Auto-Approval Quick Reference

## What It Does

✅ Automatically approves safe operations:
- Documentation updates (*.md, *.txt)
- Configuration changes (*.yml, *.yaml)
- Patch/minor dependency updates
- Read-only commands (git status, ls, etc.)

⚠️ Requires manual approval for:
- Code modifications
- File deletions
- Major version updates
- Security changes

## Quick Start

### 1. Enable in Copilot Apps

```bash
# Start Logic Pro Copilot
python3 logic_copilot_lite.py

# OR start Cloud AI Builder
python3 cloud_ai_builder.py
```

Then navigate to "⚙️ Auto-Approval Settings" tab.

### 2. GitHub Actions (Already Configured!)

Auto-approval for:
- Dependabot PRs (patch/minor updates)
- Safe Copilot PRs (docs/config only)

Just enable in repository settings:
1. Settings → Actions → General
2. ✅ "Allow GitHub Actions to create and approve pull requests"

## Commands

### Toggle Auto-Approval

**Via UI:** Click "Toggle Auto-Approval" in settings tab

**Via Python:**
```python
from auto_approval import auto_approval
auto_approval.enable_auto_approval()   # Enable
auto_approval.disable_auto_approval()  # Disable
```

### Check Status

```bash
# View approval log
tail -20 .copilot_approvals.log

# Check if enabled
python3 -c "from auto_approval import auto_approval; print(auto_approval.config['enabled'])"
```

### Add Safe Patterns

```python
from auto_approval import auto_approval

# Add file pattern
auto_approval.add_safe_pattern("*.json")

# Add command
auto_approval.add_safe_command("npm test")
```

## Configuration File

**Location:** `.copilot_auto_approve.json`

**Quick edit:**
```bash
nano .copilot_auto_approve.json
```

**Example:**
```json
{
  "enabled": true,
  "safe_file_patterns": [
    "*.md", "*.txt", "*.yml"
  ],
  "safe_commands": [
    "git status", "ls", "cat"
  ]
}
```

## Monitoring

### View Stats in UI
1. Open copilot app
2. Go to "Auto-Approval Settings" tab
3. Click "Refresh Status"

### View GitHub Actions
1. Go to repository
2. Click "Actions" tab
3. View "Auto-Approve Notifications" runs

## Security

✅ **Safe (auto-approved):**
- README.md, docs/
- git status, git log
- Package patch updates

❌ **Unsafe (needs approval):**
- Python/JS code files
- rm, sudo commands
- Major version updates

## Troubleshooting

### Auto-Approval Not Working?

```python
# Check config
from auto_approval import auto_approval
print(auto_approval.config)

# Force enable
auto_approval.enable_auto_approval()
auto_approval.save_config()
```

### GitHub Actions Not Running?

1. Check workflow file: `.github/workflows/auto-approve.yml`
2. Verify permissions in Settings → Actions
3. Check Dependabot is enabled: `.github/dependabot.yml`

## Examples

### Example 1: Edit Documentation
```python
# In cloud_ai_builder.py
builder.write_file("README.md", "# New content")
# → ✅ Auto-approved (safe file type)
```

### Example 2: Run Safe Command
```python
builder.execute_command("git status")
# → ✅ Auto-approved (read-only command)
```

### Example 3: Unsafe Operation
```python
builder.execute_command("rm -rf /")
# → ⚠️ Manual approval required
```

## Quick Tips

💡 **Start conservatively** - Enable only for docs first  
💡 **Review logs weekly** - Check `.copilot_approvals.log`  
💡 **Test before deploying** - Use safe operations first  
💡 **Keep config backed up** - Commit `.copilot_auto_approve.json`

## Get Help

📖 Full docs: `AUTO_APPROVAL_GUIDE.md`  
🔍 Check logs: `cat .copilot_approvals.log`  
⚙️ View config: `cat .copilot_auto_approve.json`

---

**Status:** ✅ Production Ready  
**Last Updated:** October 2025
