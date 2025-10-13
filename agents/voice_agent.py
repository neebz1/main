#!/usr/bin/env python3
"""
🎤 Voice-Activated Agent
Talk to your agents with voice commands!
"""

import os
import subprocess
import sys
from pathlib import Path

import pyttsx3
import speech_recognition as sr


class VoiceAgent:
    def __init__(self):
        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

        # Load credentials silently
        self.load_credentials()

    def load_credentials(self):
        """Silently load Bitwarden credentials"""
        result = subprocess.run(
            ["zsh", "-c", "source ~/.zshrc && bwload && env"],
            capture_output=True,
            text=True,
        )

        self.env = {}
        for line in result.stdout.split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                self.env[key] = value

    def speak(self, text: str):
        """Text to speech"""
        print(f"\n🤖 Agent: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        """Listen for voice command"""
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speak("Sorry, speech recognition service is unavailable")
            return ""

    def execute_command(self, command: str):
        """Execute voice command"""

        # Deploy commands
        if "deploy" in command or "start" in command or "launch" in command:
            if "everything" in command or "all" in command:
                self.speak("Deploying all services now")
                subprocess.Popen(
                    ["python3", "agents/deployment_agent.py"],
                    cwd=str(self.base_dir),
                    env={**os.environ, **self.env},
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.speak("All services are deploying in the background")

            elif "cloud" in command:
                self.speak("Deploying to cloud")
                subprocess.Popen(
                    ["python3", "agents/cloud_agent.py"],
                    cwd=str(self.base_dir),
                    env={**os.environ, **self.env},
                )

        # Status commands
        elif "status" in command or "check" in command:
            import requests

            status_msg = "Checking services. "

            try:
                requests.get("http://localhost:7861", timeout=2)
                status_msg += "Mixing Engineer is running. "
            except:
                status_msg += "Mixing Engineer is stopped. "

            try:
                requests.get("http://localhost:7860", timeout=2)
                status_msg += "Music Copilot is running."
            except:
                status_msg += "Music Copilot is stopped."

            self.speak(status_msg)

        # Stop commands
        elif "stop" in command or "shutdown" in command:
            self.speak("Stopping all services")
            subprocess.run(["pkill", "-f", "deployment_agent.py"])
            subprocess.run(["pkill", "-f", "monitoring_agent.py"])
            self.speak("All services stopped")

        # Monitor commands
        elif "monitor" in command or "watch" in command:
            self.speak("Starting monitoring with auto healing")
            subprocess.Popen(
                ["python3", "agents/monitoring_agent.py"],
                cwd=str(self.base_dir),
                env={**os.environ, **self.env},
            )

        else:
            self.speak(
                "I can deploy everything, check status, stop services, or start monitoring. What would you like?"
            )

    def run(self):
        """Main voice agent loop"""
        print("\n" + "=" * 60)
        print("🎤 VOICE-ACTIVATED AGENT")
        print("Just speak your commands!")
        print("=" * 60)
        print("\nSay things like:")
        print("  - Deploy everything")
        print("  - Check status")
        print("  - Start monitoring")
        print("  - Stop all services")
        print("\nPress Ctrl+C to exit\n")

        self.speak("Voice agent activated. How can I help you?")

        try:
            while True:
                command = self.listen()

                if command:
                    if "quit" in command or "exit" in command or "goodbye" in command:
                        self.speak("Goodbye!")
                        break

                    self.execute_command(command)

        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            self.speak("Goodbye!")


if __name__ == "__main__":
    # Install dependencies if needed
    try:
        import pyttsx3
        import speech_recognition
    except ImportError:
        print("📦 Installing voice dependencies...")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "SpeechRecognition",
                "pyttsx3",
                "pyobjc",
            ]
        )
        print("✅ Dependencies installed! Please run again.")
        sys.exit(0)

    agent = VoiceAgent()
    agent.run()
