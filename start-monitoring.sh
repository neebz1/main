#!/bin/bash
# DevOps Monitoring System - Quick Start Script

echo "🔍 DevOps Monitoring System"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import psutil, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip3 install psutil requests python-dotenv
fi

echo "✅ Dependencies ready"
echo ""

# Run monitoring
echo "🚀 Running health check..."
echo ""
python3 devops_monitor.py --check

echo ""
echo "✅ Monitoring complete!"
echo ""
echo "📊 View reports in: monitoring_reports/"
echo "📖 Documentation: MONITORING_DOCS.md"
