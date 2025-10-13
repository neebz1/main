# KeyLab Essential 49 → Logic Pro — Fast Fix

## 1. Physical connection
- Unplug keyboard, plug directly into Mac (no hub), use good USB cable
- System Settings > Privacy & Security > "Allow accessories to connect" → set to "Ask" and approve

## 2. Arturia MIDI Control Center
```bash
# Download/install from arturia.com if you don't have it
open -a "MIDI Control Center"
```
- Select KeyLab Essential 49
- Set DAW Mode to "Logic Pro" or "Mackie Control"
- Click "Store To" to save to hardware
- **QUIT MCC completely** (it blocks the DAW port)

## 3. Press DAW button on keyboard
- Physical DAW button on the KeyLab should light up (enables Logic mode)

## 4. Verify macOS sees MIDI
```bash
# Open Audio MIDI Setup
open "/System/Applications/Utilities/Audio MIDI Setup.app"
```
- Window > Show MIDI Studio
- You should see "KeyLab Essential 49" and "KeyLab Essential 49 DAW"
- If missing or grey: click Rescan MIDI; if still missing: restart Mac

## 5. Logic — Enable note input
**Logic Pro > Settings > MIDI > Inputs:**
- ✅ Enable "KeyLab Essential 49"
- ❌ Disable "KeyLab Essential 49 DAW" (to avoid double triggers)

**Test:**
- Create Software Instrument track
- Record-arm it
- Play keys → should hear sound

## 6. Logic — Enable transport/faders
**Logic Pro > Control Surfaces > Setup:**
- Click "New" > "Install" > select "Mackie Control"
- Click the new Mackie Control device
- Set ports:
  - **Input Port:** `KeyLab Essential 49 DAW`
  - **Output Port:** `KeyLab Essential 49 DAW`

**Test:**
- Press Play/Stop/Record on KeyLab → should control Logic transport
- Move faders → should control Logic mixer

## 7. Still broken? Nuclear reset
```bash
# Close Logic first, then run:
rm ~/Library/Preferences/com.apple.logic.pro.cs
```
- Reopen Logic
- Repeat step 6 (add Mackie Control + set DAW ports)

## 8. Common port name variations
If you don't see "KeyLab Essential 49 DAW", look for:
- `MIDIIN2 (KeyLab Essential 49)`
- `MIDIOUT2 (KeyLab Essential 49)`
- Use those for the Mackie Control ports

## 9. Troubleshooting
| Problem | Fix |
|---------|-----|
| Notes work, transport doesn't | Step 6: add Mackie Control, use DAW ports |
| Nothing works | Steps 1-4: cable/driver/DAW mode |
| Faders move wrong channels | Control Surfaces > Rebuild Defaults |
| "Port in use" error | Quit MCC, Ableton, other DAWs |
| Grey in MIDI Studio | Rescan MIDI; different USB port; restart |

---

**Done correctly:**
- Keys play notes (using "KeyLab Essential 49" port)
- Transport buttons work (using "KeyLab Essential 49 DAW" port via Mackie Control)
- Faders control mixer (same DAW port)

If step X fails, tell me which one and what error/symptom you see.


./setup-api-keys.sh
