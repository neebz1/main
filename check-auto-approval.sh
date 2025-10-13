#!/bin/bash
# Auto-Approval Status Checker
# Quick way to check auto-approval system status

echo "🤖 Auto-Approval System Status"
echo "================================"
echo ""

# Check if auto_approval.py exists
if [ ! -f "auto_approval.py" ]; then
    echo "❌ auto_approval.py not found!"
    exit 1
fi

# Check if enabled
ENABLED=$(python3 -c "from auto_approval import auto_approval; print('Yes' if auto_approval.config.get('enabled') else 'No')" 2>/dev/null)
if [ $? -eq 0 ]; then
    if [ "$ENABLED" = "Yes" ]; then
        echo "✅ Auto-Approval: ENABLED"
    else
        echo "⚠️  Auto-Approval: DISABLED"
    fi
else
    echo "❌ Error checking status"
    exit 1
fi

echo ""
echo "📊 Statistics:"
python3 << 'EOF'
from auto_approval import auto_approval
stats = auto_approval.get_approval_stats()
print(f"   Total actions: {stats['total']}")
print(f"   Auto-approved: {stats['approved']}")
print(f"   Rejected: {stats['rejected']}")
print(f"   Approval rate: {stats['approval_rate']:.1f}%")
EOF

echo ""
echo "📁 Files:"
if [ -f ".copilot_approvals.log" ]; then
    LOG_SIZE=$(wc -l < .copilot_approvals.log)
    echo "   ✅ Approval log: $LOG_SIZE entries"
else
    echo "   ⚠️  No approval log yet"
fi

if [ -f ".copilot_auto_approve.json" ]; then
    echo "   ✅ Config file exists"
else
    echo "   ⚠️  No config file (will be created on first run)"
fi

echo ""
echo "🔧 Quick Commands:"
echo "   Enable:  python3 -c 'from auto_approval import auto_approval; print(auto_approval.enable_auto_approval())'"
echo "   Disable: python3 -c 'from auto_approval import auto_approval; print(auto_approval.disable_auto_approval())'"
echo "   View log: tail -20 .copilot_approvals.log"
echo ""
