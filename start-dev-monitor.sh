#!/bin/bash
# Development Monitor - Quick Start Script

echo "🎯 Development Progress Monitor"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "dev_monitor.py" ]; then
    echo "❌ Error: dev_monitor.py not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

echo "Select an option:"
echo ""
echo "1) 📊 Generate Single Report"
echo "2) 🔄 Start Continuous Monitoring (30-min intervals)"
echo "3) 🌐 Launch Web Dashboard"
echo "4) 📋 View Latest Report"
echo "5) 🛑 Stop All Monitoring"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "📊 Generating development progress report..."
        echo ""
        python3 dev_monitor.py
        ;;
    
    2)
        echo ""
        echo "🔄 Starting continuous monitoring..."
        echo "Reports will be generated every 30 minutes"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 dev_monitor.py --continuous
        ;;
    
    3)
        echo ""
        echo "🌐 Launching web dashboard..."
        echo "Dashboard will be available at http://localhost:7862"
        echo ""
        python3 dev_monitor_dashboard.py
        ;;
    
    4)
        echo ""
        echo "📋 Latest Report:"
        echo ""
        if [ -f "dev_reports/latest_report.json" ]; then
            python3 -c "
import json
with open('dev_reports/latest_report.json', 'r') as f:
    report = json.load(f)
    print(f\"Generated: {report['timestamp']}\")
    print(f\"Overall Progress: {report['overall_progress_percent']:.1f}%\")
    print(f\"\\nReport saved in: dev_reports/latest_report.json\")
"
        else
            echo "No report found yet. Generate one first!"
        fi
        ;;
    
    5)
        echo ""
        echo "🛑 Stopping all monitoring processes..."
        pkill -f "dev_monitor.py --continuous"
        pkill -f "dev_monitor_dashboard.py"
        echo "✅ All monitoring stopped"
        ;;
    
    *)
        echo "❌ Invalid choice. Please run again and select 1-5."
        exit 1
        ;;
esac
