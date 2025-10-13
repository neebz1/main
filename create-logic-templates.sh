#!/bin/bash

# Logic Pro Template Creator
# Creates production-ready templates optimized for MIDI controllers

echo "🎹 Creating Logic Pro Templates for Your KeyLab..."
echo "=================================================="

# Template directories
LOGIC_TEMPLATES="$HOME/Music/Audio Music Apps/Project Templates/Custom Templates"
PLUGIN_SETTINGS="$HOME/Music/Audio Music Apps/Plug-In Settings"
CHANNEL_STRIPS="$HOME/Music/Audio Music Apps/Channel Strip Settings"

# Create directories if they don't exist
mkdir -p "$LOGIC_TEMPLATES"
mkdir -p "$PLUGIN_SETTINGS"
mkdir -p "$CHANNEL_STRIPS"

echo ""
echo "📁 Template Directories:"
echo "  Templates: $LOGIC_TEMPLATES"
echo "  Plug-ins:  $PLUGIN_SETTINGS"
echo "  Strips:    $CHANNEL_STRIPS"
echo ""

# Function to create AppleScript template
create_template() {
    local TEMPLATE_NAME=$1
    local TRACK_CONFIG=$2

    echo "Creating template: $TEMPLATE_NAME"

    osascript <<EOF
tell application "Logic Pro"
    activate
    delay 2

    -- Create new project
    tell application "System Events"
        keystroke "n" using {command down}
        delay 1

        -- Select Empty Project
        key code 36 -- Return
        delay 1
    end tell

    -- Project will open with track chooser
    -- We'll configure it via System Events
    tell application "System Events"
        tell process "Logic Pro"
            -- Configure based on template type
            delay 1

            -- Click Create button
            keystroke return
        end tell
    end tell

    delay 2

    -- Save as template
    tell application "System Events"
        tell process "Logic Pro"
            keystroke "s" using {command down, shift down}
            delay 1

            -- Type template name
            keystroke "$TEMPLATE_NAME"
            delay 0.5

            keystroke return
        end tell
    end tell

end tell
EOF
}

echo "🎵 OPTION 1: Manual Template Creation (Recommended)"
echo "=================================================="
echo ""
echo "I'll guide you through creating templates manually since"
echo "it gives you better control and won't interfere with Logic."
echo ""
echo "Templates to create:"
echo ""

cat > "$LOGIC_TEMPLATES/TEMPLATE_GUIDE.txt" << 'GUIDE'
🎹 LOGIC PRO TEMPLATES FOR YOUR KEYLAB ESSENTIAL 49

Quick Start: Open Logic Pro and create these templates manually for best results.
Each template is optimized for your MIDI controller workflow.

════════════════════════════════════════════════════════════════════════

TEMPLATE 1: "MIDI Beat Production"
────────────────────────────────────
Perfect for: Hip-hop, trap, electronic beats
Tracks: 8 MIDI + 4 Audio

Setup Steps:
1. Logic Pro > New Project > Empty Project
2. Create these tracks:

   MIDI Tracks:
   - Drums (Drummer or EXS24 with drum kit)
   - 808 Bass (Alchemy or SubBoomBass)
   - Synth Lead (Alchemy preset)
   - Synth Pad (Alchemy preset)
   - Keys/Piano (Stock Logic piano)
   - Pluck/Arp (Retro Synth)
   - FX/Riser (stock effects)
   - Sampler (Quick Sampler - empty, ready for drops)

   Audio Tracks:
   - Vocals/Recording
   - Sample 1
   - Sample 2
   - Master Bus Processing

3. Set all MIDI tracks to receive from "All"
4. Color code:
   - Drums: Red
   - Bass: Orange
   - Synths: Blue
   - Vocals: Green

5. Save As Template:
   File > Save As Template > "MIDI Beat Production"

MIDI Controller Mapping:
- Pads → Drums track
- Faders 1-8 → Track volumes
- Knobs 1-4 → Plugin parameters (learn mode)
- Transport → Play/Stop/Record

════════════════════════════════════════════════════════════════════════

TEMPLATE 2: "Live Recording + MIDI"
────────────────────────────────────
Perfect for: Recording vocals/instruments with MIDI backing
Tracks: 4 MIDI + 8 Audio

Setup Steps:
1. Logic Pro > New Project > Empty Project
2. Create these tracks:

   MIDI Tracks:
   - Drums/Beat
   - Bass
   - Keys
   - Synth/Pad

   Audio Tracks:
   - Lead Vocal (Comp)
   - Vocal Double
   - Ad-libs
   - Guitar/Instrument 1
   - Guitar/Instrument 2
   - Harmony Vocal
   - FX/Texture
   - Reference Track

3. Set up vocal chain on Lead Vocal:
   - Channel EQ (default)
   - Compressor (Platinum Digital)
   - DeEsser
   - Space Designer (small room)

4. Enable "Low Latency Mode" for recording
5. Save As Template: "Live Recording + MIDI"

