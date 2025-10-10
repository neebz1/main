#!/usr/bin/env bash
# 🤖 AI Tool Integrations - Cursor, Kimi K2, OpenRouter, Hugging Face

set -e

echo "🤖 Configuring AI tool integrations..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create AI tools config directory
mkdir -p "$HOME/.config/vibe-coding/ai-tools"

# ━━━ Cursor AI Configuration ━━━
echo "📝 Configuring Cursor AI..."

CURSOR_CONFIG="$HOME/Library/Application Support/Cursor/User"
mkdir -p "$CURSOR_CONFIG"

# Create Cursor AI rules file
cat > "$HOME/.config/vibe-coding/ai-tools/cursor-rules.md" << 'EOF'
# Cursor AI Rules - Vibe Coding Environment

## Code Style
- Use modern ES6+ JavaScript/TypeScript syntax
- Prefer functional programming patterns
- Use async/await over promises chains
- Include JSDoc comments for functions
- Follow Airbnb style guide

## Imports
- Use named imports over default when possible
- Group imports: external → internal → relative
- Sort imports alphabetically

## Best Practices
- Write self-documenting code
- Prefer composition over inheritance
- Keep functions small and focused
- Use meaningful variable names
- Add error handling for async operations

## AI Workflow
- Provide context from related files when asking
- Request explanations for complex logic
- Ask for refactoring suggestions regularly
- Use AI for documentation generation

## Vibe Coding Style
- Add aesthetic console logs with emojis
- Use colorful terminal output (chalk, colors)
- Create beautiful CLI interfaces
- Prioritize developer experience
EOF

# Link Cursor rules
ln -sf "$HOME/.config/vibe-coding/ai-tools/cursor-rules.md" "$CURSOR_CONFIG/.cursorrules" 2>/dev/null || true

# ━━━ OpenRouter Configuration ━━━
echo "📝 Configuring OpenRouter..."

cat > "$HOME/.config/vibe-coding/ai-tools/openrouter-config.json" << 'EOF'
{
  "api_base": "https://openrouter.ai/api/v1",
  "default_model": "anthropic/claude-3.5-sonnet",
  "models": {
    "fast": "anthropic/claude-3-haiku",
    "balanced": "anthropic/claude-3.5-sonnet",
    "powerful": "anthropic/claude-opus-4",
    "code": "meta-llama/codellama-70b-instruct",
    "creative": "google/gemini-pro-1.5"
  },
  "parameters": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 4096
  }
}
EOF

# Create OpenRouter CLI wrapper
cat > "$HOME/.config/vibe-coding/ai-tools/openrouter-cli.py" << 'EOF'
#!/usr/bin/env python3
# OpenRouter CLI - Quick AI prompts from terminal

import os
import sys
import json
import httpx
from pathlib import Path

CONFIG_FILE = Path.home() / ".config/vibe-coding/ai-tools/openrouter-config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def query_openrouter(prompt, model=None):
    config = load_config()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not set. Run: bwload")
        sys.exit(1)
    
    model = model or config["default_model"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://vibe-coding.local",
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        **config["parameters"]
    }
    
    print(f"🤖 Querying {model}...\n")
    
    with httpx.Client() as client:
        response = client.post(
            f"{config['api_base']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60.0
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            print(answer)
            print(f"\n💰 Tokens: {result['usage']['total_tokens']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: openrouter-cli.py <prompt> [model]")
        print("\nAvailable models: fast, balanced, powerful, code, creative")
        sys.exit(1)
    
    prompt = sys.argv[1]
    model_alias = sys.argv[2] if len(sys.argv) > 2 else None
    
    if model_alias:
        config = load_config()
        model = config["models"].get(model_alias, model_alias)
    else:
        model = None
    
    query_openrouter(prompt, model)
EOF

chmod +x "$HOME/.config/vibe-coding/ai-tools/openrouter-cli.py"

# ━━━ Kimi K2 Configuration ━━━
echo "📝 Configuring Kimi K2 integration..."

cat > "$HOME/.config/vibe-coding/ai-tools/kimi-config.sh" << 'EOF'
#!/usr/bin/env bash
# Kimi K2 Configuration

# Kimi API endpoints (placeholder - update with actual endpoints)
export KIMI_API_BASE="https://api.moonshot.cn/v1"
export KIMI_MODEL="moonshot-v1-8k"

# Quick Kimi query function
kimi() {
    local prompt="$*"
    
    if [ -z "$KIMI_API_KEY" ]; then
        echo "❌ KIMI_API_KEY not set"
        return 1
    fi
    
    curl -s -X POST "$KIMI_API_BASE/chat/completions" \
        -H "Authorization: Bearer $KIMI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$KIMI_MODEL\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}]
        }" | jq -r '.choices[0].message.content'
}

# Export function
export -f kimi
EOF

# ━━━ Hugging Face Configuration ━━━
echo "📝 Configuring Hugging Face..."

