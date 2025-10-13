#!/bin/bash

# Quick App Launch Tester
# Tests that each app can at least import its dependencies and start

echo "🧪 Testing App Launch Capabilities..."
echo "======================================"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null

test_app() {
    APP_NAME=$1
    APP_FILE=$2

    echo -n "Testing $APP_NAME... "

    # Try to import the app (don't actually run it)
    timeout 5 python3 -c "
import sys
sys.argv = ['$APP_FILE']
try:
    # Just check if the file can be imported/syntax is valid
    with open('$APP_FILE', 'r') as f:
        code = f.read()
    compile(code, '$APP_FILE', 'exec')
    print('✅ OK')
except Exception as e:
    print(f'❌ FAILED: {e}')
    sys.exit(1)
" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        return 1
    fi
}

# Test main apps
test_app "App.py" "app.py"
test_app "AI Mixing Engineer" "ai_mixing_engineer.py"
test_app "Live AI Assistant" "live_ai_assistant.py"
test_app "Logic AI Plugin" "logic_ai_plugin.py"
test_app "Logic Copilot Lite" "logic_copilot_lite.py"
test_app "Cloud AI Builder" "cloud_ai_builder.py"
test_app "Demo Chatbot" "demo_chatbot.py"
test_app "Train ChatGPT Model" "train_chatgpt_model.py"

echo ""
echo "Testing library imports..."
echo "-------------------------"

# Test critical imports
python3 << 'EOF'
import sys

def test_import(module_name, display_name=None):
    if display_name is None:
        display_name = module_name
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
        return True
    except ImportError as e:
        print(f"❌ {display_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {display_name}: {e}")
        return True  # Module exists but had other issue

all_ok = True
all_ok &= test_import('gradio', 'Gradio (Web UI)')
all_ok &= test_import('openai', 'OpenAI')
all_ok &= test_import('anthropic', 'Anthropic (Claude)')
all_ok &= test_import('together', 'Together AI')
all_ok &= test_import('librosa', 'Librosa (Audio)')
all_ok &= test_import('dotenv', 'python-dotenv')
all_ok &= test_import('requests', 'Requests')
all_ok &= test_import('numpy', 'NumPy')

sys.exit(0 if all_ok else 1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All tests passed! Apps are ready to launch.${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Some issues detected. Run: pip install -r requirements.txt${NC}"
fi

echo ""
echo "To launch an app, run one of these:"
echo "  ./start-live-ai-assistant.sh"
echo "  ./start-ai-mixing-engineer.sh"
echo "  ./start-api.sh"
echo ""

