#!/usr/bin/env python3
"""
👁️ Autonomous Monitoring Agent
Monitors all services and auto-heals when issues are detected
"""

import subprocess
import time
from datetime import datetime
from pathlib import Path

import requests


class MonitoringAgent:
    def __init__(self):
        self.services = {
            "AI Mixing Engineer": {
                "type": "http",
                "url": "http://localhost:7861",
                "script": "start-ai-mixing-engineer.sh",
            },
            "Music Copilot": {
                "type": "http",
                "url": "http://localhost:7860",
                "script": "start-music-ai.sh",
            },
        }

        self.base_dir = Path("/Users/nr/Documents/GitHub/main")
        self.logs = []

    def check_http_service(self, name: str, url: str) -> bool:
        """Check if HTTP service is responding"""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def restart_service(self, name: str, script: str):
        """Restart a failed service"""
        print(f"🔄 Restarting {name}...")

        try:
            script_path = self.base_dir / script
            subprocess.Popen(
                ["bash", str(script_path)],
                cwd=str(self.base_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            time.sleep(5)  # Wait for service to start
            print(f"✅ {name} restarted")

            self.log_event(name, "restarted")

        except Exception as e:
            print(f"❌ Failed to restart {name}: {e}")
            self.log_event(name, f"restart_failed: {e}")

    def log_event(self, service: str, event: str):
        """Log monitoring events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {service}: {event}"
        self.logs.append(log_entry)

        # Write to file
        log_file = self.base_dir / "agents" / "monitoring.log"
        with open(log_file, "a") as f:
            f.write(log_entry + "\n")

    def monitor_all_services(self):
        """Monitor all services continuously"""
        print("\n" + "=" * 60)
        print("👁️ AUTONOMOUS MONITORING AGENT")
        print("Monitoring all services...")
        print("=" * 60)
        print("\nPress Ctrl+C to stop\n")

        check_interval = 30  # seconds

        try:
            while True:
                print(
                    f"\n🔍 Checking services... [{datetime.now().strftime('%H:%M:%S')}]"
                )

                for name, config in self.services.items():
                    if config["type"] == "http":
                        is_healthy = self.check_http_service(name, config["url"])

                        if is_healthy:
                            print(f"  🟢 {name}: OK")
                        else:
                            print(f"  🔴 {name}: DOWN - Auto-healing...")
                            self.log_event(name, "service_down")
                            self.restart_service(name, config["script"])

                print(f"\n⏳ Next check in {check_interval} seconds...")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")
            self.show_summary()

    def show_summary(self):
        """Show monitoring summary"""
        print("\n" + "=" * 60)
        print("📊 Monitoring Summary")
        print("=" * 60)
        print(f"Total events logged: {len(self.logs)}")

        if self.logs:
            print("\nRecent events:")
            for log in self.logs[-10:]:
                print(f"  {log}")

    def run(self):
        """Main agent loop"""
        self.monitor_all_services()


if __name__ == "__main__":
    agent = MonitoringAgent()
    agent.run()
