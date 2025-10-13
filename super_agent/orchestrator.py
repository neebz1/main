"""
Super Agent Orchestrator

Main coordinator that manages all AI agents and ensures
they work together without conflicts.
"""

import asyncio
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path for imports when run as script
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from super_agent.context import AgentContext
    from super_agent.resources import ResourceManager
    from super_agent.router import TaskRouter
else:
    from .context import AgentContext
    from .resources import ResourceManager
    from .router import TaskRouter


class SuperAgent:
    """
    Main orchestrator for multi-agent coordination
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize Super Agent orchestrator.
        
        Args:
            config_file: Optional YAML config file
        """
        # Initialize subsystems
        self.context = AgentContext()
        self.resources = ResourceManager()
        
        # Agent registry
        self.agents = self._initialize_agents()
        
        # Task router
        self.router = TaskRouter(self.agents)
        
        # State
        self.running = False
        self._task_queue = asyncio.Queue()
    
    def _initialize_agents(self) -> Dict[str, Dict]:
        """
        Initialize agent registry with known agents.
        
        Returns:
            Dictionary of agent configurations
        """
        return {
            # Coding agents
            'cline': {
                'type': 'ide_extension',
                'capabilities': ['code_generation', 'file_edit', 'terminal', 'debug'],
                'priority': 9,
                'status': 'idle',
                'port': None
            },
            'cursor_ai': {
                'type': 'ide_builtin',
                'capabilities': ['code_generation', 'chat', 'inline_edit'],
                'priority': 8,
                'status': 'idle',
                'port': None
            },
            'github_copilot': {
                'type': 'ide_extension',
                'capabilities': ['code_completion', 'suggestions'],
                'priority': 7,
                'status': 'idle',
                'port': None
            },
            
            # Music agents
            'logic_copilot': {
                'type': 'web_service',
                'capabilities': ['music_chat', 'production_tips', 'sound_packs'],
                'priority': 8,
                'status': 'idle',
                'port': 7860
            },
            'mixing_engineer': {
                'type': 'web_service',
                'capabilities': ['audio_analysis', 'mixing_suggestions', 'visualization'],
                'priority': 9,
                'status': 'idle',
                'port': 7861
            },
            'live_ai_assistant': {
                'type': 'standalone',
                'capabilities': ['voice', 'vision', 'screen_capture', 'realtime'],
                'priority': 8,
                'status': 'idle',
                'port': None
            },
            'logic_ai_plugin': {
                'type': 'standalone',
                'capabilities': ['osc_control', 'logic_automation', 'vision', 'realtime'],
                'priority': 9,
                'status': 'idle',
                'port': None
            },
            
            # Documentation agents
            'docs_agent': {
                'type': 'api_service',
                'capabilities': ['doc_search', 'indexing', 'embedding', 'rag'],
                'priority': 7,
                'status': 'idle',
                'port': 8000
            }
        }
    
    async def execute(self, task: str, agent: str = None, context: Dict = None) -> Dict:
        """
        Execute a task using the appropriate agent(s).
        
        Args:
            task: Task description
            agent: Optional specific agent to use
            context: Optional task context
            
        Returns:
            {
                'status': 'success' | 'failure',
                'agent': agent_name,
                'result': any,
                'message': str
            }
        """
        # Route to appropriate agent if not specified
        if agent is None:
            routing = self.router.route_task(task, context)
            agent = routing['agent']
            
            if agent is None:
                return {
                    'status': 'failure',
                    'agent': None,
                    'result': None,
                    'message': 'No suitable agent found for task'
                }
        
        # Check if agent exists
        if agent not in self.agents:
            return {
                'status': 'failure',
                'agent': agent,
                'result': None,
                'message': f'Agent "{agent}" not found'
            }
        
        # Update agent state
        self.context.set_agent_state(agent, 'active')
        self.context.add_action(agent, f"Executing: {task[:100]}", 'in_progress')
        
        try:
            # Execute via agent adapter
            result = await self._execute_with_agent(agent, task, context)
            
            # Update state
            self.context.set_agent_state(agent, 'idle')
            self.context.add_action(agent, f"Completed: {task[:100]}", 'success', {'result': str(result)[:200]})
            
            return {
                'status': 'success',
                'agent': agent,
                'result': result,
                'message': f'Task completed by {agent}'
            }
            
        except Exception as e:
            # Update state on error
            self.context.set_agent_state(agent, 'error')
            self.context.add_action(agent, f"Failed: {task[:100]}", 'failure', {'error': str(e)})
            
            return {
                'status': 'failure',
                'agent': agent,
                'result': None,
                'message': f'Error: {str(e)}'
            }
    
    async def execute_complex(self, task: str, subtasks: List[str] = None) -> Dict:
        """
        Execute a complex task using multiple agents.
        
        Args:
            task: Main task description
            subtasks: Optional list of subtasks
            
        Returns:
            {
                'status': 'success' | 'failure',
                'coordinator': agent_name,
                'agents': [agent_names],
                'results': [results],
                'message': str
            }
        """
        # Route complex task
        routing = self.router.route_complex_task(task, subtasks)
        
        # Execute subtasks
        results = []
        for step in routing['plan']:
            result = await self.execute(step['task'], agent=step['agent'])
            results.append(result)
            
            # If any subtask fails, stop
            if result['status'] == 'failure':
                return {
                    'status': 'failure',
                    'coordinator': routing['coordinator'],
                    'agents': routing['agents'],
                    'results': results,
                    'message': f'Failed at step {step["order"]}: {result["message"]}'
                }
        
        return {
            'status': 'success',
            'coordinator': routing['coordinator'],
            'agents': routing['agents'],
            'results': results,
            'message': 'Complex task completed successfully'
        }
    
    async def _execute_with_agent(self, agent: str, task: str, context: Dict = None) -> Any:
        """
        Execute task via specific agent adapter.
        
        This is a stub - actual implementation would use agent-specific APIs.
        """
        # In a real implementation, this would:
        # 1. Load the appropriate adapter for the agent
        # 2. Call the adapter's execute method
        # 3. Return the result
        
        # For now, just simulate execution
        print(f"[{agent}] Executing: {task}")
        await asyncio.sleep(0.1)  # Simulate work
        
        return f"Simulated result from {agent}"
    
    def get_status(self) -> Dict:
        """
        Get current status of all agents and resources.
        
        Returns:
            Comprehensive status dictionary
        """
        agent_states = {}
        for name, info in self.agents.items():
            agent_states[name] = {
                'type': info['type'],
                'status': self.context.get_agent_state(name) or 'idle',
                'capabilities': info['capabilities'],
                'priority': info['priority']
            }
        
        return {
            'agents': agent_states,
            'resources': self.resources.get_resource_summary(),
            'context': {
                'locked_files': list(self.context.files_locked.keys()),
                'active_goals': self.context.get_goals(),
                'recent_actions': self.context.get_recent_actions(limit=5)
            }
        }
    
    def get_activity_log(self, agent: str = None, limit: int = 10) -> List[Dict]:
        """
        Get recent activity log.
        
        Args:
            agent: Optional agent name to filter by
            limit: Maximum number of actions to return
            
        Returns:
            List of recent actions
        """
        return self.context.get_recent_actions(agent=agent, limit=limit)
    
    def register_agent(self, name: str, config: Dict):
        """
        Register a new agent.
        
        Args:
            name: Agent name
            config: Agent configuration
        """
        self.agents[name] = config
        self.router.register_agent(
            name,
            config.get('capabilities', []),
            config.get('priority', 5)
        )
    
    def route_task(self, task: str) -> Dict:
        """
        Route a task without executing it.
        
        Args:
            task: Task description
            
        Returns:
            Routing information
        """
        return self.router.route_task(task)
    
    def start_monitoring(self):
        """Start background monitoring of agents and resources"""
        self.running = True
        asyncio.create_task(self._monitor_loop())
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.running = False
    
    async def _monitor_loop(self):
        """Background loop for monitoring and cleanup"""
        while self.running:
            # Clean up expired file locks
            self.context.clear_old_locks(max_age=300)
            
            # Check system resources
            if self.resources.is_system_overloaded():
                print("⚠️ Warning: System resources are critically low")
            
            await asyncio.sleep(30)  # Check every 30 seconds


def main():
    """
    Main entry point for super agent
    """
    print("🦸 Super Agent Orchestrator")
    print("=" * 60)
    
    # Initialize
    sa = SuperAgent()
    
    # Show status
    status = sa.get_status()
    print(f"\n✅ Initialized with {len(status['agents'])} agents:")
    for name, info in status['agents'].items():
        print(f"   - {name:20} [{info['type']:15}] {info['status']}")
    
    print("\n📊 System Resources:")
    resources = status['resources']['system']
    print(f"   - CPU: {resources['cpu_percent']:.1f}%")
    print(f"   - Memory: {resources['memory_percent']:.1f}%")
    print(f"   - Available Memory: {resources['memory_available_gb']:.1f} GB")
    
    print("\n🚀 Super Agent ready!")
    print("   Use programmatically or start the dashboard")
    print("=" * 60)


if __name__ == '__main__':
    main()
