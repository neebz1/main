#!/usr/bin/env python3
"""
☁️ Autonomous Cloud Deployment Agent
Automatically deploys services to Railway, Render, and other cloud platforms
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class CloudAgent:
    def __init__(self):
        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
        self.deployments = {}

    def load_credentials(self):
        """Load Bitwarden credentials"""
        print("🔐 Loading Bitwarden credentials...")

        result = subprocess.run(
            ["zsh", "-c", "source ~/.zshrc && bwload && env"],
            capture_output=True,
            text=True,
        )

        env_vars = {}
        for line in result.stdout.split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                env_vars[key] = value

        return env_vars

    def setup_railway_cli(self):
        """Install and configure Railway CLI"""
        print("🚂 Setting up Railway CLI...")

        # Check if installed
        result = subprocess.run(["which", "railway"], capture_output=True)
        if result.returncode != 0:
            print("📦 Installing Railway CLI...")
            subprocess.run(["npm", "install", "-g", "@railway/cli"])

        print("✅ Railway CLI ready")

    def deploy_to_railway(self, project_dir: str, project_name: str):
        """Deploy project to Railway"""
        print(f"\n🚂 Deploying {project_name} to Railway...")

        project_path = self.base_dir / project_dir
        if not project_path.exists():
            print(f"❌ Project not found: {project_dir}")
            return False

        try:
            # Initialize Railway project
            subprocess.run(
                ["railway", "init", "-n", project_name], cwd=str(project_path)
            )

            # Deploy
            subprocess.run(["railway", "up"], cwd=str(project_path))

            # Get URL
            result = subprocess.run(
                ["railway", "domain"],
                cwd=str(project_path),
                capture_output=True,
                text=True,
            )

            print(f"✅ Deployed to: {result.stdout.strip()}")

            self.deployments[project_name] = {
                "platform": "railway",
                "url": result.stdout.strip(),
                "status": "deployed",
            }

            return True

        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False

    def deploy_all_cloud_services(self):
        """Deploy all cloud services"""
        print("\n" + "=" * 60)
        print("☁️ AUTONOMOUS CLOUD DEPLOYMENT AGENT")
        print("=" * 60)

        # Load credentials
        env_vars = self.load_credentials()

        # Setup Railway
        self.setup_railway_cli()

        # Deploy CursorDocsIndex API
        print("\n📚 Deploying CursorDocsIndex API...")
        self.deploy_to_railway("CursorDocsIndex", "cursor-docs-api")

        print("\n" + "=" * 60)
        print("✅ Cloud deployment complete!")
        print("=" * 60)

        # Show deployed services
        self.show_deployments()

    def show_deployments(self):
        """Show all deployed services"""
        print("\n🌐 Deployed Services:")
        print("-" * 60)

        for name, info in self.deployments.items():
            print(f"✅ {name}")
            print(f"   Platform: {info['platform']}")
            print(f"   URL: {info['url']}")

        print("-" * 60)

    def run(self):
        """Main agent loop"""
        try:
            self.deploy_all_cloud_services()
        except Exception as e:
            print(f"❌ Cloud agent error: {e}")


if __name__ == "__main__":
    agent = CloudAgent()
    agent.run()
