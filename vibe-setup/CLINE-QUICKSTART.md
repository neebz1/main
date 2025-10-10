# 🤖 Cline AI Assistant - Quick Start Guide

## What is Cline?

Cline (formerly Claude Dev) is a powerful AI coding assistant that runs directly in VS Code/Cursor. Unlike GitHub Copilot which suggests code, Cline can:
- **Write entire files** from scratch
- **Edit multiple files** in your project
- **Execute terminal commands** (with your approval)
- **Browse the web** for documentation
- **Understand your entire codebase** context
- **Debug and fix errors** automatically

Think of Cline as having an AI pair programmer that can actually *do* things, not just suggest.

---

## 🚀 Quick Setup (3 Steps)

### 1. Check Installation Status
```bash
cline-status
```

**Already installed?** ✅ Skip to Step 2!

**Not installed?** Install with:
```bash
cline-install
```

### 2. Add API Key to Bitwarden

You need an Anthropic API key for Claude:

1. Get your key: https://console.anthropic.com/
2. Add to Bitwarden:
   ```bash
   bw login
   # Add item named "ANTHROPIC_API_KEY" with your key
   ```
3. Load environment variables:
   ```bash
   bwload
   ```

**Alternative:** Set the API key directly in Cline's settings (⌘,) → Search "Cline"

### 3. Verify Setup

Open Cursor and look for the Cline icon in the sidebar (looks like a chat bubble).

Click it and type: "Hello! Can you help me code?"

If Cline responds, you're all set! 🎉

---

## 💡 How to Use Cline

### Opening Cline

**Method 1:** Click the Cline icon in the sidebar
**Method 2:** Use keyboard shortcut: `⌘ ⌥ G` (Command + Option + G)
**Method 3:** Command Palette (⌘⇧P) → "Cline: Open Chat"

### Basic Workflow

1. **Open Cline chat** (⌘ ⌥ G)
2. **Describe what you want** in natural language
3. **Review Cline's plan** before it executes
4. **Approve or reject** each action
5. **Iterate** until the task is complete

### Example Prompts

```
"Create a React component for a todo list with add/delete functionality"

"Refactor this file to use TypeScript instead of JavaScript"

"Debug why my API call is failing with a 404 error"

"Add error handling to all async functions in this project"

"Write tests for the UserService class"

"Optimize this code for better performance"

"Convert this REST API to use GraphQL"
```

---

## 🎯 Best Practices

### ✅ DO

- **Be specific** about what you want
- **Provide context** (mention file names, technologies, goals)
- **Review before approving** - always check Cline's suggestions
- **Use it for boilerplate** - let Cline write repetitive code
- **Ask for explanations** - "Explain what this code does"
- **Iterate** - refine your request based on results

### ❌ DON'T

- **Blindly approve everything** - always review changes
- **Give vague requests** - be clear about requirements
- **Trust it with security-sensitive code** - review carefully
- **Skip testing** - always test Cline's code
- **Forget to save** - Cline edits files but doesn't auto-save

---

## 🔧 Cline Commands (Terminal)

| Command | Description |
|---------|-------------|
| `cline-status` | Check if Cline is installed and configured |
| `cline-install` | Install Cline extension in all IDEs |
| `cline-docs` | View custom instructions |
| `cline-config` | Open Cline config directory |
| `cline` | Alias for `cline-status` |

---

## ⚙️ Configuration

### Your Custom Instructions

Cline has been pre-configured with your vibe-coding environment preferences:

- **Code Style:** Modern ES6+, functional programming, beautiful console output
- **Theme:** Tokyo Night aesthetics
- **Environment:** Aware of your AI tools, shortcuts, and workflow
- **Comments:** Uses emojis in section headers (🎯, 🔧, 💡, etc.)

**View custom instructions:**
```bash
cline-docs
```

**Edit custom instructions:**
```bash
cursor ~/.config/vibe-coding/cline/custom-instructions.md
```

### Cline Settings

Configure in Cursor: `⌘,` → Search "Cline"

Key settings:
- **API Provider:** Anthropic (Claude)
- **Model:** claude-3-5-sonnet-20241022
- **Context Window:** 200,000 tokens
- **Auto-approve read:** ✅ (allows reading files)
- **Auto-approve write:** ❌ (requires approval for changes)
- **Auto-approve execute:** ❌ (requires approval for commands)

---

## 🎓 Example Workflows

### 1. Create a New Feature

```
You: "Create a user authentication system with login, logout, 
and session management using JWT tokens"

Cline: [Shows plan]
- Create auth service
- Add JWT middleware
- Create login/logout routes
- Add session validation
[Approve?]

You: ✅ Approve

Cline: [Creates files and implements]
```

### 2. Debug an Issue

