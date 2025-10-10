#!/usr/bin/env python3
"""
Logic Pro Copilot - Your AI Production Assistant
Makes beatmaking fun again! 🎵
"""

import gradio as gr
import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
from together import Together
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize AI client
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

# Choose which AI to use (priority: Kimi K2 > Anthropic > OpenAI)
if TOGETHER_API_KEY:
    client = Together(api_key=TOGETHER_API_KEY)
    AI_PROVIDER = "kimi"
elif ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    AI_PROVIDER = "anthropic"
elif OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    AI_PROVIDER = "openai"
else:
    client = None
    AI_PROVIDER = None

# System prompt for the AI copilot
SYSTEM_PROMPT = """You are a friendly, encouraging music production copilot for Logic Pro. 

Your user is a beat producer and singer who's brand new to Logic Pro. Your job is to:
- Make beatmaking FUN again
- Give practical, simple advice about production and mixing
- Explain Logic Pro features in beginner-friendly terms
- Encourage experimentation and creativity
- Share production tips and tricks
- Be enthusiastic and supportive

Keep responses concise and actionable. Use emojis when it fits the vibe. Be like a producer friend who's always hyped about music.
"""

# Conversation history
conversation_history = []

def chat_with_copilot(message, history):
    """Chat with the AI copilot about production, Logic Pro, or anything music-related"""
    
    if not client:
        return "⚠️ Please add your API key to the .env file to use the AI copilot. Check config_example.txt for instructions!"
    
    try:
        if AI_PROVIDER == "kimi":
            # Build message history for Kimi K2
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for h in history:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>", "<|eom_id|>"],
                safety_model="moonshotai/Kimi-K2-Instruct"
            )
            reply = response.choices[0].message.content
            
        elif AI_PROVIDER == "anthropic":
            # Build message history for Claude
            messages = []
            for h in history:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
            messages.append({"role": "user", "content": message})
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages
            )
            reply = response.content[0].text
            
        else:  # OpenAI
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for h in history:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=1024
            )
            reply = response.choices[0].message.content
        
        return reply
        
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}\n\nMake sure your API key is set up correctly in .env"


def get_quick_tips():
    """Return random production tips"""
    tips = [
        "🎵 Try the EXS24 sampler - it's perfect for chopping samples and making custom drums",
        "🎹 Use Alchemy for crazy synth sounds - it's one of Logic's most powerful plugins",
        "🥁 Drummer is your friend! It can generate realistic drum patterns to build around",
        "🎚️ Learn the Channel EQ - it's your secret weapon for clean mixes",
        "✨ Press B to show/hide the Smart Controls - great for quick tweaks",
        "🎸 Logic's Amp Designer is amazing for both guitars and lo-fi effects on beats",
        "🔁 Use the loop browser (top right) to find Apple Loops - instant inspiration",
        "💾 Save your channel strip settings - your own custom presets are gold",
        "🎛️ Right-click any knob and select 'Learn' to assign to your MIDI controller",
        "🔊 Use the Compressor's 'Vintage' modes for that warm, analog vibe"
    ]
    import random
    return random.choice(tips)


def scan_sound_packs(sound_packs_dir="sound_packs"):
    """Scan the sound_packs directory and return organized list"""
    sound_packs_path = Path(sound_packs_dir)
    
    if not sound_packs_path.exists():
        sound_packs_path.mkdir(parents=True, exist_ok=True)
        # Create example folders
        (sound_packs_path / "drums").mkdir(exist_ok=True)
        (sound_packs_path / "loops").mkdir(exist_ok=True)
        (sound_packs_path / "one_shots").mkdir(exist_ok=True)
        (sound_packs_path / "vocals").mkdir(exist_ok=True)
        
        return "📁 Sound packs folder created! Add your samples to the 'sound_packs' folder:\n• drums/\n• loops/\n• one_shots/\n• vocals/"
    
    # Scan for audio files
    audio_extensions = {'.wav', '.mp3', '.aif', '.aiff', '.m4a'}
    results = []
    
    for category_dir in sound_packs_path.iterdir():
        if category_dir.is_dir():
            files = [f for f in category_dir.iterdir() 
                    if f.suffix.lower() in audio_extensions]
            
            if files:
                results.append(f"\n**{category_dir.name.upper()}** ({len(files)} files)")
                for f in sorted(files)[:10]:  # Show first 10
                    results.append(f"  • {f.name}")
                if len(files) > 10:
                    results.append(f"  ... and {len(files) - 10} more")
    
    if not results:
        return "📁 No sound packs found yet. Add .wav, .mp3, or .aif files to the sound_packs folder!"
    
    return "\n".join(results)


