#!/bin/bash
# Logic Pro Copilot Launcher

echo "🎵 Starting Logic Pro Copilot..."
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check for API key
if [ ! -f .env ]; then
    echo "⚠️  No .env file found."
    echo "The app will work, but AI chat features need an API key."
    echo "See config_example.txt for setup instructions."
    echo ""
fi

# Launch the app
echo "🚀 Launching Logic Pro Copilot..."
echo "The app will open in your browser at http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server when you're done."
echo "================================"
echo ""

python3 logic_copilot.py

