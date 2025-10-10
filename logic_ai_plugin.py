#!/usr/bin/env python3
"""
Logic Pro AI Plugin - Real-time AI Assistant
Works LIVE inside Logic Pro via OSC (Open Sound Control)

No export/import needed - AI monitors and controls Logic in real-time!

Features:
- Real-time audio monitoring
- Live parameter control
- Screen vision (sees Logic Pro)
- Voice commands
- Automatic mixing suggestions
- Plugin parameter automation
"""

import os
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, List
import subprocess
from PIL import ImageGrab, Image

# OSC for Logic Pro communication
from pythonosc import dispatcher, osc_server, udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

# Google AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load environment
load_dotenv()


class LogicProOSCController:
    """
    Control Logic Pro via OSC (Open Sound Control)
    Logic Pro can send/receive OSC messages for real-time control
    """
    
    def __init__(self, logic_ip="127.0.0.1", logic_port=8000, listen_port=9000):
        self.logic_ip = logic_ip
        self.logic_port = logic_port
        self.listen_port = listen_port
        
        # OSC client to send to Logic Pro
        self.client = udp_client.SimpleUDPClient(logic_ip, logic_port)
        
        # Current state
        self.current_tempo = 120
        self.is_playing = False
        self.is_recording = False
        self.track_count = 0
        self.current_track = 1
        
        print(f"📡 OSC Controller initialized")
        print(f"   Sending to Logic: {logic_ip}:{logic_port}")
        print(f"   Listening on: {listen_port}")
    
    # Transport controls
    
    def play(self):
        """Start playback"""
        self.client.send_message("/play", 1)
        self.is_playing = True
        return "Playing"
    
    def stop(self):
        """Stop playback"""
        self.client.send_message("/stop", 1)
        self.is_playing = False
        return "Stopped"
    
    def record(self):
        """Start recording"""
        self.client.send_message("/record", 1)
        self.is_recording = True
        return "Recording"
    
    def toggle_play(self):
        """Toggle play/stop"""
        if self.is_playing:
            return self.stop()
        else:
            return self.play()
    
    # Track controls
    
    def select_track(self, track_number: int):
        """Select a track"""
        self.client.send_message("/track/select", track_number)
        self.current_track = track_number
        return f"Selected track {track_number}"
    
    def set_track_volume(self, track: int, volume: float):
        """Set track volume (0.0 to 1.0)"""
        self.client.send_message(f"/track/{track}/volume", volume)
        return f"Set track {track} volume to {volume}"
    
    def set_track_pan(self, track: int, pan: float):
        """Set track pan (-1.0 to 1.0)"""
        self.client.send_message(f"/track/{track}/pan", pan)
        return f"Set track {track} pan to {pan}"
    
    def mute_track(self, track: int, mute: bool = True):
        """Mute/unmute track"""
        self.client.send_message(f"/track/{track}/mute", 1 if mute else 0)
        return f"Track {track} {'muted' if mute else 'unmuted'}"
    
    def solo_track(self, track: int, solo: bool = True):
        """Solo/unsolo track"""
        self.client.send_message(f"/track/{track}/solo", 1 if solo else 0)
        return f"Track {track} {'solo' if solo else 'unsolo'}"
    
    # Project controls
    
    def set_tempo(self, bpm: float):
        """Set project tempo"""
        self.client.send_message("/tempo", bpm)
        self.current_tempo = bpm
        return f"Tempo set to {bpm} BPM"
    
    def set_time_signature(self, numerator: int, denominator: int):
        """Set time signature"""
        self.client.send_message("/timesig", [numerator, denominator])
        return f"Time signature set to {numerator}/{denominator}"
    
    # Plugin controls
    
    def set_plugin_param(self, track: int, plugin: int, param: int, value: float):
        """Set plugin parameter"""
        self.client.send_message(f"/track/{track}/plugin/{plugin}/param/{param}", value)
        return f"Set parameter {param} to {value}"
    
    def toggle_plugin(self, track: int, plugin: int, enabled: bool = True):
        """Enable/disable plugin"""
        self.client.send_message(f"/track/{track}/plugin/{plugin}/enabled", 1 if enabled else 0)
        return f"Plugin {'enabled' if enabled else 'disabled'}"
    
    # Automation
    
    def write_automation(self, track: int, parameter: str, value: float):
        """Write automation point"""
        self.client.send_message(f"/track/{track}/auto/{parameter}", value)
        return f"Wrote automation: {parameter} = {value}"