cat > "$HOME/.config/vibe-coding/ai-tools/huggingface-cli.py" << 'EOF'
#!/usr/bin/env python3
# Hugging Face Hub CLI

import os
import sys
from huggingface_hub import HfApi, login

def setup_hf():
    token = os.getenv("HF_TOKEN")
    if token:
        login(token=token)
        print("✅ Hugging Face authenticated")
    else:
        print("❌ HF_TOKEN not set. Run: bwload")
        sys.exit(1)

def search_models(query, limit=5):
    setup_hf()
    api = HfApi()
    models = api.list_models(search=query, limit=limit)
    
    print(f"🔍 Top {limit} models for '{query}':\n")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model.modelId}")
        print(f"   Downloads: {model.downloads:,}")
        print(f"   {model.pipeline_tag or 'N/A'}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: huggingface-cli.py <search-query>")
        sys.exit(1)
    
    search_models(sys.argv[1])
EOF

chmod +x "$HOME/.config/vibe-coding/ai-tools/huggingface-cli.py"

# ━━━ AI Tools Aliases ━━━
cat > "$HOME/.config/vibe-coding/ai-tools/aliases.sh" << 'EOF'
# 🤖 AI Tools Aliases

# OpenRouter
alias ai-ask='python3 ~/.config/vibe-coding/ai-tools/openrouter-cli.py'
alias ai-fast='python3 ~/.config/vibe-coding/ai-tools/openrouter-cli.py "$@" fast'
alias ai-code='python3 ~/.config/vibe-coding/ai-tools/openrouter-cli.py "$@" code'
alias ai-powerful='python3 ~/.config/vibe-coding/ai-tools/openrouter-cli.py "$@" powerful'

# Kimi K2
source ~/.config/vibe-coding/ai-tools/kimi-config.sh

# Hugging Face
alias hf-search='python3 ~/.config/vibe-coding/ai-tools/huggingface-cli.py'

# GitHub Copilot
alias copilot-explain='gh copilot explain'
alias copilot-suggest='gh copilot suggest'

# Quick code review
alias ai-review='git diff | ai-code "Review this code diff and suggest improvements:"'

# Documentation generation
alias ai-docs='ai-code "Generate documentation for this code:" < '
EOF

# ━━━ Create unified AI prompt wrapper ━━━
cat > "$HOME/.config/vibe-coding/ai-tools/vibe-ai.sh" << 'EOF'
#!/usr/bin/env bash
# 🎨 Vibe AI - Unified AI tool interface

USAGE="Usage: vibe-ai <tool> <prompt>

Available tools:
  openrouter, or  - OpenRouter (default: Claude Sonnet)
  kimi, k2        - Kimi K2
  copilot, gh     - GitHub Copilot
  huggingface, hf - Hugging Face search
  
Examples:
  vibe-ai or 'Explain async/await in JavaScript'
  vibe-ai kimi 'Best practices for React hooks'
  vibe-ai gh 'How to use git rebase'
"

if [ $# -lt 2 ]; then
    echo "$USAGE"
    exit 1
fi

TOOL="$1"
shift
PROMPT="$*"

case "$TOOL" in
    openrouter|or)
        python3 ~/.config/vibe-coding/ai-tools/openrouter-cli.py "$PROMPT"
        ;;
    kimi|k2)
        source ~/.config/vibe-coding/ai-tools/kimi-config.sh
        kimi "$PROMPT"
        ;;
    copilot|gh)
        gh copilot explain "$PROMPT"
        ;;
    huggingface|hf)
        python3 ~/.config/vibe-coding/ai-tools/huggingface-cli.py "$PROMPT"
        ;;
    *)
        echo "❌ Unknown tool: $TOOL"
        echo "$USAGE"
        exit 1
        ;;
esac
EOF

chmod +x "$HOME/.config/vibe-coding/ai-tools/vibe-ai.sh"

echo ""
echo "✅ AI tool integrations configured!"
echo ""
echo "🤖 Available AI Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Unified Interface:"
echo "  vibe-ai or <prompt>    → OpenRouter"
echo "  vibe-ai kimi <prompt>  → Kimi K2"
echo "  vibe-ai gh <prompt>    → GitHub Copilot"
echo "  vibe-ai hf <prompt>    → Hugging Face search"
echo ""
echo "Direct Commands:"
echo "  ai-ask <prompt>        → OpenRouter (default)"
echo "  ai-fast <prompt>       → Fast model (Haiku)"
echo "  ai-code <prompt>       → Code model (CodeLlama)"
echo "  ai-powerful <prompt>   → Powerful model (Opus)"
echo "  kimi <prompt>          → Kimi K2 query"
echo "  hf-search <query>      → Search HF models"
echo ""
echo "Copilot:"
echo "  copilot explain <cmd>  → Explain command"
echo "  copilot suggest        → Suggest commands"
echo ""
echo "Workflows:"
echo "  ai-review              → Review git diff"
echo "  ai-docs <file>         → Generate docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Make sure to run 'bwload' to load API keys from Bitwarden"

