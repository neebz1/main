#!/bin/bash

# Quick Logic Pro Setup - One Command to Rule Them All

clear

echo "🎹 LOGIC PRO + KEYLAB SETUP ASSISTANT"
echo "══════════════════════════════════════════════════════════════════"
echo ""

# Check if Logic Pro is installed
if [ ! -d "/Applications/Logic Pro.app" ]; then
    echo "❌ Logic Pro not found!"
    echo "   Please install Logic Pro from the App Store first."
    exit 1
fi

echo "✅ Logic Pro found!"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "This script will help you set up:"
echo "  1. Logic Pro templates optimized for your KeyLab"
echo "  2. MIDI controller configuration"
echo "  3. Channel strip presets"
echo "  4. Quick start workflow"
echo ""
echo -e "${YELLOW}Press Enter to continue, or Ctrl+C to cancel${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 1: VERIFY KEYLAB CONNECTION"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "📱 Checking for KeyLab Essential 49..."
echo ""

# Check if MIDI device is connected
if ioreg -c IOUSBDevice | grep -i "keylab" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ KeyLab detected!${NC}"
    DEVICE_NAME=$(ioreg -c IOUSBDevice | grep -i "keylab" -A 5 | grep "USB Product Name" | cut -d'"' -f4)
    echo "   Device: $DEVICE_NAME"
else
    echo -e "${YELLOW}⚠️  KeyLab not detected via USB${NC}"
    echo ""
    echo "Please:"
    echo "  1. Connect your KeyLab Essential 49 to your Mac"
    echo "  2. Use a direct USB connection (no hub if possible)"
    echo "  3. Make sure it's powered on"
    echo ""
    echo -e "${YELLOW}Press Enter when connected, or Ctrl+C to skip${NC}"
    read
fi

echo ""
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 2: OPEN AUDIO MIDI SETUP"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Opening Audio MIDI Setup to verify MIDI connections..."
echo ""
echo "In Audio MIDI Setup:"
echo "  1. Click Window > Show MIDI Studio"
echo "  2. You should see 'KeyLab Essential 49'"
echo "  3. You should also see 'KeyLab Essential 49 DAW'"
echo "  4. If they're grey or missing, click 'Rescan MIDI'"
echo ""

open "/System/Applications/Utilities/Audio MIDI Setup.app"

echo -e "${YELLOW}Verify your KeyLab appears, then press Enter...${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 3: CONFIGURE DAW MODE"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Setting up your KeyLab for Logic Pro control..."
echo ""
echo "📱 If you have Arturia MIDI Control Center:"
echo "  1. Open it"
echo "  2. Select 'KeyLab Essential 49'"
echo "  3. Set DAW Mode to 'Logic Pro' or 'Mackie Control'"
echo "  4. Click 'Store To' (saves to hardware)"
echo "  5. QUIT MIDI Control Center (important!)"
echo ""
echo "📱 On your KeyLab hardware:"
echo "  1. Press the DAW button (should light up)"
echo "  2. This enables transport and fader control"
echo ""
echo -e "${BLUE}If you don't have MIDI Control Center, that's OK!${NC}"
echo "The default settings will work for playing notes."
echo ""
echo -e "${YELLOW}Press Enter when ready...${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 4: OPEN LOGIC PRO"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "🎵 Opening Logic Pro..."
echo ""
echo "I'll wait for Logic to load, then guide you through MIDI setup..."
echo ""

# Open Logic Pro
open -a "Logic Pro"

echo "Waiting for Logic Pro to launch..."
sleep 5

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 5: CONFIGURE LOGIC PRO MIDI SETTINGS"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "In Logic Pro (follow these steps):"
echo ""
echo -e "${GREEN}A. Enable MIDI Input:${NC}"
echo "   Logic Pro > Settings > MIDI > Inputs"
echo "   ✅ Enable 'KeyLab Essential 49'"
echo "   ❌ Disable 'KeyLab Essential 49 DAW' (to avoid double notes)"
echo ""
echo -e "${GREEN}B. Set Up Transport Control (Optional but Recommended):${NC}"
echo "   Logic Pro > Control Surfaces > Setup"
echo "   1. Click 'New' > 'Install' > select 'Mackie Control'"
echo "   2. Click on the new 'Mackie Control' device"
echo "   3. Set Input Port: 'KeyLab Essential 49 DAW'"
echo "   4. Set Output Port: 'KeyLab Essential 49 DAW'"
echo ""
echo -e "${BLUE}This allows Play/Stop/Record buttons on your KeyLab to control Logic!${NC}"
echo ""
echo -e "${YELLOW}Complete the setup in Logic, then press Enter...${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 6: TEST YOUR SETUP"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Let's test that everything works!"
echo ""
echo "In Logic Pro:"
echo "  1. Create a new Software Instrument track (Command+Option+S)"
echo "  2. Record-enable it (red button on track)"
echo "  3. Play some keys on your KeyLab"
echo ""
echo "✅ You should hear sound!"
echo ""
echo "Also test:"
echo "  - Press Play on KeyLab → Logic should play"
echo "  - Press Stop on KeyLab → Logic should stop"
echo "  - Move a fader → Logic mixer should respond"
echo ""
echo -e "${GREEN}Does it work? (y/n)${NC}"
read -r WORKS

