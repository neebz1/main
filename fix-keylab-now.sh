#!/bin/bash
# Emergency KeyLab Essential 49 fix for Logic Pro

echo "=== KeyLab Essential 49 Emergency Fix ==="
echo ""

# Step 1: Reset macOS MIDI drivers
echo "1️⃣ Resetting macOS MIDI drivers..."
launchctl kickstart -k system/com.apple.audio.coreaudiod 2>/dev/null || sudo launchctl kickstart -k system/com.apple.audio.coreaudiod
sleep 2
echo "   ✅ Audio/MIDI driver restarted"
echo ""

# Step 2: Open Audio MIDI Setup to verify ports
echo "2️⃣ Opening Audio MIDI Setup..."
open "/System/Applications/Utilities/Audio MIDI Setup.app"
echo "   📋 In Audio MIDI Setup:"
echo "      - Go to: Window > Show MIDI Studio"
echo "      - Look for: 'KeyLab Essential 49' and 'KeyLab Essential 49 DAW'"
echo "      - If grey or missing, click 'Rescan MIDI' button"
echo ""

# Step 3: Check if we need to delete corrupted prefs
echo "3️⃣ Checking Logic Control Surface prefs..."
if [ -f ~/Library/Preferences/com.apple.logic.pro.cs ]; then
    echo "   Found existing Control Surface config"
    echo "   If transport doesn't work after setup, run:"
    echo "   rm ~/Library/Preferences/com.apple.logic.pro.cs"
fi
echo ""

# Step 4: Instructions for Logic
echo "4️⃣ Now in Logic Pro, do these 3 things:"
echo ""
echo "   A) Enable MIDI input:"
echo "      Logic Pro > Settings > MIDI > Inputs"
echo "      ✅ Check: 'KeyLab Essential 49'"
echo "      ❌ Uncheck: 'KeyLab Essential 49 DAW' (to avoid double triggers)"
echo ""
echo "   B) Add Mackie Control for transport/faders:"
echo "      Logic Pro > Control Surfaces > Setup"
echo "      Click: New > Install > select 'Mackie Control'"
echo "      Set BOTH ports to: 'KeyLab Essential 49 DAW'"
echo "         Input Port: KeyLab Essential 49 DAW"
echo "         Output Port: KeyLab Essential 49 DAW"
echo ""
echo "   C) Test it:"
echo "      - Create Software Instrument track"
echo "      - Record-arm it"
echo "      - Play keys → should hear sound"
echo "      - Press Play/Stop on KeyLab → should control Logic transport"
echo ""

# Step 5: Press DAW button on keyboard
echo "5️⃣ IMPORTANT: Press the DAW button on your KeyLab!"
echo "   The DAW button should light up on the keyboard"
echo "   This activates Logic/Mackie mode"
echo ""

echo "==================================================================="
echo "If keys still don't work after this:"
echo "1. Unplug KeyLab, wait 5 seconds, replug"
echo "2. Try a different USB port"
echo "3. Restart Mac"
echo "==================================================================="


