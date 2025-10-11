#!/usr/bin/env python3
"""
Test Suite for API Integration Monitor
Demonstrates all features and validates functionality
"""

import asyncio
import json
from pathlib import Path
from api_monitor import APIMonitor, APIProvider, APIStatus


async def test_health_checks():
    """Test 1: Health check functionality"""
    print("=" * 60)
    print("TEST 1: Health Check Functionality")
    print("=" * 60)
    
    monitor = APIMonitor(metrics_file="test_api_metrics.json")
    
    print("\n🔍 Checking all providers...")
    await monitor.check_all_providers()
    
    print("\n✅ Results:")
    for provider, metrics in monitor.metrics.items():
        print(f"  {provider}: {metrics.status}")
        if metrics.last_error:
            print(f"    Error: {metrics.last_error}")
    
    return monitor


async def test_failover_logic(monitor):
    """Test 2: Failover logic"""
    print("\n" + "=" * 60)
    print("TEST 2: Failover Logic")
    print("=" * 60)
    
    print("\n🔄 Testing failover for each provider...")
    
    for provider in APIProvider:
        failover = monitor.get_failover_provider(provider.value)
        if failover:
            print(f"  {provider.value} → {failover}")
        else:
            print(f"  {provider.value} → No failover available")


def test_usage_tracking(monitor):
    """Test 3: Usage tracking"""
    print("\n" + "=" * 60)
    print("TEST 3: Usage Tracking")
    print("=" * 60)
    
    print("\n📊 Simulating usage...")
    
    # Simulate usage for different providers
    usage_scenarios = [
        (APIProvider.TOGETHER_AI.value, 10000, "Kimi K2 - affordable"),
        (APIProvider.OPENAI.value, 5000, "GPT-4 - expensive"),
        (APIProvider.ANTHROPIC.value, 3000, "Claude - quality"),
        (APIProvider.GOOGLE_GEMINI.value, 7500, "Gemini - fast"),
    ]
    
    for provider, tokens, description in usage_scenarios:
        monitor.track_usage(provider, tokens)
        print(f"  ✓ {description}: {tokens:,} tokens")
    
    # Show updated metrics
    print("\n💰 Cost Summary:")
    for provider, metrics in monitor.metrics.items():
        if metrics.tokens_used > 0:
            print(f"  {provider}: ${metrics.estimated_cost_usd:.4f} ({metrics.tokens_used:,} tokens)")


def test_status_report(monitor):
    """Test 4: Status report generation"""
    print("\n" + "=" * 60)
    print("TEST 4: Status Report")
    print("=" * 60)
    
    report = monitor.get_status_report()
    
    print("\n📈 Summary:")
    print(f"  Healthy: {report['summary']['healthy_providers']}")
    print(f"  Degraded: {report['summary']['degraded_providers']}")
    print(f"  Failed: {report['summary']['failed_providers']}")
    print(f"  Unknown: {report['summary']['unknown_providers']}")
    print(f"  Total Cost: ${report['summary']['total_cost_usd']:.4f}")
    print(f"  Total Tokens: {report['summary']['total_tokens']:,}")
    
    print("\n🏥 Provider Status:")
    for category in ['healthy', 'degraded', 'failed', 'unknown']:
        providers = report['providers'][category]
        if providers:
            print(f"  {category.upper()}: {', '.join(providers)}")


def test_optimization_suggestions(monitor):
    """Test 5: Cost optimization suggestions"""
    print("\n" + "=" * 60)
    print("TEST 5: Cost Optimization")
    print("=" * 60)
    
    suggestions = monitor.get_cost_optimization_suggestions()
    
    print("\n💡 Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")


def test_alerts(monitor):
    """Test 6: Alert generation"""
    print("\n" + "=" * 60)
    print("TEST 6: Alerts")
    print("=" * 60)
    
    alerts = monitor.alert_on_failures()
    
    if alerts:
        print("\n🚨 Active Alerts:")
        for alert in alerts:
            print(f"  • {alert}")
    else:
        print("\n✅ No active alerts")


