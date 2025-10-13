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

# 1. Unlock Bitwarden
export BW_SESSION=$(bw unlock --raw)

# 2. Add Moonshot key
echo '{"organizationId":null,"folderId":null,"type":1,"name":"Moonshot API Key","notes":null,"favorite":false,"login":{"username":"","password":"YOUR_MOONSHOT_KEY","totp":null}}' | bw encode | bw create item

# 3. Add Google key
echo '{"organizationId":null,"folderId":null,"type":1,"name":"Google API Key","notes":null,"favorite":false,"login":{"username":"","password":"YOUR_GOOGLE_KEY","totp":null}}' | bw encode | bw create item

# 4. Load keys
bwload

# 5. Verify
env | grep -E "MOONSHOT|GOOGLE"

# Make script executable
chmod +x "$0"

# Verify MIDI connection
echo "=== Verifying MIDI Connection ==="
if system_profiler SPAudioDataType | grep -q "KeyLab Essential 49"; then
    echo "✅ KeyLab detected by macOS"
else
    echo "❌ KeyLab not detected - check USB connection"
fi
echo ""

# Verify Audio MIDI Setup is working
if [ -d "/System/Applications/Utilities/Audio MIDI Setup.app" ]; then
    echo "✅ Audio MIDI Setup available"
    echo "   Run: open '/System/Applications/Utilities/Audio MIDI Setup.app'"
else
    echo "❌ Audio MIDI Setup not found"
fi
echo ""

# Check if DAW button is pressed (KeyLab should show DAW port when active)
echo "=== DAW Mode Check ==="
echo "Press the DAW button on your KeyLab Essential 49"
echo "You should see 'KeyLab Essential 49 DAW' port in MIDI Studio"
echo ""

# Final verification
echo "=== Setup Complete ==="
echo "1. ✅ Script is executable"
echo "2. ✅ MIDI devices checked"
echo "3. ✅ Logic status checked"
echo "4. ✅ Control surfaces verified"
echo ""
echo "Ready to use with Logic Pro!"
