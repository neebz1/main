#!/usr/bin/env python3
"""
Virtual Agent Development Progress Monitor
Real-time monitoring and reporting of development metrics

Features:
- Code completion status tracking
- API integration health checks
- Test results and coverage analysis
- Performance metrics
- Security scan results
- Documentation completeness
- Deployment readiness assessment
- 30-minute automated reporting
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import threading


@dataclass
class CodeMetrics:
    """Code completion and quality metrics"""
    total_files: int = 0
    total_lines: int = 0
    python_files: int = 0
    javascript_files: int = 0
    markdown_files: int = 0
    completed_features: List[str] = None
    in_progress_features: List[str] = None
    pending_features: List[str] = None
    
    def __post_init__(self):
        if self.completed_features is None:
            self.completed_features = []
        if self.in_progress_features is None:
            self.in_progress_features = []
        if self.pending_features is None:
            self.pending_features = []


@dataclass
class APIHealthMetrics:
    """API integration health status"""
    total_endpoints: int = 0
    healthy_endpoints: int = 0
    failing_endpoints: int = 0
    response_times: Dict[str, float] = None
    last_check: str = ""
    status: str = "unknown"
    
    def __post_init__(self):
        if self.response_times is None:
            self.response_times = {}


@dataclass
class TestMetrics:
    """Test results and coverage"""
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    coverage_percent: float = 0.0
    last_run: str = ""
    test_status: str = "unknown"


@dataclass
class PerformanceMetrics:
    """Performance and resource metrics"""
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    avg_response_time_ms: float = 0.0
    requests_per_second: float = 0.0
    error_rate: float = 0.0


@dataclass
class SecurityMetrics:
    """Security scan results"""
    vulnerabilities_critical: int = 0
    vulnerabilities_high: int = 0
    vulnerabilities_medium: int = 0
    vulnerabilities_low: int = 0
    last_scan: str = ""
    scan_status: str = "not_scanned"


@dataclass
class DocumentationMetrics:
    """Documentation completeness"""
    total_modules: int = 0
    documented_modules: int = 0
    total_functions: int = 0
    documented_functions: int = 0
    readme_present: bool = False
    api_docs_present: bool = False
    completeness_percent: float = 0.0


@dataclass
class DeploymentReadiness:
    """Deployment readiness assessment"""
    ready: bool = False
    blockers: List[str] = None
    warnings: List[str] = None
    checklist: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.blockers is None:
            self.blockers = []
        if self.warnings is None:
            self.warnings = []
        if self.checklist is None:
            self.checklist = {}


class DevelopmentMonitor:
    """Main development monitoring system"""
    
    def __init__(self, project_dir: str = None):
        self.project_dir = Path(project_dir or os.getcwd())
        self.report_interval = 1800  # 30 minutes in seconds
        self.reports_dir = self.project_dir / "dev_reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.monitoring_active = False
        self.monitor_thread = None
        
    def scan_codebase(self) -> CodeMetrics:
        """Scan codebase for completion metrics"""
        metrics = CodeMetrics()
        
        # Count files by type
        py_files = list(self.project_dir.glob("**/*.py"))
        js_files = list(self.project_dir.glob("**/*.js"))
        md_files = list(self.project_dir.glob("**/*.md"))
        
        # Filter out venv and node_modules
        py_files = [f for f in py_files if 'venv' not in str(f) and 'node_modules' not in str(f)]
        js_files = [f for f in js_files if 'node_modules' not in str(f)]
        
        metrics.python_files = len(py_files)
        metrics.javascript_files = len(js_files)
        metrics.markdown_files = len(md_files)
        metrics.total_files = metrics.python_files + metrics.javascript_files + metrics.markdown_files
        
        # Count total lines of code
        total_lines = 0
        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    total_lines += len(f.readlines())
            except:
                pass
        
        for js_file in js_files:
            try:
                with open(js_file, 'r') as f:
                    total_lines += len(f.readlines())
            except:
                pass
        
        metrics.total_lines = total_lines
        
        # Detect completed, in-progress, and pending features
        metrics.completed_features = self._detect_completed_features()
        metrics.in_progress_features = self._detect_in_progress_features()
        metrics.pending_features = self._detect_pending_features()
        
        return metrics
    
    def _detect_completed_features(self) -> List[str]:
        """Detect completed features from files and docs"""
        features = []
        
        # Check for working Python modules
        main_modules = [
            "ai_mixing_engineer.py",
            "live_ai_assistant.py",
            "logic_copilot_lite.py",
            "cloud_ai_builder.py",
            "logic_ai_plugin.py"
        ]
        
        for module in main_modules:
            if (self.project_dir / module).exists():
                features.append(module.replace(".py", "").replace("_", " ").title())
        
        # Check API server
        if (self.project_dir / "CursorDocsIndex" / "api_server.py").exists():
            features.append("Docs Agent API Server")
        
        return features
    
    def _detect_in_progress_features(self) -> List[str]:
        """Detect features currently in development"""
        in_progress = []
        
        # Check for TODO comments
        py_files = list(self.project_dir.glob("*.py"))
        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    if 'TODO' in content or 'FIXME' in content:
                        feature_name = py_file.stem.replace("_", " ").title()
                        if feature_name not in in_progress:
                            in_progress.append(feature_name)
            except:
                pass
        
        return in_progress
    
    def _detect_pending_features(self) -> List[str]:
        """Detect pending features from issues or docs"""
        # This could be enhanced to read from GitHub issues
        return []
    
    def check_api_health(self) -> APIHealthMetrics:
        """Check health of API endpoints"""
        metrics = APIHealthMetrics()
        metrics.last_check = datetime.now().isoformat()
        
        # Check if API server exists
        api_file = self.project_dir / "CursorDocsIndex" / "api_server.py"
        if not api_file.exists():
            metrics.status = "not_deployed"
            return metrics
        
        # Define expected endpoints
        endpoints = [
            "/",
            "/health",
            "/search",
            "/lookup",
            "/stats",
            "/documents"
        ]
        
        metrics.total_endpoints = len(endpoints)
        
        # Try to check if server is running (basic check)
        try:
            result = subprocess.run(
                ["pgrep", "-f", "api_server"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                metrics.status = "running"
                metrics.healthy_endpoints = len(endpoints)
            else:
                metrics.status = "stopped"
        except:
            metrics.status = "unknown"
        
        return metrics
    
    def run_tests(self) -> TestMetrics:
        """Run tests and gather metrics"""
        metrics = TestMetrics()
        metrics.last_run = datetime.now().isoformat()
        
        # Check if pytest is available
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                metrics.test_status = "pytest_not_installed"
                return metrics
        except:
            metrics.test_status = "pytest_not_installed"
            return metrics
        
        # Look for test files
        test_files = list(self.project_dir.glob("**/test_*.py")) + \
                    list(self.project_dir.glob("**/*_test.py"))
        
        if not test_files:
            metrics.test_status = "no_tests_found"
            return metrics
        
        # Run pytest if tests exist
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", "-v", "--tb=short"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout + result.stderr
            
            # Parse pytest output
            if "passed" in output:
                metrics.test_status = "completed"
                # Simple parsing - could be enhanced
                for line in output.split('\n'):
                    if 'passed' in line or 'failed' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'passed' in part and i > 0:
                                try:
                                    metrics.passed_tests = int(parts[i-1])
                                except:
                                    pass
                            if 'failed' in part and i > 0:
                                try:
                                    metrics.failed_tests = int(parts[i-1])
                                except:
                                    pass
                
                metrics.total_tests = metrics.passed_tests + metrics.failed_tests
            else:
                metrics.test_status = "no_results"
                
        except subprocess.TimeoutExpired:
            metrics.test_status = "timeout"
        except Exception as e:
            metrics.test_status = f"error: {str(e)}"
        
        return metrics
    
    def gather_performance_metrics(self) -> PerformanceMetrics:
        """Gather performance metrics"""
        metrics = PerformanceMetrics()
        
        # Basic system metrics
        try:
            # Memory usage
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Look for our processes
            for line in result.stdout.split('\n'):
                if 'python' in line.lower() and any(x in line for x in ['ai_mixing', 'logic_copilot', 'api_server']):
                    parts = line.split()
                    if len(parts) > 5:
                        try:
                            # CPU is usually in column 2, MEM in column 3
                            metrics.cpu_usage_percent += float(parts[2])
                            mem_kb = float(parts[5])
                            metrics.memory_usage_mb += mem_kb / 1024
                        except:
                            pass
        except:
            pass
        
        return metrics
    
    def run_security_scan(self) -> SecurityMetrics:
        """Run security scans"""
        metrics = SecurityMetrics()
        metrics.last_scan = datetime.now().isoformat()
        
        # Check if safety is installed
        try:
            result = subprocess.run(
                ["python3", "-m", "pip", "show", "safety"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                metrics.scan_status = "safety_not_installed"
                return metrics
        except:
            metrics.scan_status = "safety_not_available"
            return metrics
        
        # Run safety check
        try:
            result = subprocess.run(
                ["python3", "-m", "safety", "check", "--json"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    # Parse vulnerabilities
                    for vuln in data:
                        severity = vuln.get('severity', 'unknown').lower()
                        if 'critical' in severity:
                            metrics.vulnerabilities_critical += 1
                        elif 'high' in severity:
                            metrics.vulnerabilities_high += 1
                        elif 'medium' in severity:
                            metrics.vulnerabilities_medium += 1
                        else:
                            metrics.vulnerabilities_low += 1
                    
                    metrics.scan_status = "completed"
                except:
                    metrics.scan_status = "completed_no_issues"
        except:
            metrics.scan_status = "error"
        
        return metrics
    
    def check_documentation(self) -> DocumentationMetrics:
        """Check documentation completeness"""
        metrics = DocumentationMetrics()
        
        # Check for README
        metrics.readme_present = (self.project_dir / "README.md").exists()
        
        # Check for API docs
        api_docs = self.project_dir / "CursorDocsIndex" / "DEPLOY-GUIDE.md"
        metrics.api_docs_present = api_docs.exists()
        
        # Count Python modules and their docstrings
        py_files = [f for f in self.project_dir.glob("*.py") 
                   if not f.name.startswith('_') and f.name != 'setup.py']
        
        metrics.total_modules = len(py_files)
        
        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    # Check for module docstring (triple quotes at start)
                    if '"""' in content[:500] or "'''" in content[:500]:
                        metrics.documented_modules += 1
                    
                    # Count functions
                    for line in content.split('\n'):
                        if line.strip().startswith('def '):
                            metrics.total_functions += 1
                            # Simple check: if docstring follows function
                            func_idx = content.find(line)
                            next_lines = content[func_idx:func_idx+200]
                            if '"""' in next_lines or "'''" in next_lines:
                                metrics.documented_functions += 1
            except:
                pass
        
        # Calculate completeness
        if metrics.total_modules > 0:
            module_completeness = (metrics.documented_modules / metrics.total_modules) * 100
            if metrics.total_functions > 0:
                function_completeness = (metrics.documented_functions / metrics.total_functions) * 100
                metrics.completeness_percent = (module_completeness + function_completeness) / 2
            else:
                metrics.completeness_percent = module_completeness
        
        return metrics
    
    def assess_deployment_readiness(self, 
                                   code: CodeMetrics,
                                   api: APIHealthMetrics,
                                   tests: TestMetrics,
                                   security: SecurityMetrics,
                                   docs: DocumentationMetrics) -> DeploymentReadiness:
        """Assess overall deployment readiness"""
        readiness = DeploymentReadiness()
        
        checklist = {
            "code_present": code.total_files > 0,
            "api_endpoints_defined": api.total_endpoints > 0,
            "readme_exists": docs.readme_present,
            "no_critical_vulnerabilities": security.vulnerabilities_critical == 0,
            "documentation_adequate": docs.completeness_percent > 30,
            "tests_exist": tests.total_tests > 0 or tests.test_status == "pytest_not_installed"
        }
        
        readiness.checklist = checklist
        
        # Identify blockers
        if not checklist["code_present"]:
            readiness.blockers.append("No code files found")
        
        if security.vulnerabilities_critical > 0:
            readiness.blockers.append(f"{security.vulnerabilities_critical} critical vulnerabilities found")
        
        # Identify warnings
        if not checklist["readme_exists"]:
            readiness.warnings.append("README.md not found")
        
        if tests.test_status == "no_tests_found":
            readiness.warnings.append("No tests found")
        
        if security.vulnerabilities_high > 0:
            readiness.warnings.append(f"{security.vulnerabilities_high} high-severity vulnerabilities found")
        
        if docs.completeness_percent < 50:
            readiness.warnings.append(f"Documentation only {docs.completeness_percent:.1f}% complete")
        
        # Overall readiness
        readiness.ready = len(readiness.blockers) == 0 and all(checklist.values())
        
        return readiness
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive dashboard report"""
        print("🔍 Gathering development metrics...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_dir": str(self.project_dir),
            "report_type": "development_progress",
        }
        
        # Gather all metrics
        print("  📊 Scanning codebase...")
        code_metrics = self.scan_codebase()
        report["code_metrics"] = asdict(code_metrics)
        
        print("  🔌 Checking API health...")
        api_metrics = self.check_api_health()
        report["api_health"] = asdict(api_metrics)
        
        print("  🧪 Running tests...")
        test_metrics = self.run_tests()
        report["test_metrics"] = asdict(test_metrics)
        
        print("  ⚡ Gathering performance metrics...")
        perf_metrics = self.gather_performance_metrics()
        report["performance_metrics"] = asdict(perf_metrics)
        
        print("  🔒 Running security scan...")
        security_metrics = self.run_security_scan()
        report["security_metrics"] = asdict(security_metrics)
        
        print("  📝 Checking documentation...")
        doc_metrics = self.check_documentation()
        report["documentation_metrics"] = asdict(doc_metrics)
        
        print("  🚀 Assessing deployment readiness...")
        deployment_readiness = self.assess_deployment_readiness(
            code_metrics, api_metrics, test_metrics, security_metrics, doc_metrics
        )
        report["deployment_readiness"] = asdict(deployment_readiness)
        
        # Calculate overall progress
        progress_score = self._calculate_progress_score(report)
        report["overall_progress_percent"] = progress_score
        
        return report
    
    def _calculate_progress_score(self, report: Dict[str, Any]) -> float:
        """Calculate overall progress percentage"""
        scores = []
        
        # Code completeness (30%)
        code = report["code_metrics"]
        if code["total_files"] > 0:
            code_score = min(100, (code["total_files"] / 10) * 100)
            scores.append((code_score, 0.3))
        
        # API health (15%)
        api = report["api_health"]
        if api["total_endpoints"] > 0 and api["status"] == "running":
            api_score = (api["healthy_endpoints"] / api["total_endpoints"]) * 100
            scores.append((api_score, 0.15))
        elif api["total_endpoints"] > 0:
            scores.append((50, 0.15))
        
        # Tests (20%)
        tests = report["test_metrics"]
        if tests["total_tests"] > 0:
            test_score = (tests["passed_tests"] / tests["total_tests"]) * 100
            scores.append((test_score, 0.2))
        
        # Security (20%)
        security = report["security_metrics"]
        if security["scan_status"] in ["completed", "completed_no_issues"]:
            total_vulns = (security["vulnerabilities_critical"] + 
                          security["vulnerabilities_high"] +
                          security["vulnerabilities_medium"])
            if total_vulns == 0:
                scores.append((100, 0.2))
            else:
                security_score = max(0, 100 - (total_vulns * 10))
                scores.append((security_score, 0.2))
        
        # Documentation (15%)
        docs = report["documentation_metrics"]
        scores.append((docs["completeness_percent"], 0.15))
        
        # Calculate weighted average
        if scores:
            total_score = sum(score * weight for score, weight in scores)
            total_weight = sum(weight for _, weight in scores)
            return total_score / total_weight if total_weight > 0 else 0
        
        return 0.0
    
    def save_report(self, report: Dict[str, Any]) -> Path:
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"dev_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save as latest
        latest_file = self.reports_dir / "latest_report.json"
        with open(latest_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def format_report_text(self, report: Dict[str, Any]) -> str:
        """Format report as readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("🎯 VIRTUAL AGENT DEVELOPMENT PROGRESS REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {report['timestamp']}")
        lines.append(f"Overall Progress: {report['overall_progress_percent']:.1f}%")
        lines.append("")
        
        # Code Status
        lines.append("📊 CODE COMPLETION STATUS")
        lines.append("-" * 80)
        code = report["code_metrics"]
        lines.append(f"  Total Files: {code['total_files']} ({code['python_files']} Python, {code['javascript_files']} JS, {code['markdown_files']} MD)")
        lines.append(f"  Total Lines: {code['total_lines']:,}")
        lines.append(f"  ✅ Completed Features ({len(code['completed_features'])}):")
        for feature in code['completed_features']:
            lines.append(f"     - {feature}")
        if code['in_progress_features']:
            lines.append(f"  🔄 In Progress ({len(code['in_progress_features'])}):")
            for feature in code['in_progress_features']:
                lines.append(f"     - {feature}")
        lines.append("")
        
        # API Health
        lines.append("🔌 API INTEGRATION HEALTH")
        lines.append("-" * 80)
        api = report["api_health"]
        lines.append(f"  Status: {api['status'].upper()}")
        lines.append(f"  Endpoints: {api['healthy_endpoints']}/{api['total_endpoints']} healthy")
        lines.append(f"  Last Check: {api['last_check']}")
        lines.append("")
        
        # Tests
        lines.append("🧪 TEST RESULTS")
        lines.append("-" * 80)
        tests = report["test_metrics"]
        lines.append(f"  Status: {tests['test_status']}")
        if tests['total_tests'] > 0:
            lines.append(f"  Total: {tests['total_tests']} tests")
            lines.append(f"  ✅ Passed: {tests['passed_tests']}")
            lines.append(f"  ❌ Failed: {tests['failed_tests']}")
            lines.append(f"  ⏭️  Skipped: {tests['skipped_tests']}")
            if tests['coverage_percent'] > 0:
                lines.append(f"  Coverage: {tests['coverage_percent']:.1f}%")
        lines.append("")
        
        # Performance
        lines.append("⚡ PERFORMANCE METRICS")
        lines.append("-" * 80)
        perf = report["performance_metrics"]
        lines.append(f"  Memory Usage: {perf['memory_usage_mb']:.1f} MB")
        lines.append(f"  CPU Usage: {perf['cpu_usage_percent']:.1f}%")
        if perf['avg_response_time_ms'] > 0:
            lines.append(f"  Avg Response Time: {perf['avg_response_time_ms']:.1f} ms")
        lines.append("")
        
        # Security
        lines.append("🔒 SECURITY SCAN RESULTS")
        lines.append("-" * 80)
        security = report["security_metrics"]
        lines.append(f"  Scan Status: {security['scan_status']}")
        total_vulns = (security['vulnerabilities_critical'] + 
                      security['vulnerabilities_high'] +
                      security['vulnerabilities_medium'] +
                      security['vulnerabilities_low'])
        if total_vulns > 0:
            lines.append(f"  🚨 Critical: {security['vulnerabilities_critical']}")
            lines.append(f"  ⚠️  High: {security['vulnerabilities_high']}")
            lines.append(f"  ⚡ Medium: {security['vulnerabilities_medium']}")
            lines.append(f"  ℹ️  Low: {security['vulnerabilities_low']}")
        else:
            lines.append("  ✅ No vulnerabilities found")
        lines.append("")
        
        # Documentation
        lines.append("📝 DOCUMENTATION COMPLETENESS")
        lines.append("-" * 80)
        docs = report["documentation_metrics"]
        lines.append(f"  README Present: {'✅' if docs['readme_present'] else '❌'}")
        lines.append(f"  API Docs Present: {'✅' if docs['api_docs_present'] else '❌'}")
        lines.append(f"  Documented Modules: {docs['documented_modules']}/{docs['total_modules']}")
        lines.append(f"  Documented Functions: {docs['documented_functions']}/{docs['total_functions']}")
        lines.append(f"  Overall Completeness: {docs['completeness_percent']:.1f}%")
        lines.append("")
        
        # Deployment Readiness
        lines.append("🚀 DEPLOYMENT READINESS")
        lines.append("-" * 80)
        deployment = report["deployment_readiness"]
        lines.append(f"  Ready to Deploy: {'✅ YES' if deployment['ready'] else '❌ NO'}")
        lines.append("")
        lines.append("  Checklist:")
        for item, status in deployment['checklist'].items():
            status_icon = "✅" if status else "❌"
            lines.append(f"    {status_icon} {item.replace('_', ' ').title()}")
        
        if deployment['blockers']:
            lines.append("")
            lines.append("  🚫 BLOCKERS:")
            for blocker in deployment['blockers']:
                lines.append(f"    - {blocker}")
        
        if deployment['warnings']:
            lines.append("")
            lines.append("  ⚠️  WARNINGS:")
            for warning in deployment['warnings']:
                lines.append(f"    - {warning}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def start_monitoring(self):
        """Start continuous monitoring with 30-minute intervals"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    print(f"\n{'='*80}")
                    print(f"🔄 Starting scheduled monitoring run at {datetime.now()}")
                    print(f"{'='*80}\n")
                    
                    # Generate and save report
                    report = self.generate_report()
                    report_file = self.save_report(report)
                    
                    # Print formatted report
                    print("\n" + self.format_report_text(report))
                    print(f"\n💾 Report saved to: {report_file}")
                    
                    # Wait 30 minutes
                    print(f"\n⏰ Next report in 30 minutes ({(datetime.now() + timedelta(seconds=self.report_interval)).strftime('%H:%M:%S')})")
                    time.sleep(self.report_interval)
                    
                except Exception as e:
                    print(f"\n❌ Error in monitoring loop: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("✅ Monitoring started! Reports will be generated every 30 minutes.")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("🛑 Monitoring stopped.")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Virtual Agent Development Progress Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dir',
        default=os.getcwd(),
        help='Project directory to monitor (default: current directory)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=1800,
        help='Report interval in seconds (default: 1800 = 30 minutes)'
    )
    
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run continuously with scheduled reports'
    )
    
    parser.add_argument(
        '--output',
        choices=['text', 'json', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = DevelopmentMonitor(args.dir)
    monitor.report_interval = args.interval
    
    try:
        if args.continuous:
            print("🚀 Starting continuous monitoring...")
            print(f"📁 Project: {monitor.project_dir}")
            print(f"⏰ Interval: {args.interval // 60} minutes")
            print("\nPress Ctrl+C to stop monitoring\n")
            
            monitor.start_monitoring()
            
            # Keep main thread alive
            while True:
                time.sleep(1)
        else:
            # Single report
            print("🎯 Generating single development progress report...\n")
            report = monitor.generate_report()
            
            if args.output in ['text', 'both']:
                print("\n" + monitor.format_report_text(report))
            
            if args.output in ['json', 'both']:
                report_file = monitor.save_report(report)
                print(f"\n💾 Report saved to: {report_file}")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring interrupted by user")
        monitor.stop_monitoring()
        sys.exit(0)


if __name__ == "__main__":
    main()
