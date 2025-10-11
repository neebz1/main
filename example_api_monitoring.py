#!/usr/bin/env python3
"""
Example: Integrating API Monitor with AI Applications

This example shows how to use the API monitor for:
1. Health checks before making API calls
2. Automatic failover when APIs fail
3. Usage tracking
4. Cost monitoring
"""

import os
import asyncio
from api_monitor import APIMonitor, APIProvider


class AIApplicationWithMonitoring:
    """
    Example AI application with built-in API monitoring
    """
    
    def __init__(self):
        self.monitor = APIMonitor()
        self.preferred_provider = APIProvider.TOGETHER_AI.value
    
    async def call_ai_with_failover(self, prompt: str, max_tokens: int = 500):
        """
        Call AI API with automatic failover
        """
        # Check current provider health
        await self.monitor.check_all_providers()
        
        # Get healthy providers
        healthy = self.monitor.get_healthy_providers()
        
        if self.preferred_provider in healthy:
            provider = self.preferred_provider
            print(f"✅ Using preferred provider: {provider}")
        else:
            # Get failover
            provider = self.monitor.get_failover_provider(self.preferred_provider)
            
            if not provider:
                raise Exception("No healthy API providers available!")
            
            print(f"⚠️  Preferred provider unavailable, using failover: {provider}")
        
        # Make API call (simulated)
        result = await self._call_api(provider, prompt, max_tokens)
        
        # Track usage
        tokens_used = len(prompt.split()) + max_tokens  # Simplified
        self.monitor.track_usage(provider, tokens_used)
        
        print(f"📊 Tracked {tokens_used} tokens for {provider}")
        
        return result
    
    async def _call_api(self, provider: str, prompt: str, max_tokens: int):
        """
        Simulate API call
        In real implementation, this would call the actual API
        """
        # Simulated API call
        await asyncio.sleep(0.5)  # Simulate network delay
        
        return {
            "provider": provider,
            "response": "This is a simulated AI response",
            "tokens": max_tokens
        }
    
    def get_cost_report(self):
        """Get cost and usage report"""
        report = self.monitor.get_status_report()
        
        print("\n" + "=" * 60)
        print("💰 COST REPORT")
        print("=" * 60)
        print(f"\nTotal Cost: ${report['summary']['total_cost_usd']:.4f}")
        print(f"Total Tokens: {report['summary']['total_tokens']:,}")
        print(f"Total Requests: {report['summary']['total_requests']:,}")
        
        # Per-provider breakdown
        print("\n📊 Per-Provider Breakdown:")
        for provider, metrics in report['detailed_metrics'].items():
            if metrics['total_requests'] > 0:
                print(f"\n  {provider}:")
                print(f"    Cost: ${metrics['estimated_cost_usd']:.4f}")
                print(f"    Tokens: {metrics['tokens_used']:,}")
                print(f"    Requests: {metrics['total_requests']}")
                print(f"    Success Rate: {metrics['success_count']/metrics['total_requests']*100:.1f}%")
        
        # Optimization suggestions
        suggestions = self.monitor.get_cost_optimization_suggestions()
        print("\n💡 Optimization Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")


async def main():
    """
    Demo the monitoring integration
    """
    print("🎚️ AI Application with API Monitoring Demo")
    print("=" * 60)
    
    # Initialize app
    app = AIApplicationWithMonitoring()
    
    # Simulate some API calls
    print("\n📡 Making API calls with automatic failover...\n")
    
    for i in range(5):
        try:
            result = await app.call_ai_with_failover(
                prompt=f"Generate music production tip #{i+1}",
                max_tokens=200
            )
            print(f"  Response: {result['response'][:50]}...")
            print()
        except Exception as e:
            print(f"  ❌ Error: {e}")
            print()
    
    # Get cost report
    app.get_cost_report()
    
    # Check for alerts
    print("\n" + "=" * 60)
    print("🚨 ALERTS")
    print("=" * 60)
    alerts = app.monitor.alert_on_failures()
    if alerts:
        for alert in alerts:
            print(f"\n{alert}")
    else:
        print("\n✅ No alerts - all systems operational!")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
