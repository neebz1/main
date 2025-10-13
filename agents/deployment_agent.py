#!/usr/bin/env python3
"""
🤖 Autonomous Deployment Agent
Automatically deploys and manages all AI services using Bitwarden credentials
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Optional


class DeploymentAgent:
    def __init__(self):
        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
        self.services = {}
        self.api_keys = {}

    def load_bitwarden_credentials(self) -> bool:
        """Load API keys from Bitwarden"""
        print("🔐 Loading credentials from Bitwarden...")

        try:
            # Source .bitwarden-oauth
            oauth_file = self.base_dir / ".bitwarden-oauth"
            if not oauth_file.exists():
                print("❌ .bitwarden-oauth not found")
                return False

            # Run bwload function
            result = subprocess.run(
                ["zsh", "-c", "source ~/.zshrc && bwload && env"],
                capture_output=True,
                text=True,
            )

            # Parse environment variables
            for line in result.stdout.split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key in [
                        "OPENROUTER_API_KEY",
                        "GOOGLE_API_KEY",
                        "MOONSHOT_API_KEY",
                        "GITHUB_TOKEN",
                        "HF_TOKEN",
                        "OPENAI_API_KEY",
                        "ANTHROPIC_API_KEY",
                    ]:
                        self.api_keys[key] = value

            print(f"✅ Loaded {len(self.api_keys)} API keys")
            return True

        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            return False

    def deploy_service(
        self, name: str, script: str, port: Optional[int] = None
    ) -> bool:
        """Deploy a service"""
        print(f"\n🚀 Deploying {name}...")

        try:
            script_path = self.base_dir / script
            if not script_path.exists():
                print(f"❌ Script not found: {script}")
                return False

            # Make script executable
            os.chmod(script_path, 0o755)

            # Start service in background
            env = os.environ.copy()
            env.update(self.api_keys)

            process = subprocess.Popen(
                ["bash", str(script_path)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_dir),
            )

            self.services[name] = {
                "process": process,
                "port": port,
                "script": script,
                "status": "running",
            }

            print(f"✅ {name} started (PID: {process.pid})")
            if port:
                print(f"   URL: http://localhost:{port}")

            return True

        except Exception as e:
            print(f"❌ Error deploying {name}: {e}")
            return False

    def check_service_health(self, name: str) -> bool:
        """Check if service is running"""
        if name not in self.services:
            return False

        process = self.services[name]["process"]
        return process.poll() is None

    def deploy_all_local_services(self):
        """Deploy all local AI services"""
        print("\n" + "=" * 60)
        print("🤖 AUTONOMOUS DEPLOYMENT AGENT")
        print("Deploying all AI services...")
        print("=" * 60)

        # Load credentials
        if not self.load_bitwarden_credentials():
            print("❌ Failed to load credentials")
            return

        # Deploy services
        services_to_deploy = [
            ("AI Mixing Engineer", "start-ai-mixing-engineer.sh", 7861),
            ("Music Copilot", "start-music-ai.sh", 7860),
            ("Live AI Assistant", "start-live-ai-assistant.sh", None),
            ("Logic AI Plugin", "start-logic-ai-plugin.sh", None),
        ]

        for name, script, port in services_to_deploy:
            self.deploy_service(name, script, port)
            time.sleep(2)  # Give services time to start

        print("\n" + "=" * 60)
        print("✅ Deployment complete!")
        print("=" * 60)

        # Show status
        self.show_status()

    def deploy_cloud_service(self, service: str):
        """Deploy service to cloud (Railway/Render)"""
        print(f"\n☁️ Deploying {service} to cloud...")

        if service == "CursorDocsIndex":
            docs_dir = self.base_dir / "CursorDocsIndex"
            if not docs_dir.exists():
                print("❌ CursorDocsIndex not found")
                return False

            # Deploy to Railway
            print("🚂 Deploying to Railway...")
            subprocess.run(
                ["bash", "-c", "cd " + str(docs_dir) + " && railway up"],
                env={**os.environ, **self.api_keys},
            )

    def show_status(self):
        """Show status of all services"""
        print("\n📊 Service Status:")
        print("-" * 60)

        for name, info in self.services.items():
            status = "🟢 Running" if self.check_service_health(name) else "🔴 Stopped"
            print(f"{status} {name}")
            if info["port"]:
                print(f"         → http://localhost:{info['port']}")

        print("-" * 60)

    def monitor_services(self):
        """Monitor and restart services if they crash"""
        print("\n👁️ Monitoring services...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                time.sleep(10)

                for name, info in self.services.items():
                    if not self.check_service_health(name):
                        print(f"⚠️ {name} stopped! Restarting...")
                        self.deploy_service(name, info["script"], info["port"])

        except KeyboardInterrupt:
            print("\n\n🛑 Stopping monitoring...")
            self.stop_all_services()

    def stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")

        for name, info in self.services.items():
            process = info["process"]
            if process.poll() is None:
                process.terminate()
                print(f"✅ Stopped {name}")

        print("✅ All services stopped")

    def run(self):
        """Main agent loop"""
        try:
            # Deploy all services
            self.deploy_all_local_services()

            # Monitor and keep alive
            self.monitor_services()

        except Exception as e:
            print(f"❌ Agent error: {e}")
            self.stop_all_services()


if __name__ == "__main__":
    agent = DeploymentAgent()
    agent.run()
