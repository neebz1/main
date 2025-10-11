# 🔍 DevOps Monitoring System Documentation

## Overview

The DevOps Monitoring System provides comprehensive monitoring, health checks, and automated maintenance for the virtual agent development environment. It monitors API keys, system resources, and implements automated error recovery and reporting.

## Features

### 1. **API Key Monitoring**
- Validates presence of API keys for all providers
- Tests API key validity by making actual API calls
- Supports multiple providers:
  - Together AI (Kimi K2)
  - OpenAI (GPT-4)
  - Anthropic (Claude)
  - OpenRouter
  - Google Gemini
  - Moonshot AI

### 2. **System Health Monitoring**
- CPU usage monitoring
- Memory usage monitoring
- Disk space monitoring
- Automatic status classification (healthy/warning/critical)

### 3. **Automated Reporting**
- JSON reports with timestamps
- Historical report storage
- Latest report tracking
- Issue identification
- Actionable recommendations

### 4. **GitHub Actions Integration**
- Hourly health checks
- Automated issue creation on failures
- Security scanning
- Automated testing
- Coverage reporting

## Quick Start

### Installation

```bash
# Install required dependencies
pip install psutil requests python-dotenv pytest
```

### Basic Usage

```bash
# Run a health check
python devops_monitor.py --check

# Output as JSON
python devops_monitor.py --check --json

# Specify custom report directory
python devops_monitor.py --check --report-dir ./my_reports
```

### Python API

```python
from devops_monitor import DevOpsMonitor
from pathlib import Path

# Create monitor instance
monitor = DevOpsMonitor(report_dir=Path('./reports'))

# Perform health check
report = monitor.perform_health_check()

# Check specific API key
status = monitor.check_api_key_status(
    'OPENAI_API_KEY',
    {'name': 'OpenAI', 'test_endpoint': 'https://api.openai.com/v1/models'}
)

# Get provider fallback order
available_providers = monitor.get_provider_fallback_order()

# Generate status badge
badge_markdown = monitor.generate_status_badge()
```

## Configuration

### Environment Variables

Set these environment variables for API key monitoring:

```bash
# AI Provider API Keys
export TOGETHER_API_KEY="your_together_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export OPENROUTER_API_KEY="your_openrouter_api_key"
export GOOGLE_API_KEY="your_google_api_key"
export MOONSHOT_API_KEY="your_moonshot_api_key"
```

Or use a `.env` file:

```bash
# .env file
TOGETHER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## Monitoring Reports

### Report Structure

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "api_keys": [
    {
      "provider": "Together AI (Kimi K2)",
      "key_present": true,
      "key_valid": true,
      "error_message": "API key is valid",
      "last_checked": "2024-01-01T00:00:00"
    }
  ],
  "system_health": {
    "cpu_percent": 45.2,
    "memory_percent": 62.1,
    "disk_percent": 54.8,
    "timestamp": "2024-01-01T00:00:00",
    "status": "healthy"
  },
  "issues_found": [],
  "recommendations": [
    "System is healthy - continue monitoring"
  ]
}
```

### Report Storage

Reports are stored in the `monitoring_reports/` directory:
- `monitoring_report_YYYYMMDD_HHMMSS.json` - Timestamped reports
- `latest_report.json` - Most recent report (for quick access)

## GitHub Actions Workflows

### 1. Monitoring Workflow (`.github/workflows/monitoring.yml`)

**Triggers:**
- Hourly (cron schedule)
- Manual (workflow_dispatch)
- On push to main
- On pull requests

**Features:**
- Runs health checks
- Uploads monitoring reports
- Creates issues on critical failures
- Checks for system problems

### 2. Test Workflow (`.github/workflows/tests.yml`)

**Triggers:**
- On push to main/develop
- On pull requests
- Manual trigger

**Features:**
- Runs pytest with coverage
- Tests on Python 3.10, 3.11, 3.12
- Linting with flake8
- Code formatting with black

### 3. Security Workflow (`.github/workflows/security.yml`)

**Triggers:**
- Daily at 2 AM UTC
- Manual trigger
- On push to main

**Features:**
- Dependency vulnerability scanning (safety)
- Code security analysis (bandit)
- Secret scanning (trufflehog)
- API key exposure detection
- Automated security issue creation

## Health Status Levels

### Healthy ✅
- CPU < 80%
- Memory < 80%
- Disk < 80%
- At least one valid API key