if [[ $WORKS =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}🎉 Excellent! Your KeyLab is fully configured!${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Troubleshooting needed.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Notes don't play: Check Logic Pro > Settings > MIDI > Inputs"
    echo "  - Transport doesn't work: Check Control Surfaces setup"
    echo "  - Nothing works: Restart Logic Pro and try again"
    echo ""
    echo "Full guide available at:"
    echo "  ARTURIA-KEYLAB-LOGIC-FIX.md"
    echo ""
    echo -e "${YELLOW}Press Enter to continue anyway...${NC}"
    read
fi

clear

echo "══════════════════════════════════════════════════════════════════"
echo "STEP 7: CREATE YOUR FIRST TEMPLATE"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "🎵 Let's create a production-ready template!"
echo ""
echo "I recommend starting with: MIDI BEAT PRODUCTION"
echo ""
echo -e "${GREEN}Template setup (in Logic Pro):${NC}"
echo ""
echo "1. File > New > Empty Project"
echo ""
echo "2. Create these 8 Software Instrument tracks:"
echo "   • Drums (Choose: Drummer or drum kit)"
echo "   • 808 Bass (Choose: Alchemy > Bass > 808)"
echo "   • Synth Lead (Choose: Alchemy > Lead)"
echo "   • Synth Pad (Choose: Alchemy > Pad)"
echo "   • Keys (Choose: Studio Piano)"
echo "   • Pluck (Choose: Retro Synth)"
echo "   • FX (Choose: any FX preset)"
echo "   • Sampler (Choose: Quick Sampler - leave empty)"
echo ""
echo "3. Create 4 Audio tracks for recording/samples"
echo ""
echo "4. Color code your tracks:"
echo "   Right-click track header > Assign Track Color"
echo "   • Drums: Red"
echo "   • Bass: Orange  "
echo "   • Synths: Blue"
echo "   • Vocals/Audio: Green"
echo ""
echo "5. Save as template:"
echo "   File > Save As Template..."
echo "   Name it: 'MIDI Beat Production'"
echo ""
echo "6. Done! Now you can use this template anytime:"
echo "   File > New From Template > MIDI Beat Production"
echo ""
echo -e "${YELLOW}Press Enter when you've saved the template...${NC}"
read

clear

echo "══════════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "🎉 Your Logic Pro + KeyLab setup is ready!"
echo ""
echo -e "${GREEN}What you can do now:${NC}"
echo ""
echo "  🎹 Play MIDI with your KeyLab"
echo "  🎛️  Control Logic with transport buttons"
echo "  🎵 Use your custom template (File > New From Template)"
echo "  🔊 Record audio and MIDI"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "  1. Create more templates using the guide:"
echo "     open ~/Music/Audio\ Music\ Apps/Project\ Templates/Custom\ Templates/TEMPLATE_GUIDE.txt"
echo ""
echo "  2. Save custom channel strips for faster workflow"
echo ""
echo "  3. Map Smart Controls to your KeyLab knobs:"
echo "     Press B in Logic > External Assignment"
echo ""
echo "  4. Start making beats!"
echo ""
echo -e "${GREEN}Template guides available:${NC}"
echo "  - MIDI Beat Production"
echo "  - Live Recording + MIDI"
echo "  - Quick Sketch"
echo "  - Sample Chop & Flip"
echo "  - MIDI Orchestra"
echo ""
echo "All guides saved to:"
echo "  ~/Music/Audio Music Apps/Project Templates/Custom Templates/"
echo ""
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "🎵 Happy producing! Your Mac is ready to create! 🚀"
echo ""

