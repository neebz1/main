"""
Resource Manager

Manages system resources like ports, API rate limits,
CPU/memory usage to prevent conflicts.
"""

import time
import psutil
from typing import Dict, Set, Optional, List
from collections import defaultdict


class ResourceManager:
    """
    Manages system resources and prevents conflicts
    """
    
    def __init__(self):
        self.ports_in_use: Dict[int, str] = {}        # {port: agent_name}
        self.api_calls: Dict[str, List[float]] = defaultdict(list)  # {service: [timestamps]}
        self.api_limits: Dict[str, int] = {
            'openrouter': 60,
            'kimi_k2': 100,
            'anthropic': 50,
            'openai': 60,
            'gemini': 60
        }
    
    def allocate_port(self, agent: str, preferred_port: int) -> Optional[int]:
        """
        Allocate a port for an agent.
        
        Args:
            agent: Agent name
            preferred_port: Desired port number
            
        Returns:
            Port number if available, None if unavailable
        """
        # Check if preferred port is available
        if preferred_port not in self.ports_in_use:
            if self._is_port_available(preferred_port):
                self.ports_in_use[preferred_port] = agent
                return preferred_port
        
        # Try to find alternative port
        for port in range(preferred_port, preferred_port + 100):
            if port not in self.ports_in_use and self._is_port_available(port):
                self.ports_in_use[port] = agent
                return port
        
        return None
    
    def release_port(self, port: int, agent: str) -> bool:
        """
        Release a port allocation.
        
        Args:
            port: Port number
            agent: Agent name
            
        Returns:
            True if released, False if not allocated to this agent
        """
        if port in self.ports_in_use and self.ports_in_use[port] == agent:
            del self.ports_in_use[port]
            return True
        return False
    
    def get_port_owner(self, port: int) -> Optional[str]:
        """Get the agent using a specific port"""
        return self.ports_in_use.get(port)
    
    def check_api_limit(self, service: str) -> bool:
        """
        Check if API rate limit allows another call.
        
        Args:
            service: Service name (openrouter, kimi_k2, etc.)
            
        Returns:
            True if call is allowed, False if rate limited
        """
        if service not in self.api_limits:
            return True  # No limit set
        
        limit = self.api_limits[service]
        current_time = time.time()
        
        # Remove timestamps older than 60 seconds
        self.api_calls[service] = [
            ts for ts in self.api_calls[service]
            if current_time - ts < 60
        ]
        
        # Check if under limit
        return len(self.api_calls[service]) < limit
    
    def track_api_call(self, service: str, agent: str):
        """
        Record an API call.
        
        Args:
            service: Service name
            agent: Agent making the call
        """
        self.api_calls[service].append(time.time())
    
    def get_api_calls_remaining(self, service: str) -> int:
        """
        Get number of API calls remaining in current minute.
        
        Args:
            service: Service name
            
        Returns:
            Number of calls available
        """
        if service not in self.api_limits:
            return 999  # Unlimited
        
        limit = self.api_limits[service]
        current_time = time.time()
        
        # Count recent calls
        recent_calls = sum(
            1 for ts in self.api_calls[service]
            if current_time - ts < 60
        )
        
        return max(0, limit - recent_calls)
    
    def wait_for_api_availability(self, service: str, timeout: int = 60) -> bool:
        """
        Wait until API call is available.
        
        Args:
            service: Service name
            timeout: Maximum wait time in seconds
            
        Returns:
            True if available, False if timed out
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_api_limit(service):
                return True
            time.sleep(0.5)
        
        return False
    
    def get_system_resources(self) -> Dict:
        """
        Get current system resource usage.
        
        Returns:
            Dictionary with CPU, memory, disk usage
        """
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'disk_percent': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections())
        }
    
    def is_system_overloaded(self) -> bool:
        """
        Check if system resources are critically low.
        
        Returns:
            True if system is overloaded
        """
        resources = self.get_system_resources()
        
        return (
            resources['cpu_percent'] > 90 or
            resources['memory_percent'] > 90 or
            resources['disk_percent'] > 95
        )
    
    def get_resource_summary(self) -> Dict:
        """
        Get summary of all managed resources.
        
        Returns:
            Dictionary with ports, API limits, system resources
        """
        system = self.get_system_resources()
        
        api_status = {}
        for service in self.api_limits.keys():
            api_status[service] = {
                'limit': self.api_limits[service],
                'remaining': self.get_api_calls_remaining(service),
                'usage_percent': (1 - self.get_api_calls_remaining(service) / self.api_limits[service]) * 100
            }
        
        return {
            'ports': self.ports_in_use,
            'api_limits': api_status,
            'system': system,
            'overloaded': self.is_system_overloaded()
        }
    
    def _is_port_available(self, port: int) -> bool:
        """
        Check if a port is actually available on the system.
        
        Args:
            port: Port number to check
            
        Returns:
            True if available
        """
        connections = psutil.net_connections()
        for conn in connections:
            if conn.laddr.port == port:
                return False
        return True
    
    def set_api_limit(self, service: str, limit: int):
        """
        Set or update API rate limit for a service.
        
        Args:
            service: Service name
            limit: Calls per minute
        """
        self.api_limits[service] = limit
