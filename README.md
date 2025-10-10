# 🎵 Logic Pro Copilot

Your AI production assistant that makes beatmaking fun again! A friendly companion app for Logic Pro that helps you learn, create, and vibe while producing music.

## What It Does

- **💬 AI Chat** - Ask anything about production, Logic Pro, mixing, sound design
- **📦 Sound Pack Browser** - Organize and access all your samples in one place
- **🎹 AI Loop Generator** - (Coming soon) Generate custom loops and sounds
- **📚 Quick Start Guide** - Logic Pro tips and shortcuts for beginners
- **💡 Production Tips** - Get instant advice and workflow improvements

## Quick Start

### 1. Install Python
Make sure you have Python 3.9+ installed:
```bash
python3 --version
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Set Up Your AI API Key (Optional but Recommended)

The AI chat features need an API key. Choose ONE of these providers:

**Option A: Kimi K2 (via Together AI) - Fast & Affordable**
1. Get an API key from: https://api.together.ai/settings/api-keys
2. Create a file called `.env` in this folder
3. Add: `TOGETHER_API_KEY=your_key_here`

**Option B: OpenAI (GPT-4)**
1. Get an API key from: https://platform.openai.com/api-keys
2. Create a file called `.env` in this folder
3. Add: `OPENAI_API_KEY=your_key_here`

**Option C: Anthropic (Claude)**
1. Get an API key from: https://console.anthropic.com/
2. Create a file called `.env` in this folder
3. Add: `ANTHROPIC_API_KEY=your_key_here`

See `config_example.txt` for a template.

### 4. Run It!
```bash
python3 logic_copilot.py
```

The app will open in your browser at `http://localhost:7860`

## How to Use

### Adding Sound Packs
1. Put your audio samples in the `sound_packs` folder
2. Organize by category (drums, loops, one_shots, vocals, etc.)
3. Click "Refresh" in the Sound Packs tab
4. Drag files from Finder directly into Logic Pro!

### Using the AI Copilot
Keep the app open while you produce. Ask questions like:
- "How do I make my 808s hit harder?"
- "What's the best way to layer vocals?"
- "How do I use the compressor in Logic Pro?"
- "Give me some creative ideas for this beat"

### Workflow Tips
- Keep Logic Pro Copilot open on a second monitor (or split screen)
- Use it as your production buddy - ask questions as they come up
- Get random tips for inspiration when you're stuck
- Learn Logic Pro features as you need them

## Features

✅ AI production assistant with chat interface  
✅ Sound pack browser and organizer  
✅ Built-in Logic Pro quick start guide  
✅ Production tips and tricks  
🔄 AI loop generation (coming soon)  
🔄 Automatic Logic Pro integration (coming soon)  
🔄 MIDI pattern generator (coming soon)  

## Requirements

- macOS (for Logic Pro)
- Python 3.9 or higher
- API key for AI features (Kimi K2, OpenAI, or Anthropic) - see `AI_PROVIDERS.md`
- Logic Pro X or Logic Pro 11

## Project Structure

```
logic-pro-copilot/
├── logic_copilot.py      # Main application
├── requirements.txt      # Python dependencies
├── config_example.txt    # API key template
├── sound_packs/          # Your sample library
│   ├── drums/
│   ├── loops/
│   ├── one_shots/
│   └── vocals/
└── README.md            # This file
```

## Troubleshooting

**"No API key found" warning**
- Make sure you created a `.env` file (not `.env.txt`)
- Check that your API key is valid
- Restart the app after adding the key

**Sound packs not showing**
- Make sure audio files are in supported formats (.wav, .mp3, .aif, .aiff)
- Click the refresh button
- Check that files are in subdirectories of `sound_packs/`

**Port already in use**
- Another app is using port 7860
- Edit `logic_copilot.py` and change `server_port=7860` to another number

## Tips for Beginners

1. **Start Simple** - Don't try to learn everything at once
2. **Ask Questions** - The AI copilot is here to help, no question is too basic
3. **Experiment** - Try different sounds and see what happens
4. **Save Often** - Use Save As to create versions
5. **Have Fun** - Music production should be enjoyable!

## Future Features

- Real-time Logic Pro monitoring
- AI-generated drum patterns and loops
- Automatic sample organization
- MIDI pattern generator
- Mix assistant with frequency analysis
- Collaborative session features
- Custom plugin presets

## Made With

- Python 3
- Gradio (UI framework)
- OpenAI GPT-4 / Anthropic Claude
- Love for music production ❤️

---

**Happy beatmaking!** 🎵

If you have ideas or feedback, feel free to customize this for your workflow.
