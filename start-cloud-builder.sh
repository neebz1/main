#!/bin/bash
# 🤖 Cloud AI Builder - Access from anywhere!

echo "🤖 Starting Cloud AI Builder..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

echo ""
echo "=" * 60
echo "🌐 Cloud AI Builder"
echo "Talk to your AI assistant from ANY device!"
echo "=" * 60
echo ""

# Launch the app
python cloud_ai_builder.py

