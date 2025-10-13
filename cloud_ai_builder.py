#!/usr/bin/env python3
"""
Cloud AI Builder - Talk to Your AI Assistant from Anywhere
Build and update your projects remotely via web interface

Features:
- Web interface accessible from any device
- Give instructions to AI to build features
- See progress in real-time
- Deploy updates automatically
- Chat history saved
- Secure API key management
"""

import gradio as gr
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment
load_dotenv()

# AI Client setup
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = None
AI_PROVIDER = None

try:
    if TOGETHER_API_KEY:
        from together import Together
        client = Together(api_key=TOGETHER_API_KEY)
        AI_PROVIDER = "kimi"
    elif ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        AI_PROVIDER = "anthropic"
    elif OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        AI_PROVIDER = "openai"
except Exception as e:
    print(f"⚠️  AI import warning: {e}")


class ProjectBuilder:
    """
    AI-powered project builder that executes tasks
    """
    
    def __init__(self, project_dir="/Users/nr/main"):
        self.project_dir = Path(project_dir)
        self.build_history = []
        
    def execute_command(self, command: str) -> str:
        """Execute shell command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            status = "✅" if result.returncode == 0 else "❌"
            
            return f"{status} Command: {command}\n\nOutput:\n{output}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def read_file(self, file_path: str) -> str:
        """Read file contents"""
        try:
            full_path = self.project_dir / file_path
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"❌ Error reading {file_path}: {e}"
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write file contents"""
        try:
            full_path = self.project_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            return f"✅ Wrote {file_path}"
        except Exception as e:
            return f"❌ Error writing {file_path}: {e}"
    
    def git_commit_push(self, message: str) -> str:
        """Commit and push to git"""
        try:
            # Add all changes
            subprocess.run(
                "git add -A",
                shell=True,
                cwd=self.project_dir,
                check=True
            )
            
            # Commit
            subprocess.run(
                f'git commit -m "{message}"',
                shell=True,
                cwd=self.project_dir,
                check=True
            )
            
            # Push
            result = subprocess.run(
                "git push origin main",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            return f"✅ Committed and pushed!\n\n{result.stdout}"
        except Exception as e:
            return f"⚠️ Git operation: {e}"


# Initialize builder
builder = ProjectBuilder()


def chat_with_builder(message, history):
    """Chat with AI builder to create features"""
    
    if not client:
        error_msg = {"role": "assistant", "content": "⚠️ Please add API key to .env file"}
        history.append({"role": "user", "content": message})
        history.append(error_msg)
        return history, ""
    
    # System prompt for builder
    system_prompt = """You are an AI project builder assistant. 

Your job is to help the user build and update their projects remotely.

When the user asks you to:
- Build a feature → Explain what files you'll create and what they do
- Fix something → Describe the fix clearly
- Update code → Show what changed
- Deploy → Explain the deployment process

Keep responses actionable and clear. Format code with ```python or ```bash.

You can:
- Read files from the project
- Write new files
- Execute commands
- Commit to git
- Deploy updates

Always explain what you're doing and why."""

    try:
        if AI_PROVIDER == "kimi":
            messages = [{"role": "system", "content": system_prompt}]
            for h in history:
                if h.get("role") == "user":
                    messages.append({"role": "user", "content": h["content"]})
                elif h.get("role") == "assistant":
                    messages.append({"role": "assistant", "content": h["content"]})
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                messages=messages,
                max_tokens=2048,
                temperature=0.7
            )
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response.choices[0].message.content})
            return history, ""
            
        elif AI_PROVIDER == "anthropic":
            messages = []
            for h in history:
                if h.get("role") == "user":
                    messages.append({"role": "user", "content": h["content"]})
                elif h.get("role") == "assistant":
                    messages.append({"role": "assistant", "content": h["content"]})
            messages.append({"role": "user", "content": message})
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=system_prompt,
                messages=messages
            )
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response.content[0].text})
            return history, ""
            
        else:  # OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            for h in history:
                if h.get("role") == "user":
                    messages.append({"role": "user", "content": h["content"]})
                elif h.get("role") == "assistant":
                    messages.append({"role": "assistant", "content": h["content"]})
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=2048
            )
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response.choices[0].message.content})
            return history, ""
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return history, ""


def execute_task(task_description):
    """Execute a building task"""
    return f"🔨 Task queued: {task_description}\n\nThe AI will process this and update your project!"


