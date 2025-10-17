#!/bin/bash
# 🎚️ Logic Pro AI Plugin - Real-time Control

echo "🎚️ Starting Logic Pro AI Plugin..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import pythonosc" 2>/dev/null; then
    echo "📦 Installing OSC dependencies..."
    pip install -r requirements_plugin.txt
fi

echo ""
printf '=%.0s' {1..60}
echo ""
echo "🎵 Logic Pro AI Plugin - Real-time Mode"
echo "No export/import needed - works LIVE!"
printf '=%.0s' {1..60}
echo ""
echo ""

# Launch the plugin
python logic_ai_plugin.py

