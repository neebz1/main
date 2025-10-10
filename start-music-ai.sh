#!/bin/bash
# 🎵 Logic Pro Copilot - One-click launcher

echo "🎵 Starting Logic Pro Copilot..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import gradio" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements_lite.txt
fi

# Launch the app
python logic_copilot_lite.py

