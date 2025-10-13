#!/usr/bin/env python3
"""
💬 Conversational Agent Interface
Just talk to your agents - no coding required!
"""

import os
import subprocess
from pathlib import Path


class ConversationalAgent:
    def __init__(self):
        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
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

    def execute_command(self, command: str) -> str:
        """Execute a natural language command"""
        command_lower = command.lower()

        # Deploy commands
        if any(
            word in command_lower
            for word in ["deploy", "start", "launch", "spin up", "spawn"]
        ):
            if "everything" in command_lower or "all" in command_lower:
                return self.deploy_everything()
            elif "cloud" in command_lower:
                return self.deploy_cloud()
            elif "local" in command_lower or "services" in command_lower:
                return self.deploy_local()

        # Status commands
        elif any(
            word in command_lower for word in ["status", "check", "health", "running"]
        ):
            return self.check_status()

        # Stop commands
        elif any(word in command_lower for word in ["stop", "shutdown", "kill"]):
            return self.stop_services()

        # Monitor commands
        elif any(word in command_lower for word in ["monitor", "watch"]):
            return self.start_monitoring()

        else:
            return "I can help you with:\n- Deploy everything\n- Check status\n- Stop services\n- Monitor services\n\nJust tell me what you want!"

    def deploy_everything(self) -> str:
        """Deploy all services"""
        print("🚀 Deploying everything automatically...")

        subprocess.Popen(
            ["python3", "agents/deployment_agent.py"],
            cwd=str(self.base_dir),
            env={**os.environ, **self.env},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return "✅ All services are deploying in the background!\n\nServices starting:\n- AI Mixing Engineer (http://localhost:7861)\n- Music Copilot (http://localhost:7860)\n- Live AI Assistant\n- Logic AI Plugin\n\nMonitoring automatically enabled."

    def deploy_cloud(self) -> str:
        """Deploy cloud services"""
        print("☁️ Deploying to cloud...")

        subprocess.Popen(
            ["python3", "agents/cloud_agent.py"],
            cwd=str(self.base_dir),
            env={**os.environ, **self.env},
        )

        return "✅ Cloud deployment started!\n\nDeploying CursorDocsIndex to Railway..."

    def deploy_local(self) -> str:
        """Deploy local services only"""
        return self.deploy_everything()

    def check_status(self) -> str:
        """Check service status"""
        import requests

        status = []

        # Check AI Mixing Engineer
        try:
            requests.get("http://localhost:7861", timeout=2)
            status.append("🟢 AI Mixing Engineer: Running")
        except:
            status.append("🔴 AI Mixing Engineer: Stopped")

        # Check Music Copilot
        try:
            requests.get("http://localhost:7860", timeout=2)
            status.append("🟢 Music Copilot: Running")
        except:
            status.append("🔴 Music Copilot: Stopped")

        return "\n".join(status) if status else "All services stopped"

    def stop_services(self) -> str:
        """Stop all services"""
        subprocess.run(["pkill", "-f", "deployment_agent.py"])
        subprocess.run(["pkill", "-f", "monitoring_agent.py"])

        return "✅ All services stopped"

    def start_monitoring(self) -> str:
        """Start monitoring agent"""
        subprocess.Popen(
            ["python3", "agents/monitoring_agent.py"],
            cwd=str(self.base_dir),
            env={**os.environ, **self.env},
        )

        return "👁️ Monitoring started! Auto-healing enabled."

    def chat(self):
        """Interactive chat interface"""
        print("\n" + "=" * 60)
        print("💬 CONVERSATIONAL AGENT")
        print("Just tell me what you want - no coding required!")
        print("=" * 60)
        print("\nExamples:")
        print("  - Deploy everything")
        print("  - Check status")
        print("  - Start monitoring")
        print("  - Stop all services")
        print("\nType 'quit' to exit\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("\n👋 Goodbye!")
                    break

                if not user_input:
                    continue

                response = self.execute_command(user_input)
                print(f"\n🤖 Agent: {response}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    agent = ConversationalAgent()
    agent.chat()
