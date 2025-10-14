#!/usr/bin/env python3
"""
Verification script for Advanced AI Development Environment
Checks that all components are properly installed and configured
"""

import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Tuple, Dict, Any

class SetupVerifier:
    """Verify advanced AI dev setup"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
        
    def check_command(self, command: str, name: str) -> bool:
        """Check if a command exists"""
        try:
            subprocess.run([command, "--version"], 
                         capture_output=True, 
                         check=True,
                         timeout=5)
            print(f"✅ {name}: Found")
            self.checks_passed += 1
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print(f"❌ {name}: Not found - install with: brew install {command}")
            self.checks_failed += 1
            return False
    
    def check_python_package(self, package: str, name: str = None) -> bool:
        """Check if a Python package is installed"""
        if name is None:
            name = package
        
        try:
            importlib.import_module(package)
            print(f"✅ {name}: Installed")
            self.checks_passed += 1
            return True
        except ImportError:
            print(f"❌ {name}: Not installed")
            self.checks_failed += 1
            return False
    
    def check_service(self, service: str, port: int) -> bool:
        """Check if a service is running"""
        import socket
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"✅ {service}: Running on port {port}")
            self.checks_passed += 1
            return True
        else:
            print(f"⚠️  {service}: Not running (port {port}) - start with: brew services start {service}")
            self.warnings += 1
            return False
    
    def check_file_exists(self, path: Path, name: str) -> bool:
        """Check if a file exists"""
        if path.exists():
            print(f"✅ {name}: Found at {path}")
            self.checks_passed += 1
            return True
        else:
            print(f"❌ {name}: Not found at {path}")
            self.checks_failed += 1
            return False
    
    def verify_system_tools(self):
        """Verify system tools"""
        print("\n🔧 System Tools")
        print("=" * 60)
        
        tools = [
            ("python3.11", "Python 3.11+"),
            ("brew", "Homebrew"),
            ("cmake", "CMake"),
            ("rust", "Rust"),
            ("cargo", "Cargo"),
            ("go", "Go"),
            ("node", "Node.js"),
            ("npm", "NPM"),
        ]
        
        for cmd, name in tools:
            self.check_command(cmd, name)
    
    def verify_python_packages(self):
        """Verify Python packages"""
        print("\n🐍 Python Packages (Core)")
        print("=" * 60)
        
        packages = [
            ("torch", "PyTorch"),
            ("transformers", "HuggingFace Transformers"),
            ("langchain", "LangChain"),
            ("fastapi", "FastAPI"),
            ("typer", "Typer"),
            ("rich", "Rich"),
        ]
        
        for pkg, name in packages:
            self.check_python_package(pkg, name)
        
        print("\n🚀 Advanced Packages")
        print("=" * 60)
        
        advanced_packages = [
            ("peft", "PEFT (LoRA)"),
            ("bitsandbytes", "BitsAndBytes"),
            ("chromadb", "ChromaDB"),
            ("sentence_transformers", "Sentence Transformers"),
        ]
        
        for pkg, name in advanced_packages:
            try:
                importlib.import_module(pkg)
                print(f"✅ {name}: Installed")
                self.checks_passed += 1
            except ImportError:
                print(f"⚠️  {name}: Not installed (optional)")
                self.warnings += 1
    
    def verify_services(self):
        """Verify services"""
        print("\n🌐 Services")
        print("=" * 60)
        
        services = [
            ("Redis", 6379),
            ("Ollama", 11434),
        ]
        
        for service, port in services:
            self.check_service(service.lower(), port)
    
    def verify_project_structure(self):
        """Verify project structure"""
        print("\n📁 Project Structure")
        print("=" * 60)
        
        workspace = Path("/Users/nr/Documents/GitHub/main")
        
        files = [
            (workspace / "advanced_ai_dev_setup.py", "Setup Script"),
            (workspace / "advanced_ai_cli.py", "CLI Tool"),
            (workspace / "launch_advanced_ai_env.sh", "Launcher"),
            (workspace / "ADVANCED-AI-DEV-SETUP.md", "Documentation"),
            (workspace / "advanced_ai_tools" / "advanced_agent_system.py", "Agent System"),
            (workspace / "advanced_ai_tools" / "model_serving_advanced.py", "Model Serving"),
            (workspace / "advanced_ai_tools" / "fine_tuning_system.py", "Fine-Tuning"),
            (workspace / "advanced_ai_tools" / "code_intelligence.py", "Code Intelligence"),
            (workspace / "advanced_ai_tools" / "ai_monitoring_system.py", "Monitoring"),
            (workspace / "advanced_ai_tools" / "experimental_tools.py", "Experimental Tools"),
        ]
        
        for path, name in files:
            self.check_file_exists(path, name)
    
    def verify_configuration(self):
        """Verify configuration"""
        print("\n⚙️  Configuration")
        print("=" * 60)
        
        config_dir = Path.home() / ".config" / "advanced_ai_dev"
        
        if config_dir.exists():
            print(f"✅ Config directory: {config_dir}")
            self.checks_passed += 1
        else:
            print(f"⚠️  Config directory not found (will be created on first run)")
            self.warnings += 1
    
    def verify_rust_tools(self):
        """Verify Rust tools"""
        print("\n🦀 Rust Tools (Optional)")
        print("=" * 60)
        
        tools = [
            ("rg", "ripgrep"),
            ("fd", "fd"),
            ("bat", "bat"),
        ]
        
        for cmd, name in tools:
            try:
                subprocess.run([cmd, "--version"], 
                             capture_output=True, 
                             check=True,
                             timeout=5)
                print(f"✅ {name}: Found")
                self.checks_passed += 1
            except:
                print(f"⚠️  {name}: Not found (optional) - install with: cargo install {cmd}")
                self.warnings += 1
    
    def print_summary(self):
        """Print verification summary"""
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        
        total = self.checks_passed + self.checks_failed
        
        print(f"\n✅ Passed: {self.checks_passed}")
        print(f"❌ Failed: {self.checks_failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        
        if self.checks_failed == 0:
            print("\n🎉 All critical checks passed!")
            print("🚀 Your advanced AI development environment is ready!")
            print("\nNext steps:")
            print("  1. Run: ./launch_advanced_ai_env.sh")
            print("  2. Or: python advanced_ai_cli.py status")
            print("  3. Read: ADVANCED-AI-DEV-SETUP.md")
            return 0
        else:
            print("\n⚠️  Some checks failed. Please install missing components.")
            print("\nTo install missing components:")
            print("  1. Run: ./install_advanced_ai_tools.sh")
            print("  2. Or install manually using the commands above")
            return 1
    
    def run_all_checks(self) -> int:
        """Run all verification checks"""
        print("=" * 60)
        print("🔍 ADVANCED AI DEVELOPMENT ENVIRONMENT VERIFICATION")
        print("=" * 60)
        
        self.verify_system_tools()
        self.verify_python_packages()
        self.verify_services()
        self.verify_project_structure()
        self.verify_configuration()
        self.verify_rust_tools()
        
        return self.print_summary()

def main():
    verifier = SetupVerifier()
    exit_code = verifier.run_all_checks()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

