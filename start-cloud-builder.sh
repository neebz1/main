#!/bin/bash
# 🤖 Cloud AI Builder - Access from anywhere!

echo "🤖 Starting Cloud AI Builder..."
echo ""

# Go to the right directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

echo ""
printf '=%.0s' {1..60}
echo ""
echo "🌐 Cloud AI Builder"
echo "Talk to your AI assistant from ANY device!"
printf '=%.0s' {1..60}
echo ""
echo ""

# Launch the app
python cloud_ai_builder.py