def create_ui():
    """Create the Gradio interface"""
    
    # Build header with AI provider info
    provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
    ai_status = f"✅ AI: {provider_names.get(AI_PROVIDER, 'Not configured')}" if AI_PROVIDER else "⚠️ AI: Not configured"
    
    with gr.Blocks(theme=gr.themes.Soft(), title="Logic Pro Copilot") as app:
        gr.Markdown(
            f"""
            # 🎵 Logic Pro Copilot
            ### Your AI production assistant - making beatmaking fun again!
            {ai_status}
            """
        )
        
        with gr.Tabs():
            # AI Chat Tab
            with gr.Tab("💬 AI Copilot"):
                gr.Markdown("Ask me anything about production, Logic Pro tips, mixing, or just chat about music!")
                
                chatbot = gr.Chatbot(
                    height=500,
                    placeholder="👋 Hey! I'm your Logic Pro copilot. Ask me anything about beatmaking, Logic Pro features, or production tips!",
                    show_label=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here... (e.g., 'How do I make my 808s hit harder?')",
                        show_label=False,
                        scale=4
                    )
                    submit = gr.Button("Send", scale=1, variant="primary")
                
                # Quick action buttons
                with gr.Row():
                    gr.Button("💡 Give me a tip").click(
                        lambda: get_quick_tips(),
                        outputs=gr.Textbox(label="Quick Tip", lines=2)
                    )
                
                # Handle chat
                msg.submit(chat_with_copilot, [msg, chatbot], [chatbot])
                submit.click(chat_with_copilot, [msg, chatbot], [chatbot])
            
            # Sound Packs Tab
            with gr.Tab("📦 Sound Packs"):
                gr.Markdown(
                    """
                    ### Your Sample Library
                    Browse and manage your sound packs. Just drag samples from here into Logic Pro!
                    """
                )
                
                with gr.Row():
                    scan_btn = gr.Button("🔄 Refresh Sound Packs", variant="primary")
                
                sound_list = gr.Markdown(scan_sound_packs())
                scan_btn.click(scan_sound_packs, outputs=sound_list)
                
                gr.Markdown(
                    """
                    **How to add sounds:**
                    1. Put your samples in the `sound_packs` folder
                    2. Organize them: drums, loops, one_shots, vocals, etc.
                    3. Click refresh to see them here
                    4. Drag files directly from Finder into Logic Pro
                    """
                )
            
            # Loop Generator Tab (Coming Soon)
            with gr.Tab("🎹 AI Loop Generator"):
                gr.Markdown(
                    """
                    ### AI Loop Generator
                    *(Coming in the next update!)*
                    
                    This will let you:
                    - Generate custom drum loops
                    - Create melody loops from text descriptions
                    - AI-powered sound design
                    - One-click export to Logic Pro
                    
                    Stay tuned! 🎵
                    """
                )
            
            # Logic Pro Tips Tab
            with gr.Tab("📚 Quick Start Guide"):
                gr.Markdown(
                    """
                    ### Logic Pro Essentials for Beatmakers
                    
                    #### Getting Started
                    - **Press K** - Turn metronome on/off
                    - **Spacebar** - Play/Stop
                    - **R** - Start recording
                    - **Command + K** - Show/hide virtual keyboard
                    
                    #### Must-Know Tools
                    1. **Drummer** - AI drummer that creates realistic beats
                    2. **Quick Sampler** - Drag any audio to create a playable instrument
                    3. **Step Sequencer** - Perfect for trap/hip-hop drums
                    4. **Alchemy** - Powerful synth for pads and leads
                    5. **EXS24 / Sampler** - Advanced sampling
                    
                    #### Workflow Tips
                    - Use **Apple Loops** (top right) for instant inspiration
                    - **Smart Tempo** automatically matches tempos
                    - **Flex Time** lets you fix timing without re-recording
                    - Create **Track Stacks** to organize similar sounds
                    - Save your favorite plugin settings as **presets**
                    
                    #### Production Tips
                    - 🎚️ Mix at low volume - your ears (and neighbors) will thank you
                    - 🎵 Start with drums and bass - build from the foundation
                    - ✨ Less is more - don't over-complicate the beat
                    - 💾 Save versions as you go - never lose a good idea
                    - 🎧 Reference other tracks - A/B your mix with songs you love
                    
                    **Got questions? Ask the AI Copilot in the chat tab!**
                    """
                )
        
        gr.Markdown(
            """
            ---
            💡 **Pro tip:** Keep this window open while working in Logic Pro for instant help!
            """
        )
    
    return app


if __name__ == "__main__":
    print("🎵 Starting Logic Pro Copilot...")
    print("=" * 50)
    
    if not OPENAI_API_KEY and not ANTHROPIC_API_KEY and not TOGETHER_API_KEY:
        print("⚠️  Warning: No API key found!")
        print("To enable AI chat features:")
        print("1. Copy config_example.txt to .env")
        print("2. Add your API key (OpenAI, Anthropic, or Kimi K2)")
        print("3. Restart the app")
        print("=" * 50)
    elif AI_PROVIDER:
        provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
        print(f"✅ AI Provider: {provider_names.get(AI_PROVIDER, AI_PROVIDER)}")
        print("=" * 50)
    
    app = create_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )

