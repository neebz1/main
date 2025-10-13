#!/bin/bash
# Quick diagnostic for Arturia KeyLab Essential 49 + Logic Pro

echo "=== Arturia KeyLab Essential 49 Diagnostics ==="
echo ""

# Check if keyboard is connected via USB
echo "1. USB Connection Check:"
system_profiler SPUSBDataType | grep -i "keylab" && echo "   ✅ KeyLab detected via USB" || echo "   ❌ KeyLab NOT detected — replug USB cable"
echo ""

# Check macOS MIDI devices
echo "2. macOS MIDI Devices:"
if command -v aseqdump &> /dev/null || ls /dev/cu.* 2>/dev/null | grep -i midi &> /dev/null; then
    ls /dev/cu.* 2>/dev/null | grep -i "keylab\|midi" || echo "   No MIDI devices in /dev/cu.*"
fi

# Better check using ioreg
ioreg -c IOUSBDevice -r -l | grep -i "keylab" && echo "   ✅ KeyLab in IORegistry" || echo "   ❌ Not in IORegistry"
echo ""

# Check if MIDI Control Center is running (can block DAW port)
echo "3. MIDI Control Center Status:"
pgrep -fl "MIDI Control Center" && echo "   ⚠️  MCC is RUNNING — quit it to free DAW port" || echo "   ✅ MCC not running"
echo ""

# Check if Logic is running
echo "4. Logic Pro Status:"
pgrep -fl "Logic Pro" && echo "   ✅ Logic Pro is running" || echo "   ⚠️  Logic Pro not running"
echo ""

# Check Control Surface prefs
echo "5. Logic Control Surface Prefs:"
if [ -f ~/Library/Preferences/com.apple.logic.pro.cs ]; then
    echo "   ✅ Control Surface prefs exist"
    echo "   If transport doesn't work, delete this file and reconfigure"
else
    echo "   ⚠️  No Control Surface prefs — you'll need to set up Mackie Control"
fi
echo ""

# Quick MIDI device list via system_profiler
echo "6. All MIDI Devices (Audio MIDI Setup should show these):"
system_profiler SPAudioDataType | grep -A 5 "MIDI Devices:" || echo "   Run: open '/System/Applications/Utilities/Audio MIDI Setup.app'"
echo ""

echo "=== Next Steps ==="
echo "1. If KeyLab NOT detected: replug USB, try different port/cable"
echo "2. If MCC running: quit it completely"
echo "3. Open Audio MIDI Setup > Show MIDI Studio > verify two KeyLab ports"
echo "4. Logic > Settings > MIDI > Inputs: enable 'KeyLab Essential 49'"
echo "5. Logic > Control Surfaces > Setup > add 'Mackie Control' using DAW ports"
echo ""
echo "Full guide: ARTURIA-KEYLAB-LOGIC-FIX.md"

# Verify MIDI connection more thoroughly
echo ""
echo "=== Detailed MIDI Connection Check ==="
if system_profiler SPAudioDataType | grep -q "KeyLab Essential 49"; then
    echo "✅ KeyLab detected by macOS Audio subsystem"
    system_profiler SPAudioDataType | grep -A 10 "KeyLab"
else
    echo "❌ KeyLab not detected in audio devices - check USB connection"
fi
echo ""

# Check if DAW button is pressed (KeyLab should show DAW port when active)
echo "=== DAW Mode Check ==="
echo "Make sure the DAW button on your KeyLab Essential 49 is pressed/lit"
echo "You should see 'KeyLab Essential 49 DAW' port in Audio MIDI Setup"
echo ""

# Open Audio MIDI Setup for user
echo "=== Opening Audio MIDI Setup ==="
if [ -d "/System/Applications/Utilities/Audio MIDI Setup.app" ]; then
    open "/System/Applications/Utilities/Audio MIDI Setup.app"
    echo "✅ Opened Audio MIDI Setup"
    echo "   Go to: Window > Show MIDI Studio"
    echo "   Look for: KeyLab Essential 49 and KeyLab Essential 49 DAW"
else
    echo "❌ Audio MIDI Setup not found"
fi
echo ""

# Check for Logic Pro Control Surface conflicts
echo "=== Logic Pro Control Surface Check ==="
if [ -f ~/Library/Preferences/com.apple.logic.pro.cs ]; then
    echo "✅ Control Surface prefs exist"
    echo "   If transport doesn't work, delete: rm ~/Library/Preferences/com.apple.logic.pro.cs"
else
    echo "⚠️  No Control Surface prefs found"
    echo "   You need to set up Mackie Control in Logic"
fi
echo ""

echo "=== Ready! ==="
echo "Next: Open Logic Pro and follow ARTURIA-KEYLAB-LOGIC-FIX.md steps 5-6"
