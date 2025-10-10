#!/usr/bin/env bash
# 🤖 Cline AI Assistant Setup - VS Code/Cursor Extension

set -e

echo "🤖 Setting up Cline AI Assistant..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create Cline config directory
mkdir -p "$HOME/.config/vibe-coding/cline"

# ━━━ Cline Configuration ━━━
echo "📝 Creating Cline configuration..."

cat > "$HOME/.config/vibe-coding/cline/cline_settings.json" << 'EOF'
{
  "cline.apiProvider": "anthropic",
  "cline.apiKey": "",
  "cline.apiModelId": "claude-3-5-sonnet-20241022",
  "cline.alwaysAllowReadOnly": true,
  "cline.alwaysAllowWrite": false,
  "cline.alwaysAllowExecute": false,
  "cline.enableClineReporter": true,
  "cline.customInstructions": "You are working in a vibe-coding environment with enhanced AI tools. Use modern ES6+ syntax, functional programming patterns, and beautiful console output with emojis. Follow Tokyo Night theme aesthetics.",
  "cline.browserCommandsEnabled": true,
  "cline.soundEnabled": true,
  "cline.diffEnabled": true,
  "cline.requestDelaySeconds": 3,
  "cline.writeDelayMs": 1000,
  "cline.contextWindow": 200000,
  "cline.maxFileLineThreshold": 1000,
  "cline.taskHistory": []
}
EOF

# ━━━ Create Cline Custom Instructions ━━━
cat > "$HOME/.config/vibe-coding/cline/custom-instructions.md" << 'EOF'
# Cline Custom Instructions - Vibe Coding Environment

## Environment Context
You are working in a carefully crafted vibe-coding environment with:
- Tokyo Night theme aesthetics
- Enhanced terminal tools (eza, bat, btop, fzf)
- Multiple AI integrations (OpenRouter, Kimi K2, GitHub Copilot)
- Hammerspoon global shortcuts
- Bitwarden for secure key management
- Starship prompt with custom config

## Code Style Guidelines

### General Principles
- Write clean, self-documenting code
- Prefer composition over inheritance
- Use meaningful variable names
- Add error handling for all async operations
- Include JSDoc comments for public functions

### JavaScript/TypeScript
- Use modern ES6+ syntax
- Prefer `const` over `let`, never use `var`
- Use async/await over promise chains
- Destructure objects and arrays when appropriate
- Use template literals for string interpolation
- Arrow functions for callbacks, named functions for methods

### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Prefer f-strings for formatting
- Use list/dict comprehensions when readable
- Add docstrings to all public functions/classes

### Imports Organization
1. Standard library imports
2. Third-party library imports
3. Local/internal imports
4. Sort alphabetically within each group

### Error Handling
- Always use try/except (Python) or try/catch (JS/TS)
- Provide meaningful error messages
- Log errors with context
- Never swallow exceptions silently

## Aesthetic Preferences

### Console Output
- Use emojis for visual clarity (✅ ❌ 🚀 ⚡ 💡 🎨 🔥 etc.)
- Colorful terminal output (chalk, colors, rich)
- Beautiful CLI interfaces with boxes and formatting
- Progress indicators for long operations

### Comments
- Use emojis in section headers: `// 🎯 Main Logic`, `// 🔧 Helper Functions`
- Explain "why" not "what" in comments
- Add TODO comments with emojis: `// TODO: 🚧 Implement caching`

### File Organization
- Group related functions together with emoji section headers
- Separate concerns into modules
- Keep files under 300 lines when possible

## Project Patterns

### Configuration Files
- Use JSON/YAML for config when possible
- Environment variables for secrets (loaded via Bitwarden)
- Document all config options

### Testing
- Write tests for critical functionality
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Git Commits
- Use conventional commits format
- Include emoji prefixes: `✨ feat:`, `🐛 fix:`, `📝 docs:`, `♻️ refactor:`

## AI Workflow Integration

### When Working on Tasks
1. Understand the full context before coding
2. Ask clarifying questions if requirements are unclear
3. Break complex tasks into smaller steps
4. Test changes before marking complete
5. Update documentation as needed

