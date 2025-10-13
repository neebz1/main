#!/usr/bin/env python3
"""
DevOps Monitoring System for Virtual Agent Development
Monitors API keys, system health, and provides automated maintenance
"""

import os
import sys
import json
import time
import psutil
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()


@dataclass
class APIKeyStatus:
    """API key validation status"""
    provider: str
    key_present: bool
    key_valid: Optional[bool] = None
    error_message: Optional[str] = None
    last_checked: str = ""
    
    def to_dict(self):
        return asdict(self)


@dataclass
class SystemHealth:
    """System health metrics"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    timestamp: str
    status: str  # healthy, warning, critical
    
    def to_dict(self):
        return asdict(self)


@dataclass
class MonitoringReport:
    """Complete monitoring report"""
    timestamp: str
    api_keys: List[Dict]
    system_health: Dict
    issues_found: List[str]
    recommendations: List[str]
    
    def to_dict(self):
        return asdict(self)


class DevOpsMonitor:
    """
    Comprehensive DevOps monitoring system for virtual agent development
    """
    
    # Supported AI providers
    PROVIDERS = {
        'TOGETHER_API_KEY': {
            'name': 'Together AI (Kimi K2)',
            'test_endpoint': 'https://api.together.xyz/v1/models',
            'required': False
        },
        'OPENAI_API_KEY': {
            'name': 'OpenAI (GPT-4)',
            'test_endpoint': 'https://api.openai.com/v1/models',
            'required': False
        },
        'ANTHROPIC_API_KEY': {
            'name': 'Anthropic (Claude)',
            'test_endpoint': 'https://api.anthropic.com/v1/messages',
            'required': False
        },
        'OPENROUTER_API_KEY': {
            'name': 'OpenRouter',
            'test_endpoint': 'https://openrouter.ai/api/v1/models',
            'required': False
        },
        'GOOGLE_API_KEY': {
            'name': 'Google Gemini',
            'test_endpoint': None,  # Uses different auth method
            'required': False
        },
        'MOONSHOT_API_KEY': {
            'name': 'Moonshot AI',
            'test_endpoint': 'https://api.moonshot.cn/v1/models',
            'required': False
        }
    }
    
    def __init__(self, report_dir: Path = None):
        """Initialize monitoring system"""
        self.report_dir = report_dir or Path('./monitoring_reports')
        self.report_dir.mkdir(exist_ok=True)
        
    def check_api_key_status(self, env_var: str, config: Dict) -> APIKeyStatus:
        """Check if an API key is present and optionally validate it"""
        key_value = os.getenv(env_var)
        status = APIKeyStatus(
            provider=config['name'],
            key_present=bool(key_value),
            last_checked=datetime.now().isoformat()
        )
        
        if not key_value:
            status.error_message = "API key not found in environment"
            return status
        
        # Validate key if endpoint is available
        if config.get('test_endpoint'):
            try:
                status.key_valid, status.error_message = self._validate_api_key(
                    env_var, key_value, config['test_endpoint']
                )
            except Exception as e:
                status.key_valid = False
                status.error_message = f"Validation error: {str(e)}"
        else:
            status.key_valid = None
            status.error_message = "Validation not supported for this provider"
        
        return status
    
    def _validate_api_key(self, env_var: str, key: str, endpoint: str) -> tuple:
        """Validate API key by making a test request"""
        try:
            headers = {}
            
            # Set up authentication based on provider
            if 'OPENAI' in env_var:
                headers['Authorization'] = f'Bearer {key}'
            elif 'ANTHROPIC' in env_var:
                headers['x-api-key'] = key
                headers['anthropic-version'] = '2023-06-01'
            elif 'TOGETHER' in env_var:
                headers['Authorization'] = f'Bearer {key}'
            elif 'OPENROUTER' in env_var:
                headers['Authorization'] = f'Bearer {key}'
            elif 'MOONSHOT' in env_var:
                headers['Authorization'] = f'Bearer {key}'
            
            # Make test request with timeout
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True, "API key is valid"
            elif response.status_code == 401:
                return False, "API key is invalid (401 Unauthorized)"
            elif response.status_code == 403:
                return False, "API key is invalid (403 Forbidden)"
            else:
                return None, f"Unexpected response: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return None, "Request timeout - API might be slow"
        except requests.exceptions.ConnectionError:
            return None, "Connection error - check network"
        except Exception as e:
            return None, f"Validation error: {str(e)}"
    
    def check_system_health(self) -> SystemHealth:
        """Check system resource usage"""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        # Determine status
        status = "healthy"
        if cpu > 80 or memory > 80 or disk > 80:
            status = "warning"
        if cpu > 90 or memory > 90 or disk > 90:
            status = "critical"
        
        return SystemHealth(
            cpu_percent=cpu,
            memory_percent=memory,
            disk_percent=disk,
            timestamp=datetime.now().isoformat(),
            status=status
        )
    
    def perform_health_check(self) -> MonitoringReport:
        """Perform complete health check"""
        print("🔍 DevOps Monitoring System - Health Check")
        print("=" * 60)
        
        # Check API keys
        print("\n📋 Checking API Keys...")
        api_statuses = []
        for env_var, config in self.PROVIDERS.items():
            status = self.check_api_key_status(env_var, config)
            api_statuses.append(status.to_dict())
            
            # Print status
            icon = "✅" if status.key_present else "❌"
            print(f"{icon} {config['name']}: {'Present' if status.key_present else 'Missing'}")
            if status.key_valid is not None:
                valid_icon = "✅" if status.key_valid else "❌"
                print(f"   {valid_icon} Validation: {status.error_message or 'Valid'}")
        
        # Check system health
        print("\n💻 Checking System Health...")
        health = self.check_system_health()
        status_icon = "✅" if health.status == "healthy" else "⚠️" if health.status == "warning" else "🚨"
        print(f"{status_icon} Status: {health.status.upper()}")
        print(f"   CPU: {health.cpu_percent}%")
        print(f"   Memory: {health.memory_percent}%")
        print(f"   Disk: {health.disk_percent}%")
        
        # Generate issues and recommendations
        issues = self._identify_issues(api_statuses, health)
        recommendations = self._generate_recommendations(issues, api_statuses, health)
        
        if issues:
            print("\n⚠️ Issues Found:")
            for issue in issues:
                print(f"   • {issue}")
        
        if recommendations:
            print("\n💡 Recommendations:")
            for rec in recommendations:
                print(f"   • {rec}")
        
        # Create report
        report = MonitoringReport(
            timestamp=datetime.now().isoformat(),
            api_keys=api_statuses,
            system_health=health.to_dict(),
            issues_found=issues,
            recommendations=recommendations
        )
        
        # Save report
        self._save_report(report)
        
        print(f"\n📊 Report saved to: {self.report_dir}")
        print("=" * 60)
        
        return report
    
    def _identify_issues(self, api_statuses: List[Dict], health: SystemHealth) -> List[str]:
        """Identify system issues"""
        issues = []
        
        # Check if any API key is present
        has_any_key = any(status['key_present'] for status in api_statuses)
        if not has_any_key:
            issues.append("No API keys configured - AI features will not work")
        
        # Check for invalid keys
        for status in api_statuses:
            if status['key_present'] and status['key_valid'] is False:
                issues.append(f"{status['provider']} API key is invalid")
        
        # Check system resources
        if health.status == "warning":
            issues.append("System resources are running high")
        elif health.status == "critical":
            issues.append("CRITICAL: System resources are critically high")
        
        if health.cpu_percent > 80:
            issues.append(f"High CPU usage: {health.cpu_percent}%")
        if health.memory_percent > 80:
            issues.append(f"High memory usage: {health.memory_percent}%")
        if health.disk_percent > 80:
            issues.append(f"High disk usage: {health.disk_percent}%")
        
        return issues
    
    def _generate_recommendations(self, issues: List[str], api_statuses: List[Dict], 
                                  health: SystemHealth) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []
        
        # API key recommendations
        missing_keys = [s['provider'] for s in api_statuses if not s['key_present']]
        if missing_keys:
            recommendations.append(
                f"Configure at least one API key: {', '.join(missing_keys[:3])}"
            )
        
        invalid_keys = [s['provider'] for s in api_statuses 
                       if s['key_present'] and s['key_valid'] is False]
        if invalid_keys:
            recommendations.append(
                f"Check and update invalid API keys: {', '.join(invalid_keys)}"
            )
        
        # System health recommendations
        if health.cpu_percent > 80:
            recommendations.append("High CPU usage detected - consider closing unnecessary processes")
        if health.memory_percent > 80:
            recommendations.append("High memory usage detected - restart applications or upgrade RAM")
        if health.disk_percent > 80:
            recommendations.append("Low disk space - clean up unnecessary files")
        
        # General recommendations
        if not recommendations:
            recommendations.append("System is healthy - continue monitoring")
        
        return recommendations
    
    def _save_report(self, report: MonitoringReport):
        """Save monitoring report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.report_dir / f"monitoring_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        
        # Also save as latest
        latest_file = self.report_dir / "latest_report.json"
        with open(latest_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
    
    def generate_status_badge(self) -> str:
        """Generate a status badge for README"""
        latest_report = self.report_dir / "latest_report.json"
        
        if not latest_report.exists():
            return "![Status](https://img.shields.io/badge/status-unknown-lightgrey)"
        
        with open(latest_report) as f:
            report = json.load(f)
        
        status = report['system_health']['status']
        
        if status == "healthy":
            return "![Status](https://img.shields.io/badge/status-healthy-brightgreen)"
        elif status == "warning":
            return "![Status](https://img.shields.io/badge/status-warning-yellow)"
        else:
            return "![Status](https://img.shields.io/badge/status-critical-red)"
    
    def get_provider_fallback_order(self) -> List[str]:
        """Get the order of API providers based on availability"""
        print("\n🔄 Determining Provider Fallback Order...")
        
        available = []
        for env_var, config in self.PROVIDERS.items():
            status = self.check_api_key_status(env_var, config)
            if status.key_present and status.key_valid != False:
                available.append(config['name'])
        
        if available:
            print(f"✅ Available providers: {', '.join(available)}")
        else:
            print("❌ No API providers available")
        
        return available


def main():
    """Main entry point for monitoring system"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='DevOps Monitoring System for Virtual Agent'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Perform health check'
    )
    parser.add_argument(
        '--report-dir',
        default='./monitoring_reports',
        help='Directory for monitoring reports'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = DevOpsMonitor(report_dir=Path(args.report_dir))
    
    # Perform health check
    if args.check or len(sys.argv) == 1:
        report = monitor.perform_health_check()
        
        if args.json:
            print("\n" + json.dumps(report.to_dict(), indent=2))
    
    # Get fallback order
    monitor.get_provider_fallback_order()


if __name__ == "__main__":
    main()
