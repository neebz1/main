#!/bin/bash
# Create a shortcuts wallpaper image

cat > /tmp/shortcuts.txt << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🎹 AI MUSIC STUDIO - KEYBOARD SHORTCUTS 🎹          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════

🎹 LOGIC PRO COPILOT                    ⌃⌥M
   Your AI music production assistant
   Port: 7860 | Login: admin/[your-password]

🎚️ AI MIXING ENGINEER                   ⌃⌥E
   Professional audio analysis & suggestions
   Port: 7861 | Login: admin/[your-password]

☁️ CLOUD AI BUILDER                      ⌃⌥C
   Build features remotely with AI
   Port: 7862 | Login: admin/[your-password]

🔌 REST API SERVER                       ⌃⌥A
   Backend API with authentication
   Port: 8000 | Docs: /docs

📊 SECURITY CHECK                        ⌃⌥S
   Run security audit

═══════════════════════════════════════════════════════════════════

📁 QUICK TERMINAL COMMANDS:

cd /Users/nr/Documents/GitHub/main

./start-music-ai.sh                Start Logic Pro Copilot
./start-ai-mixing-engineer.sh      Start AI Mixing Engineer
./start-cloud-builder.sh           Start Cloud Builder
./start-api.sh                     Start REST API
./security-check.sh                Security Audit
python3 setup_wizard.py            Setup Wizard

═══════════════════════════════════════════════════════════════════

🎛️ LOGITECH MX KEYS MINI SHORTCUTS:

F1  →  Launch Music AI
F2  →  Launch Mixing AI
F3  →  Launch Cloud Builder
F4  →  Open Logic Pro
F5  →  Start/Stop Recording
F6  →  Play/Pause
F7  →  Open Finder (sound_packs)
F8  →  Security Check

═══════════════════════════════════════════════════════════════════

🖱️ LOGITECH MX MOUSE SHORTCUTS:

Button 4 (Side) →  Next Track
Button 5 (Side) →  Previous Track
Middle Click   →  Open Terminal

═══════════════════════════════════════════════════════════════════

🎹 LOGIC PRO MIDI KEYBOARD:

C1  →  Kick Drum
D1  →  Snare
E1  →  Hi-Hat Closed
F1  →  Hi-Hat Open
G1  →  Clap
A1  →  Crash

C2+ →  Melodic Instruments (Auto-mapped)

═══════════════════════════════════════════════════════════════════

🔑 IMPORTANT FILES:

.env                          Your API keys & passwords
YOUR-ORGANIZED-ENVIRONMENT.md Complete guide
SHORTCUTS.md                  Detailed shortcuts
setup_wizard.py               Interactive setup (Port 7777)

═══════════════════════════════════════════════════════════════════

🎵 READY TO MAKE MUSIC! 🎵

Your complete AI music studio is set up and ready to go!
All apps are password-protected for security.
Check YOUR-ORGANIZED-ENVIRONMENT.md for detailed instructions.

═══════════════════════════════════════════════════════════════════
EOF

echo "✅ Shortcuts reference created at /tmp/shortcuts.txt"
echo "📋 Copy this to your desktop or set as wallpaper!"
cat /tmp/shortcuts.txt

