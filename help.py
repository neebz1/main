#!/usr/bin/env python3
"""
🆘 Help & Diagnostic Tool
Run this when you need help or want to check system status
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    """Print a nice header"""
    print("\n" + "━" * 60)
    print(f"  {text}")
    print("━" * 60 + "\n")

def check_python():
    """Check Python version"""
    print("🐍 Python Check:")
    version = sys.version
    print(f"   Version: {version}")
    
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Dependency Check:")
    
    deps = {
        "Core": ["gradio", "dotenv", "together"],
        "AI Clients": ["anthropic", "openai"],
        "Audio Processing": ["librosa", "soundfile", "matplotlib", "numpy", "PIL"],
        "Voice (Optional)": ["google.generativeai", "speech_recognition", "pyttsx3"]
    }
    
    all_ok = True
    for category, packages in deps.items():
        print(f"\n   {category}:")
        for package in packages:
            # Handle special cases
            module_name = package
            if package == "dotenv":
                module_name = "dotenv"
            elif package == "PIL":
                module_name = "PIL"
                
            try:
                __import__(module_name)
                print(f"      ✅ {package}")
            except ImportError:
                print(f"      ❌ {package} (install: pip3 install {package})")
                if category in ["Core", "AI Clients"]:
                    all_ok = False
    
    return all_ok

def check_env_file():
    """Check .env file and API keys"""
    print("\n🔑 API Key Check:")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("   ❌ .env file not found")
        print("   📝 Create it: cp config_example.txt .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Try to load and check keys
    from dotenv import dotenv_values
    config = dotenv_values(".env")
    
    keys = {
        "TOGETHER_API_KEY": "Kimi K2 (Together AI)",
        "OPENAI_API_KEY": "OpenAI (ChatGPT)",
        "ANTHROPIC_API_KEY": "Anthropic (Claude)",
        "GEMINI_API_KEY": "Google (Gemini)"
    }
    
    found_keys = False
    for key, name in keys.items():
        if key in config and config[key] and config[key].strip() and not config[key].startswith("your_"):
            print(f"   ✅ {name}: Configured")
            found_keys = True
        else:
            print(f"   ⚠️  {name}: Not configured")
    
    return found_keys

def check_scripts():
    """Check if scripts exist and are executable"""
    print("\n📜 Script Check:")
    
    scripts = [
        "start-music-ai.sh",
        "start-ai-mixing-engineer.sh",
        "start-live-ai-assistant.sh",
        "fix-everything.sh"
    ]
    
    all_ok = True
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            is_executable = os.access(script_path, os.X_OK)
            if is_executable:
                print(f"   ✅ {script}")
            else:
                print(f"   ⚠️  {script} (not executable - run: chmod +x {script})")
                all_ok = False
        else:
            print(f"   ❌ {script} not found")
            all_ok = False
    
    return all_ok

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Port Check:")
    
    ports = {
        7860: "Logic Pro Copilot",
        7861: "AI Mixing Engineer"
    }
    
    all_ok = True
    for port, app in ports.items():
        try:
            result = subprocess.run(
                ["lsof", "-i", f":{port}", "-sTCP:LISTEN"],
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(f"   ⚠️  Port {port} ({app}): In use")
                print(f"      Kill it: kill -9 $(lsof -t -i:{port})")
                all_ok = False
            else:
                print(f"   ✅ Port {port} ({app}): Available")
        except FileNotFoundError:
            print(f"   ⚠️  Cannot check port {port} (lsof not available)")
    
    return all_ok

def check_files():
    """Check if key files exist"""
    print("\n📁 File Check:")
    
    files = [
        ("logic_copilot_lite.py", "Logic Pro Copilot"),
        ("ai_mixing_engineer.py", "AI Mixing Engineer"),
        ("live_ai_assistant.py", "Live AI Assistant"),
        ("requirements.txt", "Dependencies list")
    ]
    
    all_ok = True
    for file, desc in files:
        if Path(file).exists():
            print(f"   ✅ {file} ({desc})")
        else:
            print(f"   ❌ {file} ({desc}) not found")
            if file.endswith(".py"):
                all_ok = False
    
    return all_ok

def get_quick_fixes():
    """Suggest quick fixes based on issues"""
    print("\n🔧 Quick Fixes:")
    print("\n   If dependencies are missing:")
    print("      pip3 install gradio together python-dotenv anthropic openai")
    
    print("\n   If .env file is missing:")
    print("      cp config_example.txt .env")
    print("      # Then edit .env and add your API keys")
    
    print("\n   If scripts aren't executable:")
    print("      chmod +x start-*.sh fix-everything.sh")
    
    print("\n   If ports are in use:")
    print("      kill -9 $(lsof -t -i:7860)")
    print("      kill -9 $(lsof -t -i:7861)")
    
    print("\n   For a complete fix:")
    print("      ./fix-everything.sh")

def print_summary(checks):
    """Print overall summary"""
    print_header("📊 SUMMARY")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("🎉 Everything looks good!\n")
        print("Ready to launch:")
        print("   ./start-music-ai.sh              # Logic Pro Copilot")
        print("   ./start-ai-mixing-engineer.sh    # AI Mixing Engineer")
        print("\nOr run directly:")
        print("   python3 logic_copilot_lite.py")
        print("   python3 ai_mixing_engineer.py")
    else:
        print("⚠️  Some issues detected!\n")
        failed = [name for name, passed in checks.items() if not passed]
        print(f"Failed checks: {', '.join(failed)}\n")
        print("🆘 Run this to fix everything:")
        print("   ./fix-everything.sh")
        print("\nOr see TROUBLESHOOTING.md for detailed help")
    
    print("\n" + "━" * 60)

def main():
    """Main diagnostic routine"""
    print_header("🆘 AI Music Suite - Help & Diagnostics")
    print("This tool will check your setup and help you fix any issues.\n")
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    checks = {}
    
    # Run all checks
    checks["Python"] = check_python()
    checks["Files"] = check_files()
    
    try:
        checks["Dependencies"] = check_dependencies()
    except Exception as e:
        print(f"\n   ❌ Error checking dependencies: {e}")
        checks["Dependencies"] = False
    
    try:
        checks["API Keys"] = check_env_file()
    except Exception as e:
        print(f"\n   ❌ Error checking .env: {e}")
        checks["API Keys"] = False
    
    checks["Scripts"] = check_scripts()
    checks["Ports"] = check_ports()
    
    # Show quick fixes
    get_quick_fixes()
    
    # Print summary
    print_summary(checks)
    
    print("\n💡 Need more help? Read TROUBLESHOOTING.md")
    print("   cat TROUBLESHOOTING.md | less")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Try running: ./fix-everything.sh")
