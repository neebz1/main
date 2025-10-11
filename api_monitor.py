#!/usr/bin/env python3
"""
API Integration Monitor for Multi-Provider Setup
Monitors OpenRouter, Google Gemini, Together AI, Anthropic, OpenAI, and Moonshot AI

Features:
- Real-time API health monitoring
- Response time tracking
- Error rate monitoring
- Usage and cost tracking
- Automatic failover
- Cost optimization suggestions
"""

import os
import time
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import httpx
from dotenv import load_dotenv

load_dotenv()


class APIProvider(Enum):
    """Supported API providers"""
    OPENROUTER = "openrouter"
    GOOGLE_GEMINI = "google_gemini"
    TOGETHER_AI = "together_ai"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    MOONSHOT_AI = "moonshot_ai"


class APIStatus(Enum):
    """API health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class APIMetrics:
    """Metrics for an API provider"""
    provider: str
    status: str
    response_time_ms: Optional[float] = None
    error_count: int = 0
    success_count: int = 0
    total_requests: int = 0
    last_check: Optional[str] = None
    last_error: Optional[str] = None
    estimated_cost_usd: float = 0.0
    tokens_used: int = 0
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.error_count / self.total_requests) * 100
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.success_count / self.total_requests) * 100


@dataclass
class ProviderConfig:
    """Configuration for an API provider"""
    name: str
    api_key_env: str
    base_url: str
    health_check_endpoint: Optional[str] = None
    cost_per_1k_tokens: float = 0.0  # Average cost
    timeout: int = 30


class APIMonitor:
    """
    Comprehensive API monitoring system
    """
    
    # Provider configurations
    PROVIDER_CONFIGS = {
        APIProvider.OPENROUTER: ProviderConfig(
            name="OpenRouter",
            api_key_env="OPENROUTER_API_KEY",
            base_url="https://openrouter.ai/api/v1",
            health_check_endpoint="/models",
            cost_per_1k_tokens=0.002,  # Varies by model
            timeout=30
        ),
        APIProvider.GOOGLE_GEMINI: ProviderConfig(
            name="Google Gemini",
            api_key_env="GOOGLE_API_KEY",
            base_url="https://generativelanguage.googleapis.com/v1beta",
            health_check_endpoint="/models",
            cost_per_1k_tokens=0.001,  # Gemini Flash
            timeout=30
        ),
        APIProvider.TOGETHER_AI: ProviderConfig(
            name="Together AI (Kimi K2)",
            api_key_env="TOGETHER_API_KEY",
            base_url="https://api.together.xyz/v1",
            health_check_endpoint="/models",
            cost_per_1k_tokens=0.0005,  # Very affordable
            timeout=30
        ),
        APIProvider.ANTHROPIC: ProviderConfig(
            name="Anthropic (Claude)",
            api_key_env="ANTHROPIC_API_KEY",
            base_url="https://api.anthropic.com/v1",
            health_check_endpoint="/messages",
            cost_per_1k_tokens=0.008,  # Claude Sonnet
            timeout=30
        ),
        APIProvider.OPENAI: ProviderConfig(
            name="OpenAI (GPT-4)",
            api_key_env="OPENAI_API_KEY",
            base_url="https://api.openai.com/v1",
            health_check_endpoint="/models",
            cost_per_1k_tokens=0.01,  # GPT-4
            timeout=30
        ),
        APIProvider.MOONSHOT_AI: ProviderConfig(
            name="Moonshot AI",
            api_key_env="MOONSHOT_API_KEY",
            base_url="https://api.moonshot.cn/v1",  # Hypothetical
            health_check_endpoint="/models",
            cost_per_1k_tokens=0.003,
            timeout=30
        ),
    }
    
    def __init__(self, metrics_file: str = "api_metrics.json"):
        """Initialize the API monitor"""
        self.metrics_file = Path(metrics_file)
        self.metrics: Dict[str, APIMetrics] = {}
        self.load_metrics()
        
        # Initialize metrics for all providers
        for provider in APIProvider:
            if provider.value not in self.metrics:
                self.metrics[provider.value] = APIMetrics(
                    provider=provider.value,
                    status=APIStatus.UNKNOWN.value
                )
    
    def load_metrics(self):
        """Load metrics from disk"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    self.metrics = {
                        k: APIMetrics(**v) for k, v in data.items()
                    }
            except Exception as e:
                print(f"⚠️  Error loading metrics: {e}")
    
    def save_metrics(self):
        """Save metrics to disk"""
        try:
            with open(self.metrics_file, 'w') as f:
                data = {k: asdict(v) for k, v in self.metrics.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving metrics: {e}")
    
    async def check_provider_health(self, provider: APIProvider) -> APIMetrics:
        """
        Check health of a specific provider
        """
        config = self.PROVIDER_CONFIGS[provider]
        metrics = self.metrics[provider.value]
        
        # Check if API key is configured
        api_key = os.getenv(config.api_key_env)
        if not api_key:
            metrics.status = APIStatus.UNKNOWN.value
            metrics.last_check = datetime.now().isoformat()
            metrics.last_error = "API key not configured"
            return metrics
        
        # Perform health check
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=config.timeout) as client:
                # Build headers
                headers = self._build_headers(provider, api_key)
                
                # Make health check request
                url = f"{config.base_url}{config.health_check_endpoint}"
                
                response = await client.get(url, headers=headers)
                
                response_time = (time.time() - start_time) * 1000  # ms
                
                if response.status_code == 200:
                    metrics.status = APIStatus.HEALTHY.value
                    metrics.response_time_ms = response_time
                    metrics.success_count += 1
                    metrics.last_error = None
                elif response.status_code == 429:
                    metrics.status = APIStatus.DEGRADED.value
                    metrics.response_time_ms = response_time
                    metrics.error_count += 1
                    metrics.last_error = "Rate limit exceeded"
                else:
                    metrics.status = APIStatus.DEGRADED.value
                    metrics.response_time_ms = response_time
                    metrics.error_count += 1
                    metrics.last_error = f"HTTP {response.status_code}"
                
                metrics.total_requests += 1
                metrics.last_check = datetime.now().isoformat()
                
        except asyncio.TimeoutError:
            metrics.status = APIStatus.FAILED.value
            metrics.error_count += 1
            metrics.total_requests += 1
            metrics.last_check = datetime.now().isoformat()
            metrics.last_error = "Connection timeout"
        except Exception as e:
            metrics.status = APIStatus.FAILED.value
            metrics.error_count += 1
            metrics.total_requests += 1
            metrics.last_check = datetime.now().isoformat()
            metrics.last_error = str(e)
        
        return metrics
    
    def _build_headers(self, provider: APIProvider, api_key: str) -> Dict[str, str]:
        """Build request headers for provider"""
        if provider == APIProvider.ANTHROPIC:
            return {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
        elif provider == APIProvider.GOOGLE_GEMINI:
            # Gemini uses API key in URL param
            return {}
        else:
            return {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
    
    async def check_all_providers(self) -> Dict[str, APIMetrics]:
        """Check health of all configured providers"""
        tasks = []
        for provider in APIProvider:
            tasks.append(self.check_provider_health(provider))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update metrics
        for provider, result in zip(APIProvider, results):
            if not isinstance(result, Exception):
                self.metrics[provider.value] = result
        
        self.save_metrics()
        return self.metrics
    
    def get_healthy_providers(self) -> List[str]:
        """Get list of healthy providers"""
        return [
            metrics.provider 
            for metrics in self.metrics.values() 
            if metrics.status == APIStatus.HEALTHY.value
        ]
    
    def get_failover_provider(self, primary_provider: str) -> Optional[str]:
        """
        Get a failover provider when primary fails
        Priority: Together AI -> Anthropic -> OpenAI -> Google Gemini -> OpenRouter
        """
        healthy = self.get_healthy_providers()
        
        if not healthy:
            return None
        
        # Define priority order
        priority = [
            APIProvider.TOGETHER_AI.value,
            APIProvider.ANTHROPIC.value,
            APIProvider.OPENAI.value,
            APIProvider.GOOGLE_GEMINI.value,
            APIProvider.OPENROUTER.value,
        ]
        
        # Filter out the primary provider
        available = [p for p in priority if p in healthy and p != primary_provider]
        
        return available[0] if available else None
    
    def track_usage(self, provider: str, tokens: int):
        """Track API usage and cost"""
        if provider not in self.metrics:
            return
        
        metrics = self.metrics[provider]
        metrics.tokens_used += tokens
        
        # Calculate cost
        config = next(
            (c for p, c in self.PROVIDER_CONFIGS.items() if p.value == provider),
            None
        )
        if config:
            metrics.estimated_cost_usd += (tokens / 1000) * config.cost_per_1k_tokens
        
        self.save_metrics()
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        healthy = []
        degraded = []
        failed = []
        unknown = []
        
        total_cost = 0.0
        total_tokens = 0
        total_requests = 0
        
        for metrics in self.metrics.values():
            total_cost += metrics.estimated_cost_usd
            total_tokens += metrics.tokens_used
            total_requests += metrics.total_requests
            
            if metrics.status == APIStatus.HEALTHY.value:
                healthy.append(metrics.provider)
            elif metrics.status == APIStatus.DEGRADED.value:
                degraded.append(metrics.provider)
            elif metrics.status == APIStatus.FAILED.value:
                failed.append(metrics.provider)
            else:
                unknown.append(metrics.provider)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "healthy_providers": len(healthy),
                "degraded_providers": len(degraded),
                "failed_providers": len(failed),
                "unknown_providers": len(unknown),
                "total_cost_usd": round(total_cost, 4),
                "total_tokens": total_tokens,
                "total_requests": total_requests,
            },
            "providers": {
                "healthy": healthy,
                "degraded": degraded,
                "failed": failed,
                "unknown": unknown,
            },
            "detailed_metrics": {
                provider: asdict(metrics)
                for provider, metrics in self.metrics.items()
            }
        }
    
    def get_cost_optimization_suggestions(self) -> List[str]:
        """Generate cost optimization suggestions"""
        suggestions = []
        
        # Check if expensive providers are being used
        expensive_providers = [
            APIProvider.OPENAI.value,
            APIProvider.ANTHROPIC.value,
        ]
        
        affordable_providers = [
            APIProvider.TOGETHER_AI.value,
        ]
        
        for provider in expensive_providers:
            metrics = self.metrics.get(provider)
            if metrics and metrics.total_requests > 0:
                if metrics.estimated_cost_usd > 1.0:  # More than $1
                    suggestions.append(
                        f"💡 {self.PROVIDER_CONFIGS[APIProvider(provider)].name} "
                        f"has cost ${metrics.estimated_cost_usd:.2f}. "
                        f"Consider switching to Together AI (Kimi K2) for 80% cost savings."
                    )
        
        # Check response times
        for provider, metrics in self.metrics.items():
            if metrics.response_time_ms and metrics.response_time_ms > 5000:  # 5s
                suggestions.append(
                    f"⚡ {self.PROVIDER_CONFIGS[APIProvider(provider)].name} "
                    f"has slow response time ({metrics.response_time_ms:.0f}ms). "
                    f"Consider using a faster provider for better UX."
                )
        
        # Check error rates
        for provider, metrics in self.metrics.items():
            if metrics.error_rate > 10:  # More than 10% errors
                suggestions.append(
                    f"⚠️  {self.PROVIDER_CONFIGS[APIProvider(provider)].name} "
                    f"has high error rate ({metrics.error_rate:.1f}%). "
                    f"Consider implementing retry logic or switching providers."
                )
        
        if not suggestions:
            suggestions.append("✅ All providers are operating optimally!")
        
        return suggestions
    
    def alert_on_failures(self) -> List[str]:
        """Generate alerts for failed or degraded APIs"""
        alerts = []
        
        for provider, metrics in self.metrics.items():
            config = self.PROVIDER_CONFIGS[APIProvider(provider)]
            
            if metrics.status == APIStatus.FAILED.value:
                alerts.append(
                    f"🚨 CRITICAL: {config.name} API is DOWN! "
                    f"Last error: {metrics.last_error}"
                )
            elif metrics.status == APIStatus.DEGRADED.value:
                alerts.append(
                    f"⚠️  WARNING: {config.name} API is DEGRADED. "
                    f"Error rate: {metrics.error_rate:.1f}%. "
                    f"Last error: {metrics.last_error}"
                )
        
        return alerts


