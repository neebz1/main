# 🔍 DevOps Monitoring System

[![Status](https://img.shields.io/badge/status-operational-brightgreen)](./monitoring_reports/latest_report.json)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](./test_devops_monitor.py)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)

Comprehensive DevOps monitoring system for virtual agent development environments. Monitors API keys, system health, and provides automated maintenance and reporting.

## 🎯 Features

- ✅ **API Key Monitoring** - Validates presence and validity of all AI provider keys
- 🏥 **System Health Checks** - Monitors CPU, memory, and disk usage
- 📊 **Automated Reporting** - JSON reports with historical tracking
- 🔄 **Provider Fallback** - Automatic failover between AI providers
- 🚨 **GitHub Actions Integration** - Automated monitoring and issue creation
- 🔒 **Security Scanning** - Dependency and secret scanning
- 📈 **Real-time Dashboard** - Live monitoring display
- 🧪 **Comprehensive Tests** - 20+ unit tests with mocking

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements_monitoring.txt

# Or install minimal requirements
pip install psutil requests python-dotenv pytest
```

### Run Health Check

```bash
# Basic health check
python devops_monitor.py --check

# Output as JSON
python devops_monitor.py --check --json

# Using the shell script
./start-monitoring.sh
```

### Real-time Dashboard

```bash
# Run interactive dashboard
python monitoring_dashboard.py

# Simple mode (no curses)
python monitoring_dashboard.py --simple

# Custom refresh interval (30 seconds)
python monitoring_dashboard.py --interval 30
```

## 📋 Supported AI Providers

| Provider | Environment Variable | Status Check |
|----------|---------------------|--------------|
| **Together AI (Kimi K2)** | `TOGETHER_API_KEY` | ✅ Full validation |
| **OpenAI (GPT-4)** | `OPENAI_API_KEY` | ✅ Full validation |
| **Anthropic (Claude)** | `ANTHROPIC_API_KEY` | ✅ Full validation |
| **OpenRouter** | `OPENROUTER_API_KEY` | ✅ Full validation |
| **Google Gemini** | `GOOGLE_API_KEY` | ⚠️ Basic check |
| **Moonshot AI** | `MOONSHOT_API_KEY` | ✅ Full validation |

## 📊 Monitoring Output

### Console Output
```
🔍 DevOps Monitoring System - Health Check
============================================================

📋 Checking API Keys...
✅ Together AI (Kimi K2): Present
   ✅ Validation: Valid
❌ OpenAI (GPT-4): Missing
✅ Anthropic (Claude): Present
   ✅ Validation: Valid

💻 Checking System Health...
✅ Status: HEALTHY
   CPU: 45.2%
   Memory: 62.1%
   Disk: 54.8%

💡 Recommendations:
   • System is healthy - continue monitoring

📊 Report saved to: monitoring_reports
```

### JSON Report
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "api_keys": [
    {
      "provider": "Together AI (Kimi K2)",
      "key_present": true,
      "key_valid": true,
      "error_message": "API key is valid"
    }
  ],
  "system_health": {
    "cpu_percent": 45.2,
    "memory_percent": 62.1,
    "disk_percent": 54.8,
    "status": "healthy"
  },
  "issues_found": [],
  "recommendations": ["System is healthy"]
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# AI Provider API Keys
TOGETHER_API_KEY=your_together_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
GOOGLE_API_KEY=your_google_api_key
MOONSHOT_API_KEY=your_moonshot_api_key
```

### GitHub Actions Secrets

Set these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

- `TOGETHER_API_KEY`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`
- `GOOGLE_API_KEY`
- `MOONSHOT_API_KEY`

## 🤖 GitHub Actions Workflows

### 1. Monitoring Workflow
**File:** `.github/workflows/monitoring.yml`

**Triggers:**
- Hourly (cron schedule)
- Manual (workflow_dispatch)
- Push to main
- Pull requests

**Features:**
- Runs health checks
- Creates issues on failures
- Uploads monitoring reports

### 2. Test Workflow
**File:** `.github/workflows/tests.yml`

**Triggers:**
- Push to main/develop
- Pull requests

**Features:**
- Runs pytest with coverage
- Tests on Python 3.10, 3.11, 3.12
- Code linting and formatting

### 3. Security Workflow
**File:** `.github/workflows/security.yml`

**Triggers:**
- Daily at 2 AM UTC
- Manual trigger

**Features:**
- Dependency vulnerability scanning
- Code security analysis
- Secret scanning
- API key exposure detection

## 🧪 Testing

```bash
# Run all tests
pytest test_devops_monitor.py -v

# Run with coverage
pytest test_devops_monitor.py -v --cov=devops_monitor --cov-report=term

# Run specific test
pytest test_devops_monitor.py::TestDevOpsMonitor::test_check_system_health_healthy -v
```

**Test Coverage:** 20+ unit tests covering all major functionality

## 🔄 Multi-Provider Integration

Use the multi-provider AI module for automatic failover:

```python
from multi_provider_ai import MultiProviderAI

# Initialize with automatic provider selection
ai = MultiProviderAI()

# Check status
status = ai.get_status()
print(f"Using: {status['provider']}")

# Chat with automatic fallback
response, error = ai.chat("Hello, how are you?")

# Health check
health = ai.health_check()
```

## 📈 Monitoring Dashboard

The real-time dashboard provides:
- Live API key status
- System resource graphs
- Auto-refresh (configurable interval)
- Keyboard controls (q to quit, r to refresh)

## 🚨 Health Status Levels

| Level | Criteria | Badge |
|-------|----------|-------|
| **Healthy** | CPU < 80%, Memory < 80%, Disk < 80% | ![Healthy](https://img.shields.io/badge/status-healthy-brightgreen) |
| **Warning** | 80-90% usage on any resource | ![Warning](https://img.shields.io/badge/status-warning-yellow) |
| **Critical** | >90% usage on any resource | ![Critical](https://img.shields.io/badge/status-critical-red) |

## 📚 Documentation

- **[Complete Documentation](./MONITORING_DOCS.md)** - Full system documentation
- **[API Reference](#)** - Python API reference
- **[Troubleshooting](#troubleshooting)** - Common issues and solutions

## 🛠️ Integration with Existing Apps

Add monitoring to your applications:

```python
from devops_monitor import DevOpsMonitor

# In your app startup
monitor = DevOpsMonitor()
report = monitor.perform_health_check()

if report.system_health['status'] == 'critical':
    # Handle critical state
    send_alert()

# Get available providers
providers = monitor.get_provider_fallback_order()
```

## 📁 Project Structure

```
.
├── devops_monitor.py           # Core monitoring system
├── test_devops_monitor.py      # Unit tests
├── monitoring_dashboard.py     # Real-time dashboard
├── multi_provider_ai.py        # Multi-provider integration
├── start-monitoring.sh         # Quick start script
├── requirements_monitoring.txt # Dependencies
├── MONITORING_DOCS.md          # Full documentation
├── MONITORING_README.md        # This file
├── .github/workflows/
│   ├── monitoring.yml          # Monitoring workflow
│   ├── tests.yml               # Test workflow
│   └── security.yml            # Security workflow
└── monitoring_reports/         # Generated reports
    └── latest_report.json      # Latest report
```

## 🔍 Troubleshooting

### No API keys configured
**Solution:** Add at least one API key to `.env` file

### API key is invalid
**Solution:**
1. Verify key is correct
2. Check provider account status
3. Regenerate key if needed

### High system resources
**Solution:**
1. Check running processes
2. Restart resource-heavy applications
3. Clear temporary files

### Monitoring reports not generating
**Solution:**
1. Check write permissions
2. Verify dependencies installed
3. Run with `--report-dir /tmp/reports` for testing

## 🤝 Contributing

1. Add features to `devops_monitor.py`
2. Add tests to `test_devops_monitor.py`
3. Update documentation
4. Run test suite: `pytest test_devops_monitor.py -v`
5. Submit pull request

## 📝 License

Same license as parent repository.

## 🙏 Support

- **Issues:** GitHub Issues (auto-created on failures)
- **Documentation:** [MONITORING_DOCS.md](./MONITORING_DOCS.md)
- **Reports:** Check `monitoring_reports/` directory

---

**Made with ❤️ for reliable AI development environments**