```
You: "The API call on line 45 of api.ts is failing with a 
network error. Can you debug it?"

Cline: [Reads api.ts, identifies issue, proposes fix]
```

### 3. Refactor Code

```
You: "Refactor UserController.js to use async/await instead 
of promise chains, and add proper error handling"

Cline: [Analyzes code, refactors, adds try/catch blocks]
```

### 4. Write Tests

```
You: "Write comprehensive unit tests for the PaymentService 
class using Jest"

Cline: [Creates test file with multiple test cases]
```

---

## 🔑 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘ ⌥ G` | Open Cline chat |
| `⌘ ⇧ P` | Command palette (search "Cline") |
| `⌘ ,` | Open settings (search "Cline") |

---

## 🛠️ Troubleshooting

### Cline Not Responding

1. Check API key: `cline-status`
2. Reload Cline: Restart Cursor
3. Check rate limits: You might have hit API limits
4. Verify internet connection

### "API Key Not Set" Error

**Option 1: Bitwarden**
```bash
bw unlock
bwload
```

**Option 2: Direct in Cline**
- Open Cline settings (⌘,)
- Search "Cline API Key"
- Paste your Anthropic API key

### Extension Not Found

```bash
cline-install
```

Then restart Cursor.

### Changes Not Saving

Cline edits files but doesn't auto-save. Press `⌘ S` to save.

---

## 💰 Cost & Usage

### Pricing

Cline uses Claude 3.5 Sonnet via Anthropic API:
- **Input:** ~$3 per million tokens
- **Output:** ~$15 per million tokens

**Typical session:** $0.10 - $0.50 for most coding tasks

### Tips to Save Money

- Be specific to reduce back-and-forth
- Use smaller context (don't include entire large files if not needed)
- Start with cheaper models for simple tasks
- Set usage limits in your Anthropic account

---

## 🎨 Vibe Coding Integration

Cline has been configured to match your vibe-coding environment:

### Custom Instructions Included

- ✅ Tokyo Night color scheme awareness
- ✅ Emoji-enhanced code comments
- ✅ Modern ES6+ JavaScript/TypeScript patterns
- ✅ Functional programming preferences
- ✅ Beautiful console output (chalk, colors, rich)
- ✅ Integration with your AI tools (ai-ask, vibe-ai)
- ✅ Awareness of Hammerspoon shortcuts
- ✅ Bitwarden for secrets management

### Task Templates

Pre-configured templates for common tasks:
- **feature:** New feature development
- **bugfix:** Bug fixing workflow
- **refactor:** Code refactoring
- **optimization:** Performance optimization

**View templates:**
```bash
cat ~/.config/vibe-coding/cline/task-templates.json
```

---

## 📚 Resources

### Documentation
- **Cline GitHub:** https://github.com/saoudrizwan/claude-dev
- **Marketplace:** https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev
- **Anthropic API:** https://docs.anthropic.com/

### Your Configuration Files
```bash
~/.config/vibe-coding/cline/
├── cline_settings.json          # Cline preferences
├── custom-instructions.md       # Your coding rules
├── task-templates.json          # Task workflows
├── cline-helper.sh             # Helper scripts
└── aliases.sh                  # Shell aliases
```

### Getting Help
```bash
cline-docs              # View custom instructions
cline-status           # Check setup
cline-config           # Open config directory
```

---

## 🚀 Pro Tips

1. **Use Cline for boilerplate** - Let it write repetitive code while you focus on logic
2. **Iterate with Cline** - Start broad, then refine with follow-up prompts
3. **Combine with GitHub Copilot** - Use Copilot for autocomplete, Cline for major changes
4. **Save conversation history** - Cline remembers context within a chat session
5. **Review diffs carefully** - Always check what Cline changed
6. **Use `@files` mentions** - Type `@` to reference specific files in your prompt
7. **Ask for explanations** - "Explain why you chose this approach"
8. **Test AI-generated code** - Always verify functionality

---

## 🎯 Next Steps

1. **Try it now:**
   ```bash
   # Open Cursor
   cursor .
   
   # Press ⌘ ⌥ G to open Cline
   # Type: "Hello! Help me create a simple Express API"
   ```

2. **Explore examples:**
   - Ask Cline to explain code in your project
   - Have it write a function you need
   - Request code reviews and improvements

3. **Customize:**
   ```bash
   # Edit your custom instructions
   cursor ~/.config/vibe-coding/cline/custom-instructions.md
   ```

4. **Integrate with workflow:**
   - Use Cline for complex tasks
   - Use GitHub Copilot for autocompletion
   - Use `ai-ask` for quick questions

---

**🎨 Happy Vibe Coding with Cline! 🚀**

*Remember: Cline is a tool to augment your coding, not replace your thinking. Always review, test, and understand the code it generates.*