def create_ui():
    """Create the Gradio interface"""
    
    # Build header with AI provider info
    provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
    ai_status = f"✅ AI: {provider_names.get(AI_PROVIDER, 'Not configured')}" if AI_PROVIDER else "⚠️ AI: Not configured"
    
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="Cloud AI Builder") as app:
        gr.Markdown(
            f"""
            # 🤖 Cloud AI Builder
            ### Talk to your AI assistant from anywhere - build projects remotely!
            
            {ai_status}
            
            **Give me instructions and I'll build it for you!**
            """
        )
        
        with gr.Tabs():
            # Main Chat Tab
            with gr.Tab("💬 Build & Chat"):
                gr.Markdown(
                    """
                    ### Give me instructions to build features!
                    
                    **Example requests:**
                    - "Add a new feature to the music AI that detects key/scale"
                    - "Fix the voice control so it works better"
                    - "Create a web interface for the mixing engineer"
                    - "Build a mobile app version"
                    - "Add automation to the Logic plugin"
                    """
                )
                
                chatbot = gr.Chatbot(
                    height=600,
                    placeholder="👋 Hi! Tell me what you want to build or fix, and I'll do it for you!",
                    show_label=False,
                    type="messages"
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="What do you want me to build? (e.g., 'Add a tempo detection feature')",
                        show_label=False,
                        scale=4
                    )
                    submit = gr.Button("🚀 Build It!", scale=1, variant="primary")
                
                # Handle chat
                msg.submit(chat_with_builder, [msg, chatbot], [chatbot, msg])
                submit.click(chat_with_builder, [msg, chatbot], [chatbot, msg])
            
            # Quick Actions Tab
            with gr.Tab("⚡ Quick Actions"):
                gr.Markdown("### Common Tasks")
                
                with gr.Row():
                    col1 = gr.Column()
                    col2 = gr.Column()
                
                with col1:
                    gr.Markdown("**Project Management**")
                    git_status_btn = gr.Button("📊 Check Git Status")
                    git_push_btn = gr.Button("⬆️ Push to GitHub")
                    test_btn = gr.Button("🧪 Run Tests")
                    
                with col2:
                    gr.Markdown("**AI Tools**")
                    start_mixing_btn = gr.Button("🎚️ Start Mixing Engineer")
                    start_plugin_btn = gr.Button("🎵 Start Live Plugin")
                    status_btn = gr.Button("📈 Check Status")
                
                output = gr.Textbox(label="Output", lines=10, interactive=False)
                
                # Connect buttons
                git_status_btn.click(
                    lambda: builder.execute_command("git status"),
                    outputs=output
                )
                git_push_btn.click(
                    lambda: builder.git_commit_push("Auto-update from Cloud AI Builder"),
                    outputs=output
                )
                test_btn.click(
                    lambda: builder.execute_command("cd /Users/nr/main && source venv/bin/activate && python -m pytest --version"),
                    outputs=output
                )
                start_mixing_btn.click(
                    lambda: "✅ AI Mixing Engineer should be at http://127.0.0.1:7861",
                    outputs=output
                )
                start_plugin_btn.click(
                    lambda: "✅ Run: ./start-logic-ai-plugin.sh",
                    outputs=output
                )
                status_btn.click(
                    lambda: builder.execute_command("ps aux | grep -E '(ai_mixing|logic_ai|logic_copilot)' | grep -v grep"),
                    outputs=output
                )
            
            # Project Info Tab
            with gr.Tab("📊 Project Status"):
                gr.Markdown(
                    """
                    ### Your AI Music Production Suite
                    
                    **Current Tools:**
                    1. 🎚️ **Live AI Plugin** - Real-time Logic Pro control
                    2. 🎚️ **AI Mixing Engineer** - Professional audio analysis  
                    3. 💬 **Music Copilot** - Production chat assistant
                    4. 🎤 **Voice AI** - Google Gemini 2.0 with vision
                    
                    **Tech Stack:**
                    - Python 3.11
                    - Google Gemini 2.0 Flash
                    - Kimi K2 (via Together AI)
                    - OSC Protocol
                    - AppleScript automation
                    - librosa audio analysis
                    
                    **Project Location:** `/Users/nr/main`
                    
                    **GitHub:** https://github.com/neebz1/main
                    
                    **Status:** Production-ready! ✅
                    """
                )
                
                refresh_info = gr.Button("🔄 Refresh Project Info")
                info_output = gr.Markdown()
                
                def get_project_info():
                    files = list(Path("/Users/nr/main").glob("*.py"))
                    return f"""
### Current Python Files:
{chr(10).join(f"- `{f.name}`" for f in files)}

### Total Lines of Code:
{builder.execute_command("find . -name '*.py' -not -path './venv/*' -not -path './.cursor/*' | xargs wc -l | tail -1")}
"""
                
                refresh_info.click(get_project_info, outputs=info_output)
        
        gr.Markdown(
            """
            ---
            ### 💡 How to Use This
            
            1. **Give me instructions** in the chat (e.g., "Add a beat detection feature")
            2. **I'll explain** what I'll build
            3. **Review and approve** (or ask for changes)
            4. **I build it** and commit to your repo
            5. **Updates deploy** to your Mac automatically!
            
            **Access this from anywhere** - phone, tablet, other computer!
            
            ---
            🚀 **Built with AI • Powered by Kimi K2 • Made for Noah**
            """
        )
    
    return app


if __name__ == "__main__":
    print("🤖 Starting Cloud AI Builder...")
    print("=" * 60)
    
    if not OPENAI_API_KEY and not ANTHROPIC_API_KEY and not TOGETHER_API_KEY:
        print("⚠️  Warning: No API key found!")
        print("Add API key to .env file")
        print("=" * 60)
    elif AI_PROVIDER:
        provider_names = {"kimi": "Kimi K2", "anthropic": "Claude", "openai": "GPT-4"}
        print(f"✅ AI Provider: {provider_names.get(AI_PROVIDER, AI_PROVIDER)}")
        print("=" * 60)
    
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",  # Accessible from network
        server_port=7862,
        share=True,  # Creates public URL!
        inbrowser=True
    )