### Tool Usage
- Prefer built-in tools over creating new scripts
- Use the vibe-coding shortcuts and aliases
- Integrate with existing AI tools (ai-ask, vibe-ai)
- Respect the Tokyo Night color scheme

### Communication Style
- Be friendly and helpful
- Explain complex concepts clearly
- Provide examples when helpful
- Suggest improvements proactively

## Environment-Specific Commands

### Available Shortcuts
- `vibe_start` - Initialize vibe session
- `ai-ask <prompt>` - Quick AI query (OpenRouter)
- `ai-code <prompt>` - Code-focused AI query
- `vibe-dash` - Show dashboard
- `ai_status` - Check AI tools status
- `lofi` - Start lo-fi music

### IDE Shortcuts (Hammerspoon)
- ⌘ ⌥ C - Open Cursor
- ⌘ ⌥ V - Open VS Code Insiders
- ⌘ ⌥ W - Open Windsurf
- ⌘ ⌥ G - GitHub Copilot Chat
- ⌘ ⌥ D - Show Dashboard

## Security
- Never hardcode API keys or secrets
- Use Bitwarden for credential management
- Load env vars via `bwload` command
- Keep sensitive data out of version control

## Best Practices
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Write code for humans first, computers second
- Optimize for readability over cleverness

## Priority
1. Code correctness and reliability
2. Code readability and maintainability
3. Performance optimization
4. Aesthetic improvements

Remember: We're building not just functional code, but a beautiful, maintainable, and enjoyable development experience! 🎨✨
EOF

# ━━━ Create Cline task templates ━━━
cat > "$HOME/.config/vibe-coding/cline/task-templates.json" << 'EOF'
{
  "templates": {
    "feature": {
      "name": "New Feature",
      "steps": [
        "Understand requirements and context",
        "Design the feature architecture",
        "Implement core functionality",
        "Add error handling and edge cases",
        "Write tests",
        "Update documentation",
        "Test thoroughly"
      ]
    },
    "bugfix": {
      "name": "Bug Fix",
      "steps": [
        "Reproduce the bug",
        "Identify root cause",
        "Design the fix",
        "Implement the fix",
        "Add test to prevent regression",
        "Verify fix works",
        "Update changelog"
      ]
    },
    "refactor": {
      "name": "Code Refactoring",
      "steps": [
        "Identify code to refactor",
        "Write tests for existing behavior",
        "Refactor code incrementally",
        "Ensure tests still pass",
        "Update documentation if needed",
        "Review for improvements"
      ]
    },
    "optimization": {
      "name": "Performance Optimization",
      "steps": [
        "Profile current performance",
        "Identify bottlenecks",
        "Design optimization strategy",
        "Implement optimizations",
        "Measure performance improvements",
        "Document changes"
      ]
    }
  }
}
EOF

# ━━━ Create Cline helper scripts ━━━
cat > "$HOME/.config/vibe-coding/cline/cline-helper.sh" << 'EOF'
#!/usr/bin/env bash
# Cline helper commands

# Check if Cline extension is installed
cline-check() {
    local cursor_ext="$HOME/.cursor/extensions"
    local vscode_ext="$HOME/.vscode-insiders/extensions"
    
    echo "🔍 Checking for Cline extension..."
    
    if [ -d "$cursor_ext" ] && ls "$cursor_ext" | grep -q "saoudrizwan.claude-dev"; then
        echo "✅ Cline found in Cursor"
        return 0
    fi
    
    if [ -d "$vscode_ext" ] && ls "$vscode_ext" | grep -q "saoudrizwan.claude-dev"; then
        echo "✅ Cline found in VS Code Insiders"
        return 0
    fi
    
    echo "❌ Cline extension not found"
    echo "💡 Install from: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev"
    return 1
}

# Show Cline status
cline-status() {
    echo "🤖 Cline AI Assistant Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cline-check
    
    echo ""
    echo "📁 Config Location:"
    echo "   $HOME/.config/vibe-coding/cline/"
    
    echo ""
    echo "🔑 API Key Status:"
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo "   ✅ ANTHROPIC_API_KEY set"
    else
        echo "   ❌ ANTHROPIC_API_KEY not set (run: bwload)"
    fi
    
    echo ""
    echo "📚 Documentation:"
    echo "   Custom Instructions: ~/.config/vibe-coding/cline/custom-instructions.md"
    echo "   Task Templates: ~/.config/vibe-coding/cline/task-templates.json"
}

