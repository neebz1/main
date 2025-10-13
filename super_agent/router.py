"""
Task Router

Intelligently routes tasks to the most appropriate agent
based on capabilities, availability, and priority.
"""

from typing import List, Dict, Optional, Any
import re


class TaskRouter:
    """
    Routes tasks to the most appropriate agent(s)
    """
    
    def __init__(self, agent_registry: Dict[str, Dict]):
        """
        Initialize router with agent registry.
        
        Args:
            agent_registry: {agent_name: {capabilities, priority, status, ...}}
        """
        self.agents = agent_registry
        
        # Task patterns for automatic routing
        self.routing_patterns = {
            'code_generation': {
                'patterns': [
                    r'create.*function',
                    r'write.*code',
                    r'implement.*',
                    r'generate.*script',
                    r'build.*app'
                ],
                'preferred_agents': ['cline', 'cursor_ai'],
                'fallback_agents': ['github_copilot']
            },
            'code_refactoring': {
                'patterns': [
                    r'refactor',
                    r'reorganize.*code',
                    r'migrate.*',
                    r'restructure'
                ],
                'preferred_agents': ['cline'],
                'fallback_agents': ['cursor_ai']
            },
            'audio_analysis': {
                'patterns': [
                    r'analyze.*audio',
                    r'mix.*track',
                    r'check.*levels',
                    r'eq.*recommendation'
                ],
                'preferred_agents': ['mixing_engineer'],
                'fallback_agents': []
            },
            'music_production': {
                'patterns': [
                    r'(how|what|why).*logic pro',
                    r'production.*tip',
                    r'sound.*pack',
                    r'beat.*making'
                ],
                'preferred_agents': ['logic_copilot'],
                'fallback_agents': ['mixing_engineer']
            },
            'documentation_search': {
                'patterns': [
                    r'search.*docs',
                    r'find.*documentation',
                    r'lookup.*api',
                    r'how to.*in'
                ],
                'preferred_agents': ['docs_agent'],
                'fallback_agents': ['cursor_ai']
            },
            'realtime_assistance': {
                'patterns': [
                    r'watch.*screen',
                    r'voice.*command',
                    r'real.*time',
                    r'live.*assist'
                ],
                'preferred_agents': ['live_ai_assistant', 'logic_ai_plugin'],
                'fallback_agents': []
            }
        }
    
    def route_task(self, task: str, context: Dict = None) -> Dict:
        """
        Route a task to the best agent.
        
        Args:
            task: Task description
            context: Optional context (current file, project, etc.)
            
        Returns:
            {
                'agent': agent_name,
                'confidence': 0-1,
                'reasoning': str,
                'alternatives': [agent_names]
            }
        """
        # Analyze task to determine type
        task_type = self._analyze_task(task)
        
        # Get agents capable of handling this task
        capable_agents = self._get_capable_agents(task_type)
        
        if not capable_agents:
            return {
                'agent': None,
                'confidence': 0,
                'reasoning': f"No agents available for task type: {task_type}",
                'alternatives': []
            }
        
        # Select best agent based on priority and availability
        selected_agent = self._select_best_agent(capable_agents, task)
        
        # Get alternatives
        alternatives = [a for a in capable_agents if a != selected_agent]
        
        return {
            'agent': selected_agent,
            'confidence': self._calculate_confidence(selected_agent, task_type),
            'reasoning': self._explain_selection(selected_agent, task_type),
            'alternatives': alternatives
        }
    
    def route_complex_task(self, task: str, subtasks: List[str] = None) -> Dict:
        """
        Route a complex task that may require multiple agents.
        
        Args:
            task: Main task description
            subtasks: Optional list of subtasks
            
        Returns:
            {
                'coordinator': agent_name,
                'agents': [agent_names],
                'plan': [{'agent': agent, 'task': task, 'order': int}]
            }
        """
        if not subtasks:
            subtasks = self._decompose_task(task)
        
        plan = []
        agents_needed = set()
        
        for i, subtask in enumerate(subtasks):
            routing = self.route_task(subtask)
            if routing['agent']:
                plan.append({
                    'agent': routing['agent'],
                    'task': subtask,
                    'order': i + 1
                })
                agents_needed.add(routing['agent'])
        
        # Select coordinator (usually the highest priority agent involved)
        coordinator = self._select_coordinator(list(agents_needed))
        
        return {
            'coordinator': coordinator,
            'agents': list(agents_needed),
            'plan': plan
        }
    
    def _analyze_task(self, task: str) -> str:
        """
        Analyze task to determine type.
        
        Returns:
            Task type string
        """
        task_lower = task.lower()
        
        # Check against patterns
        for task_type, config in self.routing_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, task_lower):
                    return task_type
        
        # Default to code generation if unclear
        return 'code_generation'
    
    def _get_capable_agents(self, task_type: str) -> List[str]:
        """
        Get agents capable of handling task type.
        
        Returns:
            List of agent names
        """
        if task_type in self.routing_patterns:
            config = self.routing_patterns[task_type]
            preferred = [a for a in config['preferred_agents'] if a in self.agents]
            fallback = [a for a in config['fallback_agents'] if a in self.agents]
            return preferred + fallback
        
        # If no specific routing, return all available agents
        return list(self.agents.keys())
    
    def _select_best_agent(self, capable_agents: List[str], task: str) -> Optional[str]:
        """
        Select the best agent from capable agents.
        
        Returns:
            Agent name
        """
        if not capable_agents:
            return None
        
        # Filter by availability
        available = [
            a for a in capable_agents
            if self.agents[a].get('status', 'idle') in ['idle', 'active']
        ]
        
        if not available:
            available = capable_agents  # Use busy agents if no idle ones
        
        # Sort by priority (higher is better)
        sorted_agents = sorted(
            available,
            key=lambda a: self.agents[a].get('priority', 5),
            reverse=True
        )
        
        return sorted_agents[0]
    
    def _select_coordinator(self, agents: List[str]) -> str:
        """
        Select coordinator for multi-agent task.
        
        Returns:
            Agent name
        """
        if not agents:
            return 'cline'  # Default coordinator
        
        # Prefer Cline for complex coordination
        if 'cline' in agents:
            return 'cline'
        
        # Otherwise, highest priority agent
        return max(agents, key=lambda a: self.agents[a].get('priority', 5))
    
    def _calculate_confidence(self, agent: str, task_type: str) -> float:
        """
        Calculate confidence score for agent selection.
        
        Returns:
            Confidence score 0-1
        """
        if task_type in self.routing_patterns:
            config = self.routing_patterns[task_type]
            if agent in config['preferred_agents']:
                return 0.9
            elif agent in config['fallback_agents']:
                return 0.6
        
        return 0.5
    
    def _explain_selection(self, agent: str, task_type: str) -> str:
        """
        Generate human-readable explanation for selection.
        
        Returns:
            Explanation string
        """
        reasons = []
        
        if task_type in self.routing_patterns:
            config = self.routing_patterns[task_type]
            if agent in config['preferred_agents']:
                reasons.append(f"Best suited for {task_type}")
            elif agent in config['fallback_agents']:
                reasons.append(f"Can handle {task_type}")
        
        if self.agents.get(agent, {}).get('priority', 0) >= 8:
            reasons.append("High priority agent")
        
        agent_status = self.agents.get(agent, {}).get('status', 'unknown')
        if agent_status == 'idle':
            reasons.append("Currently available")
        
        return "; ".join(reasons) if reasons else "Selected by default"
    
    def _decompose_task(self, task: str) -> List[str]:
        """
        Break down a complex task into subtasks.
        
        Returns:
            List of subtask descriptions
        """
        # Simple decomposition based on common patterns
        if "and" in task.lower():
            return [t.strip() for t in task.split(" and ")]
        
        # Look for numbered steps
        if any(str(i) + "." in task or str(i) + ")" in task for i in range(1, 10)):
            lines = task.split("\n")
            subtasks = []
            for line in lines:
                line = line.strip()
                if any(line.startswith(str(i)) for i in range(1, 10)):
                    # Remove number prefix
                    subtask = re.sub(r'^\d+[.)]?\s*', '', line)
                    if subtask:
                        subtasks.append(subtask)
            return subtasks
        
        # If can't decompose, return as single task
        return [task]
    
    def update_agent_status(self, agent: str, status: str):
        """
        Update agent status.
        
        Args:
            agent: Agent name
            status: New status (idle, active, busy, error)
        """
        if agent in self.agents:
            self.agents[agent]['status'] = status
    
    def register_agent(self, name: str, capabilities: List[str], priority: int = 5):
        """
        Register a new agent.
        
        Args:
            name: Agent name
            capabilities: List of capabilities
            priority: Priority (1-10, higher is better)
        """
        self.agents[name] = {
            'capabilities': capabilities,
            'priority': priority,
            'status': 'idle'
        }
    
    def unregister_agent(self, name: str):
        """Remove an agent from registry"""
        if name in self.agents:
            del self.agents[name]