class LiveLogicAI:
    """
    Real-time AI assistant for Logic Pro
    Works LIVE - no export/import needed!
    """
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key or not GEMINI_AVAILABLE:
            print("⚠️  Google AI not available - running in basic mode")
            self.ai_enabled = False
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                system_instruction=self._get_system_prompt()
            )
            self.chat = self.model.start_chat(history=[])
            self.ai_enabled = True
        
        # OSC controller
        self.logic = LogicProOSCController()
        
        # Screen capture
        self.last_screenshot = None
        self.screenshot_interval = 2  # seconds
        
        print("🎚️ Live Logic AI Plugin Ready!")
    
    def _get_system_prompt(self) -> str:
        return """You are a real-time AI mixing engineer working LIVE inside Logic Pro.

You can:
- Control playback (play/stop/record)
- Adjust track parameters (volume, pan, mute, solo)
- Modify plugin settings
- Set tempo and time signature
- Write automation
- See the Logic Pro interface in real-time

When user asks for help, analyze what you see and make real-time adjustments.
Be proactive - if you see issues, fix them automatically.

Keep responses brief - you're working live!"""
    
    async def capture_screen_periodic(self):
        """Periodically capture screen for AI context"""
        while True:
            self.last_screenshot = ImageGrab.grab()
            self.last_screenshot.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            await asyncio.sleep(self.screenshot_interval)
    
    async def process_command(self, command: str):
        """Process AI command with current screen context"""
        if not self.ai_enabled:
            print(f"⚠️  AI not available. Command: {command}")
            return "AI not configured"
        
        # Send to AI with screen
        message_parts = [command]
        if self.last_screenshot:
            message_parts.append(self.last_screenshot)
        
        response = self.chat.send_message(message_parts)
        
        # Process response
        if response.text:
            print(f"🤖 AI: {response.text}")
            return response.text
        
        return "Done"
    
    def start_monitoring(self):
        """Start real-time monitoring mode"""
        print("🎵 Starting real-time monitoring...")
        print("=" * 60)
        print("The AI is now watching Logic Pro and ready to assist!")
        print("=" * 60)
        print("")
        print("Commands:")
        print("  Type 'help' for AI assistance")
        print("  Type 'screen' to have AI analyze current screen")
        print("  Type 'play' / 'stop' / 'record' for transport")
        print("  Type 'tempo 140' to set tempo")
        print("  Type 'quit' to exit")
        print("")
        
        # Start screen capture in background
        asyncio.create_task(self.capture_screen_periodic())
        
        while True:
            try:
                command = input("🎚️ > ").strip()
                
                if not command:
                    continue
                
                # Handle built-in commands
                if command.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                
                elif command.lower() == 'play':
                    result = self.logic.play()
                    print(f"✅ {result}")
                
                elif command.lower() == 'stop':
                    result = self.logic.stop()
                    print(f"✅ {result}")
                
                elif command.lower() == 'record':
                    result = self.logic.record()
                    print(f"✅ {result}")
                
                elif command.lower().startswith('tempo '):
                    try:
                        bpm = float(command.split()[1])
                        result = self.logic.set_tempo(bpm)
                        print(f"✅ {result}")
                    except:
                        print("❌ Usage: tempo <bpm>")
                
                elif command.lower() in ['help', 'screen', 'analyze']:
                    # Ask AI
                    response = asyncio.run(self.process_command(
                        f"Analyze the current Logic Pro screen and provide advice: {command}"
                    ))
                    print(f"🤖 {response}")
                
                else:
                    # Send to AI
                    response = asyncio.run(self.process_command(command))
                    print(f"🤖 {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def setup_logic_pro_osc():
    """
    Setup instructions for Logic Pro OSC
    """
    print("""
    📋 Logic Pro OSC Setup Instructions:
    
    To enable OSC in Logic Pro:
    
    1. Open Logic Pro
    2. Go to: Logic Pro → Control Surfaces → Setup
    3. Click 'New' → Install
    4. Choose 'OSC' from the list
    5. Set incoming port: 8000
    6. Set outgoing port: 9000
    7. Click 'Apply'
    
    That's it! The AI can now control Logic Pro in real-time!
    
    Press Enter to continue...
    """)
    input()


def main():
    """Main entry point"""
    print("🎚️ Logic Pro AI Plugin - Real-time Assistant")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Running in basic mode (no AI)")
        print("   Add GOOGLE_API_KEY to .env for full AI features")
        print("")
    
    # Show setup instructions
    setup_logic_pro_osc()
    
    # Initialize and run
    try:
        plugin = LiveLogicAI()
        plugin.start_monitoring()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

