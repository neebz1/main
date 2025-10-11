#!/usr/bin/env python3
"""
Development Monitoring Dashboard - Web Interface
Real-time visualization of development metrics
"""

import gradio as gr
import json
import os
from pathlib import Path
from datetime import datetime
import threading
import time
from dev_monitor import DevelopmentMonitor


class MonitorDashboard:
    """Web dashboard for development monitoring"""
    
    def __init__(self, project_dir: str = None):
        self.monitor = DevelopmentMonitor(project_dir)
        self.latest_report = None
        self.monitoring_active = False
        
    def get_latest_report(self):
        """Get latest report data"""
        latest_file = self.monitor.reports_dir / "latest_report.json"
        if latest_file.exists():
            with open(latest_file, 'r') as f:
                return json.load(f)
        return None
    
    def generate_single_report(self):
        """Generate a single report"""
        try:
            report = self.monitor.generate_report()
            self.monitor.save_report(report)
            self.latest_report = report
            return self.format_dashboard_html(report)
        except Exception as e:
            return f"<div style='color: red;'>Error generating report: {str(e)}</div>"
    
    def start_continuous_monitoring(self):
        """Start continuous monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor.start_monitoring()
            return "✅ Monitoring started! Reports will be generated every 30 minutes."
        return "⚠️ Monitoring is already active."
    
    def stop_continuous_monitoring(self):
        """Stop continuous monitoring"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.monitor.stop_monitoring()
            return "🛑 Monitoring stopped."
        return "⚠️ Monitoring is not active."
    
    def format_dashboard_html(self, report):
        """Format report as HTML dashboard"""
        if not report:
            return "<div>No report available yet. Click 'Generate Report' to create one.</div>"
        
        # Calculate status colors
        progress = report.get('overall_progress_percent', 0)
        progress_color = "#4CAF50" if progress >= 80 else "#FF9800" if progress >= 60 else "#F44336"
        
        # Build HTML
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;">
            <h1 style="text-align: center; color: #333;">🎯 Development Progress Dashboard</h1>
            <p style="text-align: center; color: #666;">Generated: {report['timestamp']}</p>
            
            <!-- Overall Progress -->
            <div style="background: linear-gradient(135deg, {progress_color} 0%, {progress_color}AA 100%); 
                        color: white; padding: 30px; border-radius: 10px; margin: 20px 0; text-align: center;">
                <h2 style="margin: 0;">Overall Progress</h2>
                <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">{progress:.1f}%</div>
                <div style="background: rgba(255,255,255,0.3); height: 20px; border-radius: 10px; overflow: hidden; margin-top: 15px;">
                    <div style="background: white; height: 100%; width: {progress}%; transition: width 0.5s;"></div>
                </div>
            </div>
            
            <!-- Metrics Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
        """
        
        # Code Metrics Card
        code = report['code_metrics']
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #2196F3; margin-top: 0;">📊 Code Status</h3>
                    <p><strong>Files:</strong> {code['total_files']}</p>
                    <p><strong>Lines:</strong> {code['total_lines']:,}</p>
                    <p><strong>Python:</strong> {code['python_files']} files</p>
                    <p><strong>JavaScript:</strong> {code['javascript_files']} files</p>
                    <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
                        <p style="font-weight: bold;">✅ Completed: {len(code['completed_features'])}</p>
                        <p style="font-weight: bold;">🔄 In Progress: {len(code['in_progress_features'])}</p>
                    </div>
                </div>
        """
        
        # API Health Card
        api = report['api_health']
        api_color = "#4CAF50" if api['status'] == "running" else "#FF9800" if api['status'] == "stopped" else "#999"
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #4CAF50; margin-top: 0;">🔌 API Health</h3>
                    <p><strong>Status:</strong> <span style="color: {api_color}; font-weight: bold;">{api['status'].upper()}</span></p>
                    <p><strong>Endpoints:</strong> {api['healthy_endpoints']}/{api['total_endpoints']}</p>
                    <p><strong>Last Check:</strong> {api['last_check'][:19].replace('T', ' ')}</p>
                </div>
        """
        
        # Test Results Card
        tests = report['test_metrics']
        test_color = "#4CAF50" if tests['test_status'] == "completed" and tests['failed_tests'] == 0 else "#FF9800"
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #9C27B0; margin-top: 0;">🧪 Tests</h3>
                    <p><strong>Status:</strong> <span style="color: {test_color};">{tests['test_status']}</span></p>
        """
        if tests['total_tests'] > 0:
            pass_rate = (tests['passed_tests'] / tests['total_tests']) * 100
            html += f"""
                    <p><strong>Total:</strong> {tests['total_tests']}</p>
                    <p><strong>✅ Passed:</strong> {tests['passed_tests']}</p>
                    <p><strong>❌ Failed:</strong> {tests['failed_tests']}</p>
                    <p><strong>Pass Rate:</strong> {pass_rate:.1f}%</p>
            """
        html += """
                </div>
        """
        
        # Performance Card
        perf = report['performance_metrics']
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #FF9800; margin-top: 0;">⚡ Performance</h3>
                    <p><strong>Memory:</strong> {perf['memory_usage_mb']:.1f} MB</p>
                    <p><strong>CPU:</strong> {perf['cpu_usage_percent']:.1f}%</p>
        """
        if perf['avg_response_time_ms'] > 0:
            html += f"""
                    <p><strong>Avg Response:</strong> {perf['avg_response_time_ms']:.1f} ms</p>
            """
        html += """
                </div>
        """
        
        # Security Card
        security = report['security_metrics']
        total_vulns = (security['vulnerabilities_critical'] + 
                      security['vulnerabilities_high'] +
                      security['vulnerabilities_medium'] +
                      security['vulnerabilities_low'])
        security_color = "#4CAF50" if total_vulns == 0 else "#F44336" if security['vulnerabilities_critical'] > 0 else "#FF9800"
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #F44336; margin-top: 0;">🔒 Security</h3>
                    <p><strong>Status:</strong> {security['scan_status']}</p>
        """
        if total_vulns > 0:
            html += f"""
                    <p style="color: {security_color}; font-weight: bold;">⚠️ {total_vulns} vulnerabilities</p>
                    <p>🚨 Critical: {security['vulnerabilities_critical']}</p>
                    <p>⚠️ High: {security['vulnerabilities_high']}</p>
                    <p>⚡ Medium: {security['vulnerabilities_medium']}</p>
                    <p>ℹ️ Low: {security['vulnerabilities_low']}</p>
            """
        else:
            html += """
                    <p style="color: #4CAF50; font-weight: bold;">✅ No vulnerabilities</p>
            """
        html += """
                </div>
        """
        
        # Documentation Card
        docs = report['documentation_metrics']
        docs_color = "#4CAF50" if docs['completeness_percent'] >= 70 else "#FF9800" if docs['completeness_percent'] >= 40 else "#F44336"
        html += f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h3 style="color: #607D8B; margin-top: 0;">📝 Documentation</h3>
                    <p><strong>Completeness:</strong> <span style="color: {docs_color}; font-weight: bold;">{docs['completeness_percent']:.1f}%</span></p>
                    <p><strong>README:</strong> {'✅' if docs['readme_present'] else '❌'}</p>
                    <p><strong>API Docs:</strong> {'✅' if docs['api_docs_present'] else '❌'}</p>
                    <p><strong>Documented Modules:</strong> {docs['documented_modules']}/{docs['total_modules']}</p>
                    <p><strong>Documented Functions:</strong> {docs['documented_functions']}/{docs['total_functions']}</p>
                </div>
        """
        
        html += """
            </div>
        """
        
        # Deployment Readiness
        deployment = report['deployment_readiness']
        deployment_color = "#4CAF50" if deployment['ready'] else "#F44336"
        html += f"""
            <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 20px;">
                <h2 style="color: {deployment_color}; margin-top: 0;">🚀 Deployment Readiness</h2>
                <div style="font-size: 24px; font-weight: bold; color: {deployment_color}; margin-bottom: 20px;">
                    {'✅ READY TO DEPLOY' if deployment['ready'] else '❌ NOT READY'}
                </div>
                
                <h3>Checklist:</h3>
                <ul style="list-style: none; padding: 0;">
        """
        
        for item, status in deployment['checklist'].items():
            icon = "✅" if status else "❌"
            html += f"""
                    <li style="padding: 5px 0;">{icon} {item.replace('_', ' ').title()}</li>
            """
        
        html += """
                </ul>
        """
        
        if deployment['blockers']:
            html += """
                <div style="background: #ffebee; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="color: #c62828; margin-top: 0;">🚫 Blockers:</h4>
                    <ul>
            """
            for blocker in deployment['blockers']:
                html += f"<li>{blocker}</li>"
            html += """
                    </ul>
                </div>
            """
        
        if deployment['warnings']:
            html += """
                <div style="background: #fff3e0; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="color: #ef6c00; margin-top: 0;">⚠️ Warnings:</h4>
                    <ul>
            """
            for warning in deployment['warnings']:
                html += f"<li>{warning}</li>"
            html += """
                    </ul>
                </div>
            """
        
        html += """
            </div>
            
            <!-- Feature Status -->
            <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 20px;">
                <h2 style="color: #333; margin-top: 0;">📋 Feature Status</h2>
        """
        
        if code['completed_features']:
            html += """
                <h3 style="color: #4CAF50;">✅ Completed Features:</h3>
                <ul>
            """
            for feature in code['completed_features']:
                html += f"<li>{feature}</li>"
            html += "</ul>"
        
        if code['in_progress_features']:
            html += """
                <h3 style="color: #FF9800;">🔄 In Progress:</h3>
                <ul>
            """
            for feature in code['in_progress_features']:
                html += f"<li>{feature}</li>"
            html += "</ul>"
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="Development Monitor Dashboard", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🎯 Virtual Agent Development Progress Monitor")
            gr.Markdown("Real-time monitoring and reporting of development metrics")
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 Generate Report", variant="primary", scale=2)
                start_btn = gr.Button("▶️ Start Continuous Monitoring", scale=1)
                stop_btn = gr.Button("⏹️ Stop Monitoring", scale=1)
            
            status_text = gr.Textbox(label="Status", interactive=False, scale=1)
            
            dashboard_html = gr.HTML(label="Dashboard")
            
            # Button actions
            refresh_btn.click(
                fn=self.generate_single_report,
                outputs=dashboard_html
            )
            
            start_btn.click(
                fn=self.start_continuous_monitoring,
                outputs=status_text
            )
            
            stop_btn.click(
                fn=self.stop_continuous_monitoring,
                outputs=status_text
            )
            
            # Auto-load latest report on startup
            interface.load(
                fn=lambda: self.format_dashboard_html(self.get_latest_report()),
                outputs=dashboard_html
            )
        
        return interface


def main():
    """Launch dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Development Monitoring Dashboard")
    parser.add_argument('--dir', default=os.getcwd(), help='Project directory')
    parser.add_argument('--port', type=int, default=7862, help='Port number (default: 7862)')
    parser.add_argument('--share', action='store_true', help='Create public share link')
    
    args = parser.parse_args()
    
    print("🚀 Starting Development Monitor Dashboard...")
    print(f"📁 Monitoring: {args.dir}")
    
    dashboard = MonitorDashboard(args.dir)
    interface = dashboard.create_interface()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=args.port,
        share=args.share
    )


if __name__ == "__main__":
    main()
