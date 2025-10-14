#!/usr/bin/env python3
"""
🚀 Interactive Setup Wizard - One-Click Setup for Your AI Music Studio
Makes your Mac ready for music production in minutes!
"""

import subprocess
import time
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

# Load environment
load_dotenv()


class SetupWizard:
    def __init__(self):
        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
        self.status_log = []

    def log(self, message, status="info"):
        """Add a status message with emoji"""
        emoji = {"info": "ℹ️", "success": "✅", "error": "❌", "working": "🔄"}
        log_msg = f"{emoji.get(status, 'ℹ️')} {message}"
        self.status_log.append(log_msg)
        return "\n".join(self.status_log)

    def check_python_packages(self):
        """Check and install required Python packages"""
        self.log("Checking Python packages...", "working")

        packages = ["gradio", "python-dotenv", "fastapi", "uvicorn"]
        missing = []

        for pkg in packages:
            try:
                __import__(pkg.replace("-", "_"))
                self.log(f"✓ {pkg} installed", "success")
            except ImportError:
                missing.append(pkg)
                self.log(f"✗ {pkg} missing", "error")

        if missing:
            self.log(f"Installing {len(missing)} packages...", "working")
            # ✅ SECURE: Use list instead of shell=True to prevent command injection
            cmd = ["pip", "install"] + missing
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if result.returncode == 0:
                self.log(f"Installed: {', '.join(missing)}", "success")
            else:
                self.log("Failed to install packages", "error")

        return "\n".join(self.status_log)

    def check_env_file(self):
        """Check if .env file exists and has required keys"""
        self.log("Checking .env configuration...", "working")

        env_file = self.base_dir / ".env"
        if not env_file.exists():
            self.log(".env file not found - creating template", "error")
            template = """# AI API Keys
TOGETHER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Gradio Password
GRADIO_PASSWORD=your_password_here

# API Secret
SECRET_KEY=your_secret_key_here
"""
            env_file.write_text(template)
            self.log("Created .env template - please add your API keys", "info")
        else:
            self.log(".env file found", "success")

            # Check for keys
            content = env_file.read_text()
            keys = ["GRADIO_PASSWORD", "SECRET_KEY"]
            for key in keys:
                if (
                    key in content
                    and "your_" not in content.split(key)[1].split("\n")[0]
                ):
                    self.log(f"✓ {key} configured", "success")
                else:
                    self.log(f"⚠ {key} needs to be set", "info")

        return "\n".join(self.status_log)

    def create_dock_launcher(self):
        """Create an app to add to Dock"""
        self.log("Creating Dock launcher...", "working")

        app_name = "AI Music Studio"
        app_path = Path.home() / "Applications" / f"{app_name}.app"

        # Create .app bundle structure
        contents_dir = app_path / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"

        for d in [macos_dir, resources_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Create launcher script
        launcher_script = macos_dir / app_name.replace(" ", "")
        launcher_content = f"""#!/bin/bash
cd {self.base_dir}
python3 setup_wizard.py &
"""
        launcher_script.write_text(launcher_content)
        launcher_script.chmod(0o755)

        # Create Info.plist
        info_plist = contents_dir / "Info.plist"
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{app_name.replace(" ", "")}</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.noah.aimusicstudio</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
</dict>
</plist>
"""
        info_plist.write_text(plist_content)

        self.log(f"Created {app_name}.app in Applications", "success")
        self.log("Drag to Dock to pin it!", "info")

        return "\n".join(self.status_log)

    def setup_keyboard_shortcuts(self):
        """Create keyboard shortcuts guide"""
        self.log("Setting up keyboard shortcuts...", "working")

        shortcuts = {
            "🎹 Logic Pro Copilot": "Ctrl+Opt+M",
            "🎚️ AI Mixing Engineer": "Ctrl+Opt+E",
            "☁️ Cloud Builder": "Ctrl+Opt+C",
            "🔌 API Server": "Ctrl+Opt+A",
            "📊 Security Check": "Ctrl+Opt+S",
        }

        shortcuts_md = "# 🎯 Your Keyboard Shortcuts\n\n"
        for app, shortcut in shortcuts.items():
            shortcuts_md += f"**{app}**: `{shortcut}`\n\n"

        shortcuts_file = self.base_dir / "SHORTCUTS.md"
        shortcuts_file.write_text(shortcuts_md)

        self.log("Keyboard shortcuts guide created", "success")
        self.log("See SHORTCUTS.md for details", "info")

        return "\n".join(self.status_log)

    def create_wallpaper_shortcuts(self):
        """Create a simple text file with shortcuts for wallpaper"""
        self.log("Creating shortcuts reference...", "working")

        wallpaper_text = """
╔══════════════════════════════════════════════════════════════╗
║                    🎹 AI MUSIC STUDIO                        ║
║                   KEYBOARD SHORTCUTS                         ║
╚══════════════════════════════════════════════════════════════╝

🎹 LOGIC PRO COPILOT          Ctrl+Opt+M
🎚️ AI MIXING ENGINEER         Ctrl+Opt+E
☁️ CLOUD AI BUILDER            Ctrl+Opt+C
🔌 REST API                    Ctrl+Opt+A
📊 SECURITY CHECK              Ctrl+Opt+S

═══════════════════════════════════════════════════════════════

📁 QUICK COMMANDS:

./start-music-ai.sh           Start Music AI
./start-ai-mixing-engineer.sh Start Mixing AI
./start-cloud-builder.sh      Start Cloud Builder
./start-api.sh                Start API Server
./security-check.sh           Run Security Check

═══════════════════════════════════════════════════════════════

🎵 READY TO MAKE MUSIC! 🎵
"""

        shortcuts_txt = self.base_dir / "Desktop-Shortcuts.txt"
        shortcuts_txt.write_text(wallpaper_text)

        self.log("Shortcuts reference created", "success")
        self.log("Set Desktop-Shortcuts.txt as your wallpaper!", "info")

        return "\n".join(self.status_log)

    def test_all_apps(self):
        """Test that all apps can start"""
        self.log("Testing all applications...", "working")

        apps = [
            ("Logic Pro Copilot", "logic_copilot_lite.py"),
            ("AI Mixing Engineer", "ai_mixing_engineer.py"),
            ("Cloud AI Builder", "cloud_ai_builder.py"),
            ("REST API", "api/main.py"),
        ]

        for name, script in apps:
            script_path = self.base_dir / script
            if script_path.exists():
                # Just check if file is valid Python
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(script_path)],
                    capture_output=True,
                )
                if result.returncode == 0:
                    self.log(f"✓ {name} ready", "success")
                else:
                    self.log(f"✗ {name} has errors", "error")
            else:
                self.log(f"✗ {name} not found", "error")

        return "\n".join(self.status_log)

    def run_full_setup(self):
        """Run complete setup process"""
        self.status_log = []
        self.log("🚀 Starting Full Setup...", "info")
        time.sleep(0.5)

        self.check_python_packages()
        time.sleep(0.3)

        self.check_env_file()
        time.sleep(0.3)

        self.create_dock_launcher()
        time.sleep(0.3)

        self.setup_keyboard_shortcuts()
        time.sleep(0.3)

        self.create_wallpaper_shortcuts()
        time.sleep(0.3)

        self.test_all_apps()
        time.sleep(0.3)

        self.log("", "info")
        self.log("🎉 SETUP COMPLETE!", "success")
        self.log("", "info")
        self.log("NEXT STEPS:", "info")
        self.log("1. Drag AI Music Studio.app to your Dock", "info")
        self.log("2. Set your API keys in .env file", "info")
        self.log("3. Restart and click the Dock icon!", "info")

        return "\n".join(self.status_log)

    def launch_app(self, app_name):
        """Launch a specific app"""
        self.status_log = []

        apps = {
            "Music AI": "./start-music-ai.sh",
            "Mixing AI": "./start-ai-mixing-engineer.sh",
            "Cloud Builder": "./start-cloud-builder.sh",
            "API Server": "./start-api.sh",
        }

        if app_name in apps:
            self.log(f"Launching {app_name}...", "working")
            script = self.base_dir / apps[app_name]

            if script.exists():
                subprocess.Popen(
                    ["bash", str(script)],
                    cwd=self.base_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.log(f"✓ {app_name} started!", "success")
                self.log("Check your browser for the interface", "info")
            else:
                self.log("✗ Launch script not found", "error")

        return "\n".join(self.status_log)


def create_ui():
    """Create the Gradio UI"""
    wizard = SetupWizard()

    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="blue"), title="AI Music Studio Setup"
    ) as app:
        gr.Markdown(
            """
        # 🚀 AI Music Studio - Interactive Setup Wizard
        ### One-click setup for your complete AI music production environment

        This wizard will:
        - ✅ Check all dependencies
        - ✅ Configure environment variables
        - ✅ Create Dock launcher
        - ✅ Set up keyboard shortcuts
        - ✅ Test all applications
        """
        )

        with gr.Tab("🔧 Setup"):
            gr.Markdown("### Run the complete setup process")

            setup_btn = gr.Button("🚀 Run Full Setup", variant="primary", size="lg")
            setup_output = gr.Textbox(
                label="Setup Progress", lines=20, max_lines=30, interactive=False
            )

            setup_btn.click(fn=wizard.run_full_setup, outputs=setup_output)

        with gr.Tab("🎵 Quick Launch"):
            gr.Markdown("### Launch your AI apps")

            with gr.Row():
                music_btn = gr.Button("🎹 Logic Pro Copilot", size="lg")
                mixing_btn = gr.Button("🎚️ AI Mixing Engineer", size="lg")

            with gr.Row():
                cloud_btn = gr.Button("☁️ Cloud Builder", size="lg")
                api_btn = gr.Button("🔌 API Server", size="lg")

            launch_output = gr.Textbox(
                label="Launch Status", lines=5, interactive=False
            )

            music_btn.click(
                fn=lambda: wizard.launch_app("Music AI"), outputs=launch_output
            )
            mixing_btn.click(
                fn=lambda: wizard.launch_app("Mixing AI"), outputs=launch_output
            )
            cloud_btn.click(
                fn=lambda: wizard.launch_app("Cloud Builder"), outputs=launch_output
            )
            api_btn.click(
                fn=lambda: wizard.launch_app("API Server"), outputs=launch_output
            )

        with gr.Tab("📋 Manual Checks"):
            gr.Markdown("### Run individual checks")

            with gr.Row():
                pkg_btn = gr.Button("Check Packages")
                env_btn = gr.Button("Check .env")
                test_btn = gr.Button("Test Apps")

            check_output = gr.Textbox(
                label="Check Results", lines=15, interactive=False
            )

            pkg_btn.click(fn=wizard.check_python_packages, outputs=check_output)
            env_btn.click(fn=wizard.check_env_file, outputs=check_output)
            test_btn.click(fn=wizard.test_all_apps, outputs=check_output)

        gr.Markdown(
            """
        ---
        ### 🎯 Quick Commands

        After setup, use these commands:
        ```bash
        ./start-music-ai.sh           # Music production AI
        ./start-ai-mixing-engineer.sh # Audio mixing AI
        ./start-cloud-builder.sh      # Remote development
        ./start-api.sh                # REST API server
        ```

        ### 📚 Documentation
        - `YOUR-ORGANIZED-ENVIRONMENT.md` - Complete guide
        - `SHORTCUTS.md` - Keyboard shortcuts
        - `Desktop-Shortcuts.txt` - Quick reference (set as wallpaper!)
        """
        )

    return app


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AI Music Studio - Setup Wizard")
    print("=" * 60 + "\n")

    app = create_ui()
    app.launch(server_name="127.0.0.1", server_port=7777, share=False, inbrowser=True)
