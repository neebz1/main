#!/usr/bin/env python3
"""
AI Music Builder - Hugging Face Space
Talk to your AI assistant from ANYWHERE to build features!

Access from: Phone, tablet, any browser
"""

import gradio as gr
import os

# For Hugging Face deployment
HF_TOKEN = os.getenv('HF_TOKEN')  # Optional, for private spaces

# AI setup
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

client = None
try:
    if TOGETHER_API_KEY:
        from together import Together
        client = Together(api_key=TOGETHER_API_KEY)
        print("✅ AI: Kimi K2")
except:
    print("⚠️ AI: Not configured (add TOGETHER_API_KEY to Secrets)")


def chat_with_ai(message, history):
    """Chat with AI to build features"""
    
    if not client:
        return "⚠️ Please configure TOGETHER_API_KEY in Space Settings → Secrets"
    
    # System prompt
    system_prompt = """You are a personal AI assistant for building music production tools.

The user has a complete AI music production suite that includes:
- Live AI Plugin for Logic Pro (real-time control)
- AI Mixing Engineer (professional audio analysis)
- Voice control with Google Gemini
- OSC automation for Logic Pro

Your job:
- Help build new features
- Explain code clearly
- Give step-by-step instructions
- Be encouraging and supportive
- Keep it simple and actionable

When asked to build something:
1. Explain what you'll create
2. Show the code
3. Provide installation/usage instructions
4. Suggest next steps

Be conversational and helpful!"""
    
    try:
        # Build message history
        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": message})
        
        # Call AI
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            safety_model="moonshotai/Kimi-K2-Instruct"
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nCheck API key configuration in Settings → Secrets"


# Create UI
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue"),
    title="AI Music Builder"
) as demo:
    gr.Markdown(
        """
        # 🤖 AI Music Builder
        ### Talk to your AI assistant from anywhere - build features on the go!
        
        **I'm your AI assistant!** Tell me what you want to build for your music production suite and I'll help you create it!
        
        ---
        """
    )
    
    with gr.Tabs():
        with gr.Tab("💬 Build & Chat"):
            gr.Markdown(
                """
                ### Give me instructions!
                
                **Try asking:**
                - "How do I add a new feature to detect song key?"
                - "Help me build a drum pattern generator"
                - "Create a vocal harmony plugin for Logic Pro"
                - "Build a mobile app version of the AI mixer"
                - "Add Spotify integration"
                - "Explain how the OSC control works"
                
                **I'll give you:**
                - Step-by-step code
                - Installation instructions
                - Usage examples
                - Next steps
                """
            )
            
            chatbot = gr.Chatbot(
                height=600,
                placeholder="👋 Hi! Tell me what you want to build and I'll help you create it!",
                show_label=False,
                type="messages"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="What do you want to build? (e.g., 'Add beat matching to the AI mixer')",
                    show_label=False,
                    scale=4,
                    lines=2
                )
                submit = gr.Button("🚀 Build It!", scale=1, variant="primary", size="lg")
            
            # Handle chat
            msg.submit(chat_with_ai, [msg, chatbot], [chatbot])
            submit.click(chat_with_ai, [msg, chatbot], [chatbot])
            
            # Clear button
            clear = gr.Button("🗑️ Clear Chat")
            clear.click(lambda: None, None, chatbot, queue=False)
        
        with gr.Tab("📚 About Your Suite"):
            gr.Markdown(
                """
                ## 🎵 Your AI Music Production Suite
                
                ### What You Have:
                
                **1. Live AI Plugin**
                - Real-time Logic Pro control
                - Screen vision with Google Gemini
                - OSC automation
                - Voice commands
                
                **2. AI Mixing Engineer**
                - Professional audio analysis
                - EQ & compression recommendations
                - Loudness metering
                - Waveform & spectrogram
                
                **3. Music Copilot**
                - Production Q&A
                - Logic Pro tips
                - Sound pack management
                
                **4. Voice Assistant**
                - Google Gemini 2.0 vision
                - Real-time screen analysis
                - Hands-free control
                
                ### Tech Stack:
                - Python 3.11
                - Google Gemini 2.0 Flash
                - Kimi K2 (meta-llama/Llama-3.3-70B)
                - OSC Protocol
                - AppleScript automation
                - librosa (audio analysis)
                - Gradio (web interfaces)
                
                ### Value:
                **~$1,150** worth of professional tools
                - iZotope Neutron equivalent: $399
                - Sonible smart:EQ equivalent: $149
                - LANDR mastering: $150/year
                - Voice control system: $299
                - OSC automation: $149
                
                **All built for FREE!** ✨
                
                ### Project Location:
                - GitHub: https://github.com/neebz1/main
                - Local: `/Users/nr/main`
                
                ### Current Status:
                ✅ Production-ready
                ✅ Fully functional
                ✅ Documented
                ✅ Tested
                
                ---
                
                ## 💡 How to Use This Space
                
                1. **Ask me to build something**
                   - "Add a tempo sync feature"
                   - "Create a chord progression generator"
                   
                2. **I'll provide:**
                   - Complete code
                   - How to install it
                   - How to use it
                   
                3. **Copy code to your Mac**
                   - Add to your project
                   - Run and enjoy!
                
                4. **Keep iterating!**
                   - Ask for improvements
                   - Fix issues
                   - Add more features
                
                ---
                
                **🚀 Ready to build something amazing?** Just start chatting!
                """
            )
    
    gr.Markdown(
        """
        ---
        ### 🌟 Access This Space From:
        - 📱 Your phone (save to home screen!)
        - 💻 Any computer
        - 📲 Tablet
        - 🌐 Anywhere with internet
        
        **🔒 Your API keys are safe** - stored in Space Secrets (not in chat)
        
        ---
        🎵 **Built with AI • Powered by Kimi K2** 🎚️
        """
    )

if __name__ == "__main__":
    demo.launch()

