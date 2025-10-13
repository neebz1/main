"""
Base Agent Adapter

Abstract base class for all agent adapters
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAdapter(ABC):
    """
    Base class for agent adapters
    """
    
    def __init__(self, agent_name: str, super_agent):
        """
        Initialize adapter.
        
        Args:
            agent_name: Name of the agent
            super_agent: Reference to SuperAgent orchestrator
        """
        self.agent_name = agent_name
        self.super_agent = super_agent
        self.capabilities = []
    
    @abstractmethod
    async def execute(self, task: str, context: Dict = None) -> Any:
        """
        Execute a task with this agent.
        
        Args:
            task: Task description
            context: Optional task context
            
        Returns:
            Task result
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if agent is currently available.
        
        Returns:
            True if available
        """
        pass
    
    def get_status(self) -> Dict:
        """
        Get agent status.
        
        Returns:
            Status dictionary
        """
        return {
            'name': self.agent_name,
            'available': self.is_available(),
            'capabilities': self.capabilities
        }
