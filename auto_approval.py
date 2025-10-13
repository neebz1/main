"""
Auto-Approval System for Copilot Actions
Handles automatic approval of safe operations and requests
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AutoApprovalSystem:
    """System for automatically approving safe copilot actions"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize auto-approval system"""
        self.config_path = config_path or ".copilot_auto_approve.json"
        self.config = self.load_config()
        self.approval_log = []
        
    def load_config(self) -> Dict:
        """Load auto-approval configuration"""
        default_config = {
            "enabled": True,
            "auto_approve_categories": [
                "documentation",
                "formatting",
                "comments",
                "safe_refactoring",
                "dependency_updates_patch",
                "dependency_updates_minor"
            ],
            "safe_file_patterns": [
                "*.md",
                "*.txt",
                "*.yml",
                "*.yaml",
                ".gitignore",
                "README*",
                "LICENSE*"
            ],
            "safe_commands": [
                "git status",
                "git log",
                "git diff",
                "ls",
                "cat",
                "pwd",
                "echo"
            ],
            "require_approval_for": [
                "file_deletion",
                "system_modification",
                "dependency_major_update",
                "security_changes"
            ],
            "notification_settings": {
                "slack_webhook": None,
                "email": None,
                "log_approvals": True
            }
        }
        
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}. Using defaults.")
        
        return default_config
    
    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def should_auto_approve(self, action_type: str, details: Dict = None) -> tuple[bool, str]:
        """
        Check if an action should be auto-approved
        Returns: (should_approve, reason)
        """
        if not self.config.get("enabled", False):
            return False, "Auto-approval is disabled"
        
        details = details or {}
        
        # Check if action type is in auto-approve list
        if action_type in self.config.get("auto_approve_categories", []):
            reason = f"Auto-approved: {action_type} is in approved categories"
            self.log_approval(action_type, details, approved=True, reason=reason)
            return True, reason
        
        # Check if it's a safe file operation
        if action_type == "file_modification":
            file_path = details.get("file_path", "")
            if self._is_safe_file(file_path):
                reason = f"Auto-approved: {file_path} is a safe file type"
                self.log_approval(action_type, details, approved=True, reason=reason)
                return True, reason
        
        # Check if it's a safe command
        if action_type == "command_execution":
            command = details.get("command", "")
            if self._is_safe_command(command):
                reason = f"Auto-approved: '{command}' is a safe command"
                self.log_approval(action_type, details, approved=True, reason=reason)
                return True, reason
        
        # Require manual approval
        reason = f"Manual approval required for: {action_type}"
        self.log_approval(action_type, details, approved=False, reason=reason)
        return False, reason
    
    def _is_safe_file(self, file_path: str) -> bool:
        """Check if file is safe to auto-approve"""
        from fnmatch import fnmatch
        
        safe_patterns = self.config.get("safe_file_patterns", [])
        for pattern in safe_patterns:
            if fnmatch(file_path, pattern):
                return True
        return False
    
    def _is_safe_command(self, command: str) -> bool:
        """Check if command is safe to auto-approve"""
        safe_commands = self.config.get("safe_commands", [])
        
        # Check if command starts with any safe command
        for safe_cmd in safe_commands:
            if command.strip().startswith(safe_cmd):
                return True
        return False
    
    def log_approval(self, action_type: str, details: Dict, approved: bool, reason: str):
        """Log approval decision"""
        if not self.config.get("notification_settings", {}).get("log_approvals", True):
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
            "approved": approved,
            "reason": reason
        }
        
        self.approval_log.append(log_entry)
        
        # Keep only last 100 entries in memory
        if len(self.approval_log) > 100:
            self.approval_log = self.approval_log[-100:]
        
        # Optionally write to file
        self._write_log_entry(log_entry)
    
    def _write_log_entry(self, entry: Dict):
        """Write log entry to file"""
        log_file = Path(".copilot_approvals.log")
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"⚠️ Error writing log: {e}")
    
    def get_approval_stats(self) -> Dict:
        """Get statistics about approvals"""
        total = len(self.approval_log)
        if total == 0:
            return {
                "total": 0,
                "approved": 0,
                "rejected": 0,
                "approval_rate": 0
            }
        
        approved = sum(1 for entry in self.approval_log if entry["approved"])
        rejected = total - approved
        
        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": (approved / total) * 100 if total > 0 else 0
        }
    
    def enable_auto_approval(self):
        """Enable auto-approval system"""
        self.config["enabled"] = True
        self.save_config()
        return "✅ Auto-approval enabled"
    
    def disable_auto_approval(self):
        """Disable auto-approval system"""
        self.config["enabled"] = False
        self.save_config()
        return "⚠️ Auto-approval disabled"
    
    def add_safe_pattern(self, pattern: str):
        """Add a safe file pattern"""
        if pattern not in self.config["safe_file_patterns"]:
            self.config["safe_file_patterns"].append(pattern)
            self.save_config()
            return f"✅ Added safe pattern: {pattern}"
        return f"Pattern already exists: {pattern}"
    
    def add_safe_command(self, command: str):
        """Add a safe command"""
        if command not in self.config["safe_commands"]:
            self.config["safe_commands"].append(command)
            self.save_config()
            return f"✅ Added safe command: {command}"
        return f"Command already exists: {command}"


# Global instance
auto_approval = AutoApprovalSystem()