MIDI Controller Mapping:
- Keys → Currently selected MIDI track
- Faders → Recording track levels
- Record button → Record enable selected track

════════════════════════════════════════════════════════════════════════

TEMPLATE 3: "Quick Sketch / Idea Capture"
──────────────────────────────────────────
Perfect for: Fast idea capture, jamming
Tracks: 4 MIDI instruments ready to play

Setup Steps:
1. Logic Pro > New Project > Empty Project
2. Create these tracks with NO plugins (fast load):

   - Quick Sketch Drums (Drummer - Auto Drummer)
   - Quick Bass (Classic Electric Piano - transpose down)
   - Quick Keys (Studio Piano)
   - Quick Synth (Retro Synth - simple saw)

3. Enable Smart Tempo (to match any loops you drag in)
4. Set tempo to 120 BPM (neutral starting point)
5. Turn on Loop mode with 8-bar loop
6. Enable Count-In
7. Save As Template: "Quick Sketch"

Workflow:
- Press Record and JAM
- Loop records automatically stack takes
- Transpose bass with pitch wheel
- Save ideas in seconds

════════════════════════════════════════════════════════════════════════

TEMPLATE 4: "Sample Chop & Flip"
─────────────────────────────────
Perfect for: Chopping samples, boom-bap, lo-fi
Tracks: Specialized for sampling

Setup Steps:
1. Logic Pro > New Project > Empty Project
2. Create these tracks:

   - Drum Machine Designer (custom kit ready)
   - Quick Sampler 1 (drop sample here)
   - Quick Sampler 2
   - Quick Sampler 3
   - Quick Sampler 4
   - Bass (for sub bass under samples)
   - FX Stack (reverb, delay, vinyl sim)
   - Master Processing

3. Add to Master:
   - Vintage EQ
   - Vintage Compressor
   - Bitcrusher (off by default)

4. Enable Flex Pitch on all samplers
5. Save As Template: "Sample Chop & Flip"

Workflow:
- Drag sample into Quick Sampler
- Use Classic mode or Slice mode
- Play sample with MIDI controller
- Chop and rearrange via piano roll

════════════════════════════════════════════════════════════════════════

TEMPLATE 5: "MIDI Orchestra / Layers"
──────────────────────────────────────
Perfect for: Layered sounds, experimental
Tracks: 16 MIDI tracks for massive sounds

Setup Steps:
1. Logic Pro > New Project > Empty Project
2. Create 16 MIDI tracks with these assignments:

   Layers 1-4: Synth Stack
   - Alchemy (evolving pad)
   - Retro Synth (analog warmth)
   - ES2 (bright layer)
   - FM Synth (texture)

   Layers 5-8: Rhythm Section
   - Drums
   - Perc 1
   - Perc 2
   - Bass

   Layers 9-12: Melodic
   - Lead 1
   - Lead 2
   - Pluck
   - Arp

   Layers 13-16: Texture
   - Pad
   - FX 1
   - FX 2
   - Sampler

3. Group similar tracks into Track Stacks
4. Color code by function
5. Save As Template: "MIDI Orchestra"

MIDI Controller:
- Play across all tracks at once
- Use faders to balance layers
- Solo/mute to build arrangement

════════════════════════════════════════════════════════════════════════

BONUS: MIDI Controller Smart Controls Setup
────────────────────────────────────────────

For ANY template, map your KeyLab knobs/faders:

1. Open Smart Controls (press B)
2. Click the inspector icon (top left)
3. Click "External Assignment"
4. Move a knob on your KeyLab
5. It auto-assigns!

Common Mappings:
- Knob 1: Filter Cutoff
- Knob 2: Resonance
- Knob 3: Reverb Send
- Knob 4: Delay Send
- Faders 1-8: Track Volumes
- Pads: Trigger samples/loops

════════════════════════════════════════════════════════════════════════

Quick Reference - Template Usage:

1. Launch Logic Pro
2. File > New From Template
3. Choose your template
4. Start creating!

All templates are set up to work perfectly with your KeyLab Essential 49.
Just plug in and play!

════════════════════════════════════════════════════════════════════════

Created with ❤️ for your production workflow
GUIDE

echo "✅ Created: TEMPLATE_GUIDE.txt"

# Create MIDI learn script
cat > "$LOGIC_TEMPLATES/MIDI_SETUP_CHECKLIST.txt" << 'CHECKLIST'
🎹 KEYLAB ESSENTIAL 49 - LOGIC PRO SETUP CHECKLIST

Before using templates, verify your KeyLab is set up correctly:

□ Step 1: Physical Connection
  - KeyLab plugged directly into Mac (no hub)
  - USB cable is good quality
  - Green light on KeyLab is on

□ Step 2: System Settings
  - System Settings > Privacy & Security
  - "Allow accessories to connect" → set to "Ask"
  - Approve KeyLab when prompted

□ Step 3: Arturia MIDI Control Center
  - Open MIDI Control Center app
  - Select "KeyLab Essential 49"
  - Set DAW Mode to "Logic Pro" or "Mackie Control"
  - Click "Store To" (saves to hardware)
  - QUIT MIDI Control Center completely

