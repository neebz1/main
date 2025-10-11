# 🚀 DevOps Monitoring - Quick Reference

## One-Line Commands

```bash
# Run health check
python devops_monitor.py --check

# Start dashboard
python monitoring_dashboard.py

# Run tests
pytest test_devops_monitor.py -v

# Quick start (install deps + run)
./start-monitoring.sh

# View examples
python monitoring_examples.py
```

## Common Tasks

### Check API Key Status
```bash
python devops_monitor.py --check | grep "API Keys"
```

### Check System Health Only
```python
from devops_monitor import DevOpsMonitor
monitor = DevOpsMonitor()
health = monitor.check_system_health()
print(f"Status: {health.status}")
```

### Get Available Providers
```python
from devops_monitor import DevOpsMonitor
monitor = DevOpsMonitor()
providers = monitor.get_provider_fallback_order()
print(providers)
```

### Use Multi-Provider AI
```python
from multi_provider_ai import MultiProviderAI
ai = MultiProviderAI()
response, error = ai.chat("Hello!")
print(response)
```

## File Locations

| What | Where |
|------|-------|
| Core system | `devops_monitor.py` |
| Tests | `test_devops_monitor.py` |
| Dashboard | `monitoring_dashboard.py` |
| Multi-provider | `multi_provider_ai.py` |
| Examples | `monitoring_examples.py` |
| Reports | `monitoring_reports/` |
| Latest report | `monitoring_reports/latest_report.json` |
| Quick start guide | `MONITORING_README.md` |
| Full docs | `MONITORING_DOCS.md` |
| Status report | `MONITORING_STATUS_REPORT.md` |

## GitHub Actions

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| `monitoring.yml` | Hourly | Health checks |
| `tests.yml` | On push/PR | Testing |
| `security.yml` | Daily | Security scans |

## Environment Variables

```bash
# Add to .env file
TOGETHER_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
OPENROUTER_API_KEY=your_key
GOOGLE_API_KEY=your_key
MOONSHOT_API_KEY=your_key
```

## Status Indicators

| Indicator | Meaning |
|-----------|---------|
| ✅ | Working/Present |
| ❌ | Missing/Failed |
| ⚠️ | Warning |
| 🚨 | Critical |
| 🟢 | Healthy |
| 🟡 | Warning |
| 🔴 | Critical |

## Thresholds

| Resource | Warning | Critical |
|----------|---------|----------|
| CPU | 80% | 90% |
| Memory | 80% | 90% |
| Disk | 80% | 90% |

## Integration Snippet

```python
# Add to your app startup
from devops_monitor import DevOpsMonitor
from multi_provider_ai import MultiProviderAI

monitor = DevOpsMonitor()
report = monitor.perform_health_check()

ai = MultiProviderAI()
if not ai.client:
    print("⚠️ No AI provider available")
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No API keys | Add keys to `.env` |
| Tests failing | `pip install -r requirements_monitoring.txt` |
| Dashboard crash | Try `--simple` mode |
| High resources | Check running processes |
| Reports not saved | Check write permissions |

## Help

```bash
python devops_monitor.py --help
python monitoring_dashboard.py --help
pytest test_devops_monitor.py --help
```

## Quick Links

- [README](MONITORING_README.md) - Getting started
- [Docs](MONITORING_DOCS.md) - Full documentation  
- [Examples](monitoring_examples.py) - Integration examples
- [Status](MONITORING_STATUS_REPORT.md) - Implementation status

---

**Need more help?** Check the full documentation in `MONITORING_DOCS.md`