### Warning ⚠️
- CPU 80-90%
- Memory 80-90%
- Disk 80-90%

### Critical 🚨
- CPU > 90%
- Memory > 90%
- Disk > 90%
- All API keys invalid
- Critical system failures

## Error Handling & Recovery

### API Key Issues

**Problem:** API key missing or invalid

**Automatic Actions:**
1. Report in monitoring output
2. Generate recommendation
3. Create GitHub issue if critical

**Manual Fix:**
1. Add/update API key in `.env`
2. Restart application
3. Verify with health check

### System Resource Issues

**Problem:** High CPU/Memory/Disk usage

**Automatic Actions:**
1. Flag in health check
2. Categorize severity
3. Recommend actions

**Manual Fix:**
- High CPU: Close unnecessary processes
- High Memory: Restart applications, upgrade RAM
- High Disk: Clean up files, expand storage

## Automated Testing

### Running Tests

```bash
# Run all tests
pytest test_devops_monitor.py -v

# Run with coverage
pytest test_devops_monitor.py -v --cov=devops_monitor --cov-report=term

# Run specific test
pytest test_devops_monitor.py::TestDevOpsMonitor::test_check_system_health_healthy -v
```

### Test Coverage

The test suite covers:
- ✅ API key status checks
- ✅ System health monitoring
- ✅ Issue identification
- ✅ Recommendation generation
- ✅ Report saving and loading
- ✅ API key validation
- ✅ Error handling

## Best Practices

### 1. Regular Monitoring
- Run health checks daily
- Review monitoring reports weekly
- Act on recommendations promptly

### 2. API Key Management
- Rotate keys quarterly
- Use environment variables (never commit keys)
- Validate keys after rotation
- Keep backup provider configured

### 3. System Maintenance
- Monitor resource trends
- Clean up old reports (> 90 days)
- Update dependencies monthly
- Review security scans weekly

### 4. Incident Response
1. Check latest monitoring report
2. Review GitHub issues created by automation
3. Check workflow run logs
4. Apply recommended fixes
5. Verify with another health check

## Integration with Existing Systems

### Adding to Existing Applications

```python
# In your application startup
from devops_monitor import DevOpsMonitor

monitor = DevOpsMonitor()
report = monitor.perform_health_check()

if report.system_health['status'] == 'critical':
    # Handle critical state
    send_alert()

# Get available AI providers
providers = monitor.get_provider_fallback_order()
# Use first available provider
```

### Scheduled Monitoring

```bash
# Add to crontab for hourly checks
0 * * * * cd /path/to/repo && python devops_monitor.py --check >> /var/log/monitoring.log 2>&1
```

## Troubleshooting

### Issue: "No API keys configured"
**Solution:** Add at least one API key to `.env` file

### Issue: "API key is invalid"
**Solution:** 
1. Verify key is correct
2. Check provider account status
3. Regenerate key if needed
4. Test with simple API call

### Issue: "System resources critically high"
**Solution:**
1. Check running processes
2. Restart resource-heavy applications
3. Clear temporary files
4. Consider hardware upgrade

### Issue: "Monitoring reports not generating"
**Solution:**
1. Check write permissions on report directory
2. Verify Python dependencies installed
3. Run with `--report-dir /tmp/reports` for testing

## Advanced Configuration

### Custom Provider Configuration

```python
# Add custom provider to monitoring
monitor.PROVIDERS['CUSTOM_API_KEY'] = {
    'name': 'Custom Provider',
    'test_endpoint': 'https://api.custom.com/v1/test',
    'required': False
}
```

### Custom Health Thresholds

```python
# Modify thresholds in check_system_health method
def check_system_health(self):
    # Custom thresholds
    WARNING_THRESHOLD = 70  # Default: 80
    CRITICAL_THRESHOLD = 85  # Default: 90
    # ... rest of method
```

## Contributing

To add new monitoring features:

1. Add feature to `devops_monitor.py`
2. Add tests to `test_devops_monitor.py`
3. Update this documentation
4. Run full test suite
5. Submit pull request

## Support

- **Documentation:** This file
- **Issues:** GitHub Issues (automatically created for failures)
- **Logs:** Check `monitoring_reports/` directory
- **Workflows:** `.github/workflows/` directory

## Version History

- **v1.0.0** - Initial release
  - API key monitoring
  - System health checks
  - Automated reporting
  - GitHub Actions integration
  - Security scanning

## License

Same license as parent repository.