def test_metrics_persistence(monitor):
    """Test 7: Metrics persistence"""
    print("\n" + "=" * 60)
    print("TEST 7: Metrics Persistence")
    print("=" * 60)
    
    # Save current metrics
    monitor.save_metrics()
    print("\n💾 Metrics saved to: test_api_metrics.json")
    
    # Load metrics into new monitor
    new_monitor = APIMonitor(metrics_file="test_api_metrics.json")
    print("✅ Metrics loaded successfully")
    
    # Verify data matches
    print("\n🔍 Verification:")
    for provider in monitor.metrics:
        original = monitor.metrics[provider]
        loaded = new_monitor.metrics[provider]
        match = original.tokens_used == loaded.tokens_used
        status = "✓" if match else "✗"
        print(f"  {status} {provider}: {loaded.tokens_used:,} tokens")


def test_detailed_metrics(monitor):
    """Test 8: Detailed metrics display"""
    print("\n" + "=" * 60)
    print("TEST 8: Detailed Metrics")
    print("=" * 60)
    
    print("\n📊 Per-Provider Details:")
    for provider, metrics in monitor.metrics.items():
        if metrics.tokens_used > 0 or metrics.total_requests > 0:
            print(f"\n  {provider.upper()}")
            print(f"    Status: {metrics.status}")
            print(f"    Tokens: {metrics.tokens_used:,}")
            print(f"    Cost: ${metrics.estimated_cost_usd:.4f}")
            print(f"    Requests: {metrics.total_requests}")
            if metrics.response_time_ms:
                print(f"    Response Time: {metrics.response_time_ms:.0f}ms")
            if metrics.total_requests > 0:
                print(f"    Success Rate: {metrics.success_rate:.1f}%")
                print(f"    Error Rate: {metrics.error_rate:.1f}%")


def test_cost_comparison():
    """Test 9: Cost comparison calculation"""
    print("\n" + "=" * 60)
    print("TEST 9: Cost Comparison")
    print("=" * 60)
    
    # Simulate 1 million tokens across different providers
    tokens = 1_000_000
    
    print(f"\n💰 Cost for {tokens:,} tokens:")
    
    costs = {
        "Together AI (Kimi K2)": tokens / 1000 * 0.0005,
        "Google Gemini": tokens / 1000 * 0.001,
        "OpenRouter": tokens / 1000 * 0.002,
        "Moonshot AI": tokens / 1000 * 0.003,
        "Anthropic (Claude)": tokens / 1000 * 0.008,
        "OpenAI (GPT-4)": tokens / 1000 * 0.01,
    }
    
    # Sort by cost
    sorted_costs = sorted(costs.items(), key=lambda x: x[1])
    
    for provider, cost in sorted_costs:
        print(f"  {provider:25s} ${cost:8.2f}")
    
    # Calculate savings
    cheapest = sorted_costs[0][1]
    most_expensive = sorted_costs[-1][1]
    savings = most_expensive - cheapest
    savings_pct = (savings / most_expensive) * 100
    
    print(f"\n💡 Savings using {sorted_costs[0][0]}:")
    print(f"  ${savings:.2f} ({savings_pct:.1f}% cheaper than {sorted_costs[-1][0]})")


async def main():
    """Run all tests"""
    print("\n" + "🔍 API INTEGRATION MONITOR - TEST SUITE" + "\n")
    
    try:
        # Run tests
        monitor = await test_health_checks()
        await test_failover_logic(monitor)
        test_usage_tracking(monitor)
        test_status_report(monitor)
        test_optimization_suggestions(monitor)
        test_alerts(monitor)
        test_metrics_persistence(monitor)
        test_detailed_metrics(monitor)
        test_cost_comparison()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        # Cleanup test file
        test_file = Path("test_api_metrics.json")
        if test_file.exists():
            test_file.unlink()
            print("\n🧹 Cleaned up test metrics file")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
