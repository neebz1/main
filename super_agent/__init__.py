"""
Super Agent Orchestration System

Coordinates multiple AI agents working simultaneously without conflicts.
"""

__version__ = "1.0.0"

from .orchestrator import SuperAgent
from .context import AgentContext
from .resources import ResourceManager
from .router import TaskRouter

__all__ = [
    "SuperAgent",
    "AgentContext", 
    "ResourceManager",
    "TaskRouter"
]