async def main():
    """Main monitoring loop"""
    print("🔍 API Integration Monitor Starting...")
    print("=" * 60)
    
    monitor = APIMonitor()
    
    # Initial check
    print("\n📊 Checking all API providers...")
    await monitor.check_all_providers()
    
    # Generate report
    report = monitor.get_status_report()
    
    print("\n" + "=" * 60)
    print("📈 STATUS REPORT")
    print("=" * 60)
    print(f"\n✅ Healthy: {report['summary']['healthy_providers']}")
    print(f"⚠️  Degraded: {report['summary']['degraded_providers']}")
    print(f"❌ Failed: {report['summary']['failed_providers']}")
    print(f"❓ Unknown: {report['summary']['unknown_providers']}")
    print(f"\n💰 Total Cost: ${report['summary']['total_cost_usd']}")
    print(f"🎯 Total Tokens: {report['summary']['total_tokens']:,}")
    print(f"📊 Total Requests: {report['summary']['total_requests']:,}")
    
    # Provider details
    print("\n" + "=" * 60)
    print("🔧 PROVIDER DETAILS")
    print("=" * 60)
    
    for provider, metrics in monitor.metrics.items():
        config = monitor.PROVIDER_CONFIGS[APIProvider(provider)]
        status_icon = {
            APIStatus.HEALTHY.value: "✅",
            APIStatus.DEGRADED.value: "⚠️ ",
            APIStatus.FAILED.value: "❌",
            APIStatus.UNKNOWN.value: "❓"
        }.get(metrics.status, "❓")
        
        print(f"\n{status_icon} {config.name}")
        print(f"   Status: {metrics.status}")
        if metrics.response_time_ms:
            print(f"   Response Time: {metrics.response_time_ms:.0f}ms")
        if metrics.total_requests > 0:
            print(f"   Success Rate: {metrics.success_rate:.1f}%")
            print(f"   Error Rate: {metrics.error_rate:.1f}%")
            print(f"   Cost: ${metrics.estimated_cost_usd:.4f}")
        if metrics.last_error:
            print(f"   Last Error: {metrics.last_error}")
        print(f"   Last Check: {metrics.last_check or 'Never'}")
    
    # Alerts
    alerts = monitor.alert_on_failures()
    if alerts:
        print("\n" + "=" * 60)
        print("🚨 ALERTS")
        print("=" * 60)
        for alert in alerts:
            print(f"\n{alert}")
    
    # Cost optimization
    suggestions = monitor.get_cost_optimization_suggestions()
    print("\n" + "=" * 60)
    print("💡 COST OPTIMIZATION SUGGESTIONS")
    print("=" * 60)
    for suggestion in suggestions:
        print(f"\n{suggestion}")
    
    # Failover test
    print("\n" + "=" * 60)
    print("🔄 FAILOVER CONFIGURATION")
    print("=" * 60)
    for provider in APIProvider:
        failover = monitor.get_failover_provider(provider.value)
        if failover:
            print(f"\n{provider.value} → {failover}")
    
    print("\n" + "=" * 60)
    print("✅ Monitoring complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