# Open Cline documentation
cline-docs() {
    if command -v bat &> /dev/null; then
        bat "$HOME/.config/vibe-coding/cline/custom-instructions.md"
    else
        cat "$HOME/.config/vibe-coding/cline/custom-instructions.md"
    fi
}

# Install Cline extension
cline-install() {
    echo "🤖 Installing Cline extension..."
    
    # Check for Cursor
    if [ -d "/Applications/Cursor.app" ]; then
        echo "📦 Installing in Cursor..."
        cursor --install-extension saoudrizwan.claude-dev
    fi
    
    # Check for VS Code Insiders
    if [ -d "/Applications/Visual Studio Code - Insiders.app" ]; then
        echo "📦 Installing in VS Code Insiders..."
        code-insiders --install-extension saoudrizwan.claude-dev
    fi
    
    # Check for Windsurf
    if [ -d "/Applications/Windsurf.app" ]; then
        echo "📦 Installing in Windsurf..."
        windsurf --install-extension saoudrizwan.claude-dev
    fi
    
    echo "✅ Installation complete! Restart your IDE."
}

# Update Cline settings
cline-update-settings() {
    echo "🔧 Updating Cline settings in IDEs..."
    
    # Cursor
    if [ -d "$HOME/Library/Application Support/Cursor/User" ]; then
        echo "Updating Cursor settings..."
        # Merge Cline settings into Cursor settings.json
        echo "💡 Manually add Cline settings from: ~/.config/vibe-coding/cline/cline_settings.json"
    fi
    
    # VS Code Insiders
    if [ -d "$HOME/Library/Application Support/Code - Insiders/User" ]; then
        echo "Updating VS Code Insiders settings..."
        echo "💡 Manually add Cline settings from: ~/.config/vibe-coding/cline/cline_settings.json"
    fi
}

# Export functions
export -f cline-check
export -f cline-status
export -f cline-docs
export -f cline-install
export -f cline-update-settings
EOF

chmod +x "$HOME/.config/vibe-coding/cline/cline-helper.sh"

# ━━━ Add Cline aliases to shell ━━━
cat > "$HOME/.config/vibe-coding/cline/aliases.sh" << 'EOF'
# 🤖 Cline AI Assistant Aliases

# Source helper functions
source ~/.config/vibe-coding/cline/cline-helper.sh

# Quick access commands
alias cline='cline-status'
alias cline-help='cline-docs'
alias cline-config='cursor ~/.config/vibe-coding/cline/'

# Cline task shortcuts
alias cline-feature='echo "🚀 Starting new feature task..."'
alias cline-fix='echo "🐛 Starting bug fix task..."'
alias cline-refactor='echo "♻️ Starting refactor task..."'
EOF

echo ""
echo "✅ Cline setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 Cline AI Assistant - Setup Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Next Steps:"
echo ""
echo "1. Install Cline Extension:"
echo "   • Run: cline-install"
echo "   • Or manually install from VS Code/Cursor marketplace"
echo "   • Extension ID: saoudrizwan.claude-dev"
echo ""
echo "2. Configure API Key:"
echo "   • Add ANTHROPIC_API_KEY to Bitwarden"
echo "   • Run: bwload"
echo "   • Or set in Cline extension settings"
echo ""
echo "3. Verify Installation:"
echo "   • Run: cline-status"
echo "   • Open Cursor/VS Code and check for Cline icon"
echo ""
echo "📚 Documentation:"
echo "   • Custom Instructions: ~/.config/vibe-coding/cline/custom-instructions.md"
echo "   • View: cline-docs"
echo ""
echo "🎯 Quick Commands:"
echo "   cline-status      → Check Cline setup"
echo "   cline-docs        → View custom instructions"
echo "   cline-install     → Install extension"
echo "   cline-config      → Open config directory"
echo ""
echo "🔗 Resources:"
echo "   • Marketplace: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev"
echo "   • GitHub: https://github.com/saoudrizwan/claude-dev"
echo ""
echo "💡 Tip: Use ⌘ ⌥ G in Cursor/VS Code to open Cline chat!"
echo ""

