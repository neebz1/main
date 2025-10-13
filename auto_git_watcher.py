#!/usr/bin/env python3
"""
Autonomous Git Watcher - Automatically commits and pushes changes
Monitors the repository for changes and auto-commits them periodically
"""

import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()


class AutoGitWatcher:
    """
    Watches for changes and automatically commits/pushes them
    """
    
    def __init__(self, project_dir="/Users/nr/main", interval=300):
        """
        Initialize the auto git watcher
        
        Args:
            project_dir: Path to the git repository
            interval: Time in seconds between checks (default: 300 = 5 minutes)
        """
        self.project_dir = Path(project_dir)
        self.interval = interval
        self.running = False
        
        # Load config
        self.config_file = self.project_dir / ".auto_git_config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "enabled": True,
            "interval": 300,
            "auto_push": True,
            "commit_message_template": "Auto-commit: {timestamp}",
            "ignore_patterns": [
                "*.pyc",
                "__pycache__",
                ".DS_Store",
                "*.log",
                ".env",
                "venv/",
                ".cursor/",
                ".git/"
            ]
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
        
        self.config = default_config
        self.interval = self.config.get("interval", 300)
        
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving config: {e}")
    
    def has_changes(self) -> bool:
        """Check if there are uncommitted changes"""
        try:
            result = subprocess.run(
                "git status --porcelain",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            return bool(result.stdout.strip())
        except Exception as e:
            print(f"❌ Error checking git status: {e}")
            return False
    
    def get_changes_summary(self) -> str:
        """Get a summary of current changes"""
        try:
            result = subprocess.run(
                "git status --short",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"
    
    def commit_and_push(self) -> bool:
        """Commit all changes and push to remote"""
        try:
            # Add all changes
            subprocess.run(
                "git add -A",
                shell=True,
                cwd=self.project_dir,
                check=True,
                capture_output=True
            )
            
            # Generate commit message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = self.config["commit_message_template"].format(
                timestamp=timestamp
            )
            
            # Commit
            commit_result = subprocess.run(
                f'git commit -m "{commit_msg}"',
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if commit_result.returncode != 0:
                # Check if it's just "nothing to commit"
                if "nothing to commit" in commit_result.stdout.lower():
                    return True
                print(f"⚠️  Commit failed: {commit_result.stderr}")
                return False
            
            print(f"✅ Committed: {commit_msg}")
            
            # Push if enabled
            if self.config["auto_push"]:
                push_result = subprocess.run(
                    "git push origin main",
                    shell=True,
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if push_result.returncode == 0:
                    print(f"✅ Pushed to remote")
                    return True
                else:
                    print(f"⚠️  Push failed: {push_result.stderr}")
                    # Try alternative branches
                    alt_result = subprocess.run(
                        "git push",
                        shell=True,
                        cwd=self.project_dir,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if alt_result.returncode == 0:
                        print(f"✅ Pushed to remote (default branch)")
                        return True
                    return False
            
            return True
            
        except subprocess.TimeoutExpired:
            print("⚠️  Git operation timed out")
            return False
        except Exception as e:
            print(f"❌ Error in commit/push: {e}")
            return False
    
    def watch(self):
        """Start watching for changes"""
        self.running = True
        print("🤖 Autonomous Git Watcher Started")
        print("=" * 60)
        print(f"📁 Watching: {self.project_dir}")
        print(f"⏱️  Check interval: {self.interval} seconds")
        print(f"🚀 Auto-push: {'Enabled' if self.config['auto_push'] else 'Disabled'}")
        print("=" * 60)
        
        try:
            while self.running:
                if self.has_changes():
                    print(f"\n📝 Changes detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    changes = self.get_changes_summary()
                    print(f"Changes:\n{changes}\n")
                    
                    if self.commit_and_push():
                        print("✅ Auto-commit successful\n")
                    else:
                        print("⚠️  Auto-commit failed\n")
                else:
                    print(f"✓ No changes at {datetime.now().strftime('%H:%M:%S')}", end="\r")
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping autonomous git watcher...")
            self.running = False
    
    def stop(self):
        """Stop watching"""
        self.running = False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Autonomous Git Watcher")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Check interval in seconds (default: 300)"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="/Users/nr/main",
        help="Project directory to watch"
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Disable automatic pushing"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (no continuous watching)"
    )
    
    args = parser.parse_args()
    
    watcher = AutoGitWatcher(project_dir=args.dir, interval=args.interval)
    
    if args.no_push:
        watcher.config["auto_push"] = False
        watcher.save_config()
    
    if args.once:
        # Run once and exit
        print("🔍 Checking for changes...")
        if watcher.has_changes():
            print("📝 Changes detected, committing...")
            if watcher.commit_and_push():
                print("✅ Done!")
            else:
                print("❌ Failed!")
        else:
            print("✓ No changes detected")
    else:
        # Start continuous watching
        watcher.watch()


if __name__ == "__main__":
    main()
