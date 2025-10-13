"""
Agent Context Manager

Provides shared memory and state across all agents
to prevent conflicts and enable coordination.
"""

import json
import time
from typing import Dict, List, Set, Any, Optional
from datetime import datetime
from pathlib import Path


class AgentContext:
    """
    Shared context accessible by all agents.
    Prevents conflicts and enables information sharing.
    """
    
    def __init__(self, context_file: str = ".super_agent_context.json"):
        self.context_file = Path(context_file)
        
        # In-memory state
        self.files_locked: Dict[str, Dict] = {}  # {filepath: {agent, timestamp}}
        self.recent_actions: List[Dict] = []     # Recent agent actions
        self.goals: List[str] = []               # Current goals
        self.knowledge_base: Dict[str, Any] = {} # Shared knowledge
        self.agent_states: Dict[str, str] = {}   # {agent_name: status}
        
        # Load persisted context if exists
        self._load_context()
    
    def lock_file(self, filepath: str, agent: str, timeout: int = 300) -> bool:
        """
        Acquire exclusive lock on a file for editing.
        
        Args:
            filepath: Path to file to lock
            agent: Name of agent requesting lock
            timeout: Lock timeout in seconds
            
        Returns:
            True if lock acquired, False if already locked
        """
        filepath = str(Path(filepath).resolve())
        
        # Check if already locked
        if filepath in self.files_locked:
            lock_info = self.files_locked[filepath]
            lock_age = time.time() - lock_info['timestamp']
            
            # If lock expired, remove it
            if lock_age > timeout:
                del self.files_locked[filepath]
            else:
                # Still locked by another agent
                if lock_info['agent'] != agent:
                    return False
        
        # Acquire lock
        self.files_locked[filepath] = {
            'agent': agent,
            'timestamp': time.time()
        }
        
        self.add_action(agent, f"Locked file: {filepath}", "success")
        self._save_context()
        return True
    
    def release_file(self, filepath: str, agent: str) -> bool:
        """
        Release file lock.
        
        Args:
            filepath: Path to file to unlock
            agent: Name of agent releasing lock
            
        Returns:
            True if released, False if not locked by this agent
        """
        filepath = str(Path(filepath).resolve())
        
        if filepath not in self.files_locked:
            return False
            
        if self.files_locked[filepath]['agent'] != agent:
            return False
        
        del self.files_locked[filepath]
        self.add_action(agent, f"Released file: {filepath}", "success")
        self._save_context()
        return True
    
    def is_file_locked(self, filepath: str) -> Optional[str]:
        """
        Check if file is locked.
        
        Returns:
            Agent name if locked, None if available
        """
        filepath = str(Path(filepath).resolve())
        
        if filepath in self.files_locked:
            return self.files_locked[filepath]['agent']
        return None
    
    def add_action(self, agent: str, action: str, status: str, details: Dict = None):
        """
        Log an agent action for others to see.
        
        Args:
            agent: Name of agent
            action: Description of action
            status: "success", "failure", "in_progress"
            details: Optional additional information
        """
        action_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'action': action,
            'status': status,
            'details': details or {}
        }
        
        self.recent_actions.append(action_entry)
        
        # Keep only last 100 actions
        if len(self.recent_actions) > 100:
            self.recent_actions = self.recent_actions[-100:]
        
        self._save_context()
    
    def get_recent_actions(self, agent: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get recent actions, optionally filtered by agent.
        
        Args:
            agent: Optional agent name to filter by
            limit: Maximum number of actions to return
            
        Returns:
            List of recent actions
        """
        actions = self.recent_actions
        
        if agent:
            actions = [a for a in actions if a['agent'] == agent]
        
        return actions[-limit:]
    
    def share_knowledge(self, key: str, value: Any, agent: str):
        """
        Share information that other agents can access.
        
        Args:
            key: Knowledge identifier
            value: Any JSON-serializable value
            agent: Agent sharing the knowledge
        """
        self.knowledge_base[key] = {
            'value': value,
            'shared_by': agent,
            'timestamp': datetime.now().isoformat()
        }
        
        self.add_action(agent, f"Shared knowledge: {key}", "success")
        self._save_context()
    
    def get_knowledge(self, key: str) -> Optional[Any]:
        """
        Retrieve shared knowledge.
        
        Args:
            key: Knowledge identifier
            
        Returns:
            Knowledge value if exists, None otherwise
        """
        if key in self.knowledge_base:
            return self.knowledge_base[key]['value']
        return None
    
    def add_goal(self, goal: str):
        """Add a goal to work towards"""
        if goal not in self.goals:
            self.goals.append(goal)
            self._save_context()
    
    def complete_goal(self, goal: str):
        """Mark a goal as complete"""
        if goal in self.goals:
            self.goals.remove(goal)
            self._save_context()
    
    def get_goals(self) -> List[str]:
        """Get all current goals"""
        return self.goals.copy()
    
    def set_agent_state(self, agent: str, state: str):
        """
        Update agent state.
        
        Args:
            agent: Agent name
            state: "idle", "active", "busy", "error"
        """
        self.agent_states[agent] = state
        self._save_context()
    
    def get_agent_state(self, agent: str) -> str:
        """Get agent's current state"""
        return self.agent_states.get(agent, "unknown")
    
    def get_all_agent_states(self) -> Dict[str, str]:
        """Get all agent states"""
        return self.agent_states.copy()
    
    def clear_old_locks(self, max_age: int = 300):
        """
        Remove locks older than max_age seconds.
        
        Args:
            max_age: Maximum lock age in seconds
        """
        current_time = time.time()
        expired = []
        
        for filepath, lock_info in self.files_locked.items():
            if current_time - lock_info['timestamp'] > max_age:
                expired.append(filepath)
        
        for filepath in expired:
            agent = self.files_locked[filepath]['agent']
            del self.files_locked[filepath]
            self.add_action("system", f"Released expired lock: {filepath} (was held by {agent})", "success")
        
        if expired:
            self._save_context()
    
    def _save_context(self):
        """Persist context to disk"""
        try:
            data = {
                'files_locked': self.files_locked,
                'recent_actions': self.recent_actions[-100:],  # Only keep recent
                'goals': self.goals,
                'knowledge_base': self.knowledge_base,
                'agent_states': self.agent_states,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.context_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save context: {e}")
    
    def _load_context(self):
        """Load persisted context from disk"""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    
                self.files_locked = data.get('files_locked', {})
                self.recent_actions = data.get('recent_actions', [])
                self.goals = data.get('goals', [])
                self.knowledge_base = data.get('knowledge_base', {})
                self.agent_states = data.get('agent_states', {})
                
                # Clear any expired locks
                self.clear_old_locks()
        except Exception as e:
            print(f"Warning: Could not load context: {e}")
