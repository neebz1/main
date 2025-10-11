#!/usr/bin/env python3
"""
Example: Integrating DevOps Monitoring with Existing Applications

This file demonstrates how to integrate the monitoring system
with your existing AI applications like logic_copilot_lite.py,
cloud_ai_builder.py, etc.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from devops_monitor import DevOpsMonitor
from multi_provider_ai import MultiProviderAI

# Load environment
load_dotenv()


def example_1_basic_health_check():
    """Example 1: Basic health check before app startup"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Health Check")
    print("=" * 70)
    
    # Create monitor
    monitor = DevOpsMonitor()
    
    # Perform health check
    report = monitor.perform_health_check()
    
    # Check if we can proceed
    if report.system_health['status'] == 'critical':
        print("\n🚨 CRITICAL: System health is critical!")
        print("Cannot start application safely.")
        return False
    
    if not any(api['key_present'] for api in report.api_keys):
        print("\n⚠️  WARNING: No API keys configured!")
        print("Application will start but AI features will not work.")
    
    print("\n✅ Health check passed - proceeding with startup")
    return True


def example_2_provider_fallback():
    """Example 2: Using multi-provider with automatic fallback"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Multi-Provider with Fallback")
    print("=" * 70)
    
    # Initialize multi-provider AI
    ai = MultiProviderAI()
    
    # Check what provider we're using
    status = ai.get_status()
    print(f"\n📊 Status:")
    print(f"   Current Provider: {status['provider'] or 'None'}")
    print(f"   Available Providers: {', '.join(status['available_providers']) or 'None'}")
    
    # Try to chat (will automatically use best available provider)
    if ai.client:
        response, error = ai.chat(
            "Explain in one sentence what you do.",
            system_prompt="You are a helpful AI assistant."
        )
        
        if response:
            print(f"\n💬 AI Response: {response}")
        else:
            print(f"\n❌ Error: {error}")
    else:
        print("\n⚠️  No provider available - configure API keys")


def example_3_continuous_monitoring():
    """Example 3: Continuous monitoring during app runtime"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Continuous Monitoring")
    print("=" * 70)
    
    monitor = DevOpsMonitor()
    
    print("\n📊 Starting continuous monitoring...")
    print("(In production, this would run in a background thread)")
    
    # Simulate checking every hour
    for i in range(3):
        print(f"\n--- Check #{i+1} ---")
        
        # Quick system health check
        health = monitor.check_system_health()
        print(f"System Status: {health.status}")
        print(f"CPU: {health.cpu_percent}% | Memory: {health.memory_percent}% | Disk: {health.disk_percent}%")
        
        # Check if we need to alert
        if health.status == 'critical':
            print("🚨 ALERT: System resources critically high!")
            print("Action: Send notification, log issue, reduce load")
        elif health.status == 'warning':
            print("⚠️  WARNING: System resources elevated")
            print("Action: Monitor closely, prepare to scale")
        else:
            print("✅ All systems normal")
    
    print("\n✅ Monitoring demonstration complete")


def example_4_integration_template():
    """Example 4: Template for integrating with existing apps"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Integration Template")
    print("=" * 70)
    
    print("""
    # Template for integrating monitoring into existing applications
    # Add this to the top of logic_copilot_lite.py, cloud_ai_builder.py, etc.
    
    ```python
    from devops_monitor import DevOpsMonitor
    from multi_provider_ai import MultiProviderAI
    
    # At startup, before Gradio initialization
    print("🔍 Running pre-flight health check...")
    monitor = DevOpsMonitor()
    report = monitor.perform_health_check()
    
    # Initialize AI with automatic fallback
    ai = MultiProviderAI()
    
    if not ai.client:
        print("⚠️  WARNING: No AI provider available")
        print("Please configure at least one API key in .env file")
    else:
        print(f"✅ Using {ai.provider}")
    
    # Your existing Gradio code here...
    # Use ai.chat() instead of direct client calls for automatic fallback
    ```
    """)


def example_5_scheduled_monitoring():
    """Example 5: Setting up scheduled monitoring"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Scheduled Monitoring Setup")
    print("=" * 70)
    
    print("""
    # Option 1: Using cron (Linux/Mac)
    
    # Edit crontab
    $ crontab -e
    
    # Add hourly monitoring
    0 * * * * cd /path/to/repo && python devops_monitor.py --check >> monitoring.log 2>&1
    
    # Add daily report email (requires mail setup)
    0 9 * * * cd /path/to/repo && python devops_monitor.py --check --json | mail -s "Daily Monitoring Report" you@email.com
    
    # Option 2: Using GitHub Actions (already configured!)
    
    # The monitoring.yml workflow runs hourly automatically
    # It will create GitHub issues if problems are detected
    # Check .github/workflows/monitoring.yml
    
    # Option 3: Using Python scheduler in your app
    
    ```python
    import schedule
    import time
    from devops_monitor import DevOpsMonitor
    
    def scheduled_check():
        monitor = DevOpsMonitor()
        report = monitor.perform_health_check()
        
        # Send alerts if needed
        if report.issues_found:
            send_alert(report)
    
    # Schedule every hour
    schedule.every().hour.do(scheduled_check)
    
    # Run scheduler in background thread
    import threading
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    threading.Thread(target=run_scheduler, daemon=True).start()
    ```
    """)


def example_6_error_recovery():
    """Example 6: Automatic error recovery"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Automatic Error Recovery")
    print("=" * 70)
    
    print("""
    # Implement error recovery in your chat functions
    
    ```python
    from multi_provider_ai import MultiProviderAI
    
    def chat_with_ai(message, history):
        '''Chat with AI using automatic provider fallback'''
        
        # Initialize multi-provider AI
        ai = MultiProviderAI()
        
        if not ai.client:
            return "⚠️ No AI providers available. Please configure API keys."
        
        try:
            # Try chat with automatic fallback
            response, error = ai.chat(
                message,
                system_prompt="You are a helpful assistant.",
                max_tokens=1024
            )
            
            if response:
                return response
            else:
                return f"Error: {error}"
                
        except Exception as e:
            # Log error for monitoring
            print(f"❌ Chat error: {e}")
            
            # Try to reinitialize with different provider
            ai = MultiProviderAI()
            
            if ai.client:
                response, error = ai.chat(message)
                if response:
                    return f"⚠️ Recovered using fallback provider\\n\\n{response}"
            
            return f"❌ All providers failed: {str(e)}"
    ```
    """)


def run_all_examples():
    """Run all examples"""
    print("🤖 DevOps Monitoring Integration Examples")
    print("=" * 70)
    print()
    print("These examples show how to integrate monitoring")
    print("with your existing AI applications.")
    print()
    
    # Run examples
    example_1_basic_health_check()
    example_2_provider_fallback()
    example_3_continuous_monitoring()
    example_4_integration_template()
    example_5_scheduled_monitoring()
    example_6_error_recovery()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70)
    print()
    print("📚 Next Steps:")
    print("   1. Review the examples above")
    print("   2. Choose the integration approach that fits your needs")
    print("   3. Add monitoring to your existing applications")
    print("   4. Set up GitHub Actions workflows (already done!)")
    print("   5. Configure scheduled monitoring")
    print()
    print("📖 Documentation:")
    print("   • MONITORING_README.md - Quick start guide")
    print("   • MONITORING_DOCS.md - Complete documentation")
    print("   • test_devops_monitor.py - Example tests")
    print()


if __name__ == "__main__":
    run_all_examples()