□ Step 4: Press DAW Button
  - Physical DAW button on KeyLab should light up
  - This enables transport/fader control

□ Step 5: Logic MIDI Inputs
  - Logic Pro > Settings > MIDI > Inputs
  - ✅ Enable "KeyLab Essential 49"
  - ❌ Disable "KeyLab Essential 49 DAW" (avoids doubles)

□ Step 6: Logic Control Surfaces
  - Logic Pro > Control Surfaces > Setup
  - Click "New" > "Install" > "Mackie Control"
  - Set Input Port: "KeyLab Essential 49 DAW"
  - Set Output Port: "KeyLab Essential 49 DAW"

□ Step 7: Test Everything
  - Create Software Instrument track
  - Record-arm it
  - Play keys → should hear sound ✓
  - Press Play on KeyLab → Logic plays ✓
  - Move fader → Logic volume changes ✓

════════════════════════════════════════════════════════════════════════

If something doesn't work:

Keys don't make sound:
→ Check Step 5 (enable MIDI input)

Transport buttons don't work:
→ Check Step 6 (Mackie Control setup)

Faders don't control Logic:
→ Check Step 3 (DAW mode) and Step 4 (DAW button)

Nothing works at all:
→ Restart Mac, start from Step 1

════════════════════════════════════════════════════════════════════════

Once setup is complete, all templates will work perfectly with your KeyLab!
CHECKLIST

echo "✅ Created: MIDI_SETUP_CHECKLIST.txt"

# Create a quick launch script
cat > "$LOGIC_TEMPLATES/open-template.sh" << 'LAUNCH'
#!/bin/bash
# Quick Template Launcher

echo "🎹 Logic Pro Template Launcher"
echo "=============================="
echo ""
echo "Available templates:"
echo "1. MIDI Beat Production"
echo "2. Live Recording + MIDI"
echo "3. Quick Sketch"
echo "4. Sample Chop & Flip"
echo "5. MIDI Orchestra"
echo ""
echo "To use templates:"
echo "1. Open Logic Pro"
echo "2. File > New From Template"
echo "3. Choose your template"
echo ""

open -a "Logic Pro"
LAUNCH

chmod +x "$LOGIC_TEMPLATES/open-template.sh"
echo "✅ Created: open-template.sh"

# Create channel strip presets info
cat > "$CHANNEL_STRIPS/CUSTOM_STRIPS_README.txt" << 'STRIPS'
🎛️ CUSTOM CHANNEL STRIPS FOR LOGIC PRO

Channel Strips are pre-configured plugin chains you can load instantly.

To Create Custom Channel Strips:
════════════════════════════════════════════════════════════════════════

1. Set up a track with plugins you like
2. Click the "Channel Strip" dropdown (top of inspector)
3. "Save Channel Strip Setting..."
4. Name it and save

Recommended Channel Strips to Create:
────────────────────────────────────────────────────────────────────────

"Vocal - Clean & Bright"
  - Channel EQ (cut lows below 80Hz)
  - Compressor (Platinum Digital, ratio 3:1)
  - DeEsser (default)
  - Space Designer (small room)

"808 Bass - Heavy"
  - EQ (boost 40-60Hz, cut 200-400Hz)
  - Overdrive (subtle saturation)
  - Compressor (high ratio for punch)

"Synth Lead - Cutting"
  - EQ (boost 2-5kHz for presence)
  - Compressor (fast attack)
  - Stereo Delay (1/8 note)
  - Reverb (small, short decay)

"Drums - Punchy"
  - Compressor (fast attack, medium ratio)
  - Transient Designer
  - EQ (boost 60Hz and 5kHz)

"Lo-Fi Everything"
  - Bitcrusher
  - Vinyl simulator
  - Vintage EQ
  - Tape delay

════════════════════════════════════════════════════════════════════════

Once saved, load them from:
Library > Channel Strip > User Patches > [Your Name]

Saves you hours of plugin configuration!
STRIPS

echo "✅ Created: CUSTOM_STRIPS_README.txt"

echo ""
echo "=================================================="
echo "✅ Template Setup Complete!"
echo "=================================================="
echo ""
echo "📄 Created guides in:"
echo "   $LOGIC_TEMPLATES"
echo ""
echo "📖 Next steps:"
echo ""
echo "1. Read the guides:"
echo "   open '$LOGIC_TEMPLATES/TEMPLATE_GUIDE.txt'"
echo ""
echo "2. Verify MIDI setup:"
echo "   open '$LOGIC_TEMPLATES/MIDI_SETUP_CHECKLIST.txt'"
echo ""
echo "3. Open Logic Pro and create templates:"
echo "   open -a 'Logic Pro'"
echo ""
echo "4. Follow the template creation steps in the guide"
echo ""
echo "💡 Pro Tip: Start with 'MIDI Beat Production' template"
echo "   It's the most versatile for your workflow!"
echo ""

