#!/usr/bin/env python3
"""
Monitoring Dashboard - Real-time monitoring display
Provides a comprehensive view of system health and API status
"""

import os
import json
import time
import curses
from pathlib import Path
from datetime import datetime
from devops_monitor import DevOpsMonitor


class MonitoringDashboard:
    """Interactive monitoring dashboard"""
    
    def __init__(self):
        self.monitor = DevOpsMonitor()
        self.running = True
        self.refresh_interval = 60  # seconds
    
    def draw_header(self, stdscr, width):
        """Draw dashboard header"""
        header = "🔍 DevOps Monitoring Dashboard"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        stdscr.addstr(0, 0, "=" * width)
        stdscr.addstr(1, (width - len(header)) // 2, header, curses.A_BOLD)
        stdscr.addstr(2, width - len(timestamp) - 2, timestamp)
        stdscr.addstr(3, 0, "=" * width)
    
    def draw_api_status(self, stdscr, start_row, width):
        """Draw API key status section"""
        stdscr.addstr(start_row, 0, "📋 API KEY STATUS", curses.A_BOLD)
        stdscr.addstr(start_row + 1, 0, "-" * width)
        
        row = start_row + 2
        for env_var, config in self.monitor.PROVIDERS.items():
            status = self.monitor.check_api_key_status(env_var, config)
            
            icon = "✅" if status.key_present else "❌"
            status_text = f"{icon} {config['name']:<30} "
            
            if status.key_present:
                if status.key_valid is True:
                    status_text += "Valid"
                elif status.key_valid is False:
                    status_text += "INVALID"
                else:
                    status_text += "Not tested"
            else:
                status_text += "Missing"
            
            stdscr.addstr(row, 2, status_text)
            row += 1
        
        return row + 1
    
    def draw_system_health(self, stdscr, start_row, width):
        """Draw system health section"""
        stdscr.addstr(start_row, 0, "💻 SYSTEM HEALTH", curses.A_BOLD)
        stdscr.addstr(start_row + 1, 0, "-" * width)
        
        health = self.monitor.check_system_health()
        
        row = start_row + 2
        
        # Status
        status_icon = "✅" if health.status == "healthy" else "⚠️" if health.status == "warning" else "🚨"
        stdscr.addstr(row, 2, f"{status_icon} Overall Status: {health.status.upper()}")
        row += 1
        
        # CPU
        cpu_bar = self.create_progress_bar(health.cpu_percent, width - 20)
        stdscr.addstr(row, 2, f"CPU:    {cpu_bar} {health.cpu_percent:.1f}%")
        row += 1
        
        # Memory
        mem_bar = self.create_progress_bar(health.memory_percent, width - 20)
        stdscr.addstr(row, 2, f"Memory: {mem_bar} {health.memory_percent:.1f}%")
        row += 1
        
        # Disk
        disk_bar = self.create_progress_bar(health.disk_percent, width - 20)
        stdscr.addstr(row, 2, f"Disk:   {disk_bar} {health.disk_percent:.1f}%")
        row += 1
        
        return row + 1
    
    def create_progress_bar(self, percent, width=30):
        """Create a text-based progress bar"""
        filled = int((percent / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    def draw_footer(self, stdscr, height, width):
        """Draw dashboard footer"""
        footer1 = f"Press 'q' to quit | Auto-refresh: {self.refresh_interval}s"
        footer2 = "Press 'r' to refresh now"
        
        stdscr.addstr(height - 3, 0, "=" * width)
        stdscr.addstr(height - 2, 2, footer1)
        stdscr.addstr(height - 1, 2, footer2)
    
    def draw_simple(self):
        """Draw simple terminal-based dashboard (no curses)"""
        while self.running:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print("🔍 DevOps Monitoring Dashboard")
            print("=" * 70)
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)
            print()
            
            # API Status
            print("📋 API KEY STATUS")
            print("-" * 70)
            for env_var, config in self.monitor.PROVIDERS.items():
                status = self.monitor.check_api_key_status(env_var, config)
                icon = "✅" if status.key_present else "❌"
                print(f"  {icon} {config['name']:<30}", end=" ")
                
                if status.key_present:
                    if status.key_valid is True:
                        print("Valid")
                    elif status.key_valid is False:
                        print("INVALID")
                    else:
                        print("Not tested")
                else:
                    print("Missing")
            
            print()
            
            # System Health
            print("💻 SYSTEM HEALTH")
            print("-" * 70)
            health = self.monitor.check_system_health()
            
            status_icon = "✅" if health.status == "healthy" else "⚠️" if health.status == "warning" else "🚨"
            print(f"  {status_icon} Overall Status: {health.status.upper()}")
            print(f"  CPU:    {self.create_progress_bar(health.cpu_percent, 40)} {health.cpu_percent:.1f}%")
            print(f"  Memory: {self.create_progress_bar(health.memory_percent, 40)} {health.memory_percent:.1f}%")
            print(f"  Disk:   {self.create_progress_bar(health.disk_percent, 40)} {health.disk_percent:.1f}%")
            
            print()
            print("=" * 70)
            print(f"Press Ctrl+C to quit | Auto-refresh in {self.refresh_interval} seconds")
            
            try:
                time.sleep(self.refresh_interval)
            except KeyboardInterrupt:
                self.running = False
                break
    
    def run_curses(self, stdscr):
        """Run dashboard with curses (interactive)"""
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)   # Non-blocking input
        stdscr.timeout(1000)  # 1 second timeout
        
        last_refresh = 0
        
        while self.running:
            current_time = time.time()
            
            # Check if we need to refresh
            if current_time - last_refresh >= self.refresh_interval:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Draw sections
                self.draw_header(stdscr, width)
                row = self.draw_api_status(stdscr, 5, width)
                row = self.draw_system_health(stdscr, row, width)
                self.draw_footer(stdscr, height, width)
                
                stdscr.refresh()
                last_refresh = current_time
            
            # Handle input
            key = stdscr.getch()
            if key == ord('q'):
                self.running = False
            elif key == ord('r'):
                last_refresh = 0  # Force refresh
    
    def run(self, use_curses=True):
        """Run the dashboard"""
        try:
            if use_curses:
                try:
                    curses.wrapper(self.run_curses)
                except Exception as e:
                    print(f"⚠️  Curses not available, using simple mode: {e}")
                    self.draw_simple()
            else:
                self.draw_simple()
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Real-time monitoring dashboard'
    )
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple terminal mode (no curses)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Refresh interval in seconds (default: 60)'
    )
    
    args = parser.parse_args()
    
    dashboard = MonitoringDashboard()
    dashboard.refresh_interval = args.interval
    
    print("🚀 Starting monitoring dashboard...")
    print()
    
    dashboard.run(use_curses=not args.simple)


if __name__ == "__main__":
    main()
