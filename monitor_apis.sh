#!/bin/bash
# 🔍 API Integration Monitor - Run Comprehensive API Health Checks

echo "🔍 API Integration Monitor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import httpx" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required dependencies..."
    pip install httpx python-dotenv
fi

echo ""
echo "🚀 Running API monitoring..."
echo ""

# Run the monitor
python3 api_monitor.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Monitoring complete!"
echo ""
echo "📊 Metrics saved to: api_metrics.json"
echo "🔄 Run this script regularly to track API health over time"
echo ""
