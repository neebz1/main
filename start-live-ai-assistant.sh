#!/bin/bash
# 🎤 Live AI Music Assistant - Voice & Vision Control

echo "🎤 Starting Live AI Music Assistant..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import google.generativeai" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    
    # Install PortAudio for PyAudio (required for mic input)
    echo "Installing PortAudio..."
    if command -v brew &> /dev/null; then
        brew install portaudio
    else
        echo "⚠️  Homebrew not found. Please install PortAudio manually"
    fi
    
    pip install -r requirements_live_ai.txt
fi

echo ""
echo "=" * 60
echo "🎵 Live AI Music Assistant"
echo "Voice-controlled AI assistant that can see and control Logic Pro"
echo "=" * 60
echo ""

# Check for API key
if ! grep -q "GOOGLE_API_KEY" .env 2>/dev/null; then
    echo "⚠️  WARNING: GOOGLE_API_KEY not found in .env file"
    echo ""
    echo "To get your API key:"
    echo "1. Visit: https://makersuite.google.com/app/apikey"
    echo "2. Create an API key"
    echo "3. Add to .env file: GOOGLE_API_KEY=your-key-here"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

# Launch the app
python live_ai_assistant.py

