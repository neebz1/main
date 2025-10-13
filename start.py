#!/usr/bin/env python3
"""
🚀 Quick Start - Your AI Music Suite
The easiest way to get started!
"""

import sys
import os
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("🎵 AI MUSIC PRODUCTION SUITE - YOUR ONLY HOPE! 🎵")
    print("=" * 70 + "\n")

def check_basics():
    """Quick check before launching"""
    issues = []
    
    # Check .env
    if not Path(".env").exists():
        issues.append("⚠️  No .env file found (API keys needed for AI features)")
    
    # Check basic imports
    try:
        import gradio
    except ImportError:
        issues.append("❌ Gradio not installed (run: pip3 install gradio)")
        return False, issues
    
    try:
        import together
    except ImportError:
        issues.append("⚠️  Together AI not installed (run: pip3 install together)")
    
    return len([i for i in issues if i.startswith("❌")]) == 0, issues

def show_menu():
    """Show launch menu"""
    print("\n📱 Choose what to launch:\n")
    print("  1. Logic Pro Copilot (Music AI Chat)")
    print("  2. AI Mixing Engineer (Audio Analysis)")
    print("  3. Live AI Assistant (Voice Control)")
    print("  4. Run Diagnostics (Check what's wrong)")
    print("  5. Emergency Fix (Fix everything)")
    print("  q. Quit\n")
    
    choice = input("Enter choice (1-5 or q): ").strip().lower()
    return choice

def launch_copilot():
    """Launch Logic Pro Copilot"""
    print("\n🎵 Launching Logic Pro Copilot...")
    print("━" * 60)
    print("This will open in your browser at http://localhost:7860")
    print("Press Ctrl+C to stop")
    print("━" * 60 + "\n")
    os.system("python3 logic_copilot_lite.py")

def launch_mixing():
    """Launch AI Mixing Engineer"""
    print("\n🎚️ Launching AI Mixing Engineer...")
    print("━" * 60)
    print("This will open in your browser at http://localhost:7861")
    print("Press Ctrl+C to stop")
    print("━" * 60 + "\n")
    os.system("python3 ai_mixing_engineer.py")

def launch_voice():
    """Launch Live AI Assistant"""
    print("\n🎤 Launching Live AI Assistant...")
    print("━" * 60)
    print("Voice-activated AI for Logic Pro")
    print("Press Ctrl+C to stop")
    print("━" * 60 + "\n")
    os.system("python3 live_ai_assistant.py")

def run_diagnostics():
    """Run diagnostic tool"""
    print("\n🔍 Running diagnostics...")
    print("━" * 60 + "\n")
    os.system("python3 help.py")
    input("\nPress Enter to continue...")

def run_fix():
    """Run emergency fix"""
    print("\n🆘 Running emergency fix...")
    print("━" * 60 + "\n")
    os.system("./fix-everything.sh")
    input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    print_banner()
    
    # Quick checks
    can_run, issues = check_basics()
    
    if issues:
        print("⚠️  Issues detected:\n")
        for issue in issues:
            print(f"   {issue}")
        print()
        
        if not can_run:
            print("❌ Cannot proceed. Please run: ./fix-everything.sh\n")
            return
        else:
            print("💡 You can still run, but some features may not work.")
            print("   Run option 5 (Emergency Fix) to fix these issues.\n")
    else:
        print("✅ All systems ready!\n")
    
    # Main loop
    while True:
        try:
            choice = show_menu()
            
            if choice == '1':
                launch_copilot()
            elif choice == '2':
                launch_mixing()
            elif choice == '3':
                launch_voice()
            elif choice == '4':
                run_diagnostics()
            elif choice == '5':
                run_fix()
            elif choice in ['q', 'quit', 'exit']:
                print("\n👋 Goodbye! Keep making music! 🎵\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1-5 or q.\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Keep making music! 🎵\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Try running: ./fix-everything.sh\n")

if __name__ == "__main__":
    main()
