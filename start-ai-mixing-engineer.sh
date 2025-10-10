#!/bin/bash
# 🎚️ AI Mixing Engineer - One-click launcher

echo "🎚️ Starting AI Mixing Engineer..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if librosa is installed
if ! python -c "import librosa" 2>/dev/null; then
    echo "📦 Installing audio processing dependencies..."
    pip install -r requirements_mixing.txt
fi

# Launch the app
python ai_mixing_engineer.py

