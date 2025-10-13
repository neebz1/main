# 🔍 API Integration Monitor Guide

## Overview

The API Integration Monitor provides comprehensive monitoring for all AI providers used in your music production suite:

- **OpenRouter** - Embeddings for semantic search
- **Google Gemini** - Live AI assistant and Logic Pro plugin
- **Together AI (Kimi K2)** - Cost-effective AI chat
- **Anthropic (Claude)** - High-quality AI responses
- **OpenAI (GPT-4)** - Industry standard AI
- **Moonshot AI** - Ready for future integration

## Features

### 🏥 Health Monitoring
- Real-time API connectivity checks
- Response time tracking
- Error rate monitoring
- Status alerts (Healthy/Degraded/Failed)

### 💰 Cost Tracking
- Token usage tracking per provider
- Estimated cost calculations
- Cost optimization suggestions
- Usage reports

### 🔄 Automatic Failover
- Detects failed APIs
- Suggests alternative providers
- Priority-based failover: Together AI → Anthropic → OpenAI → Gemini → OpenRouter

### 📊 Detailed Metrics
- Success/error rates
- Response time statistics
- Request counts
- Last check timestamps

## Quick Start

### 1. Install Dependencies

```bash
pip install httpx python-dotenv
```

### 2. Set Up API Keys

Create or update your `.env` file with API keys:

```bash
# OpenRouter (for semantic search)
OPENROUTER_API_KEY=your_openrouter_key

# Google Gemini (for live AI)
GOOGLE_API_KEY=your_google_key

# Together AI (Kimi K2 - most affordable)
TOGETHER_API_KEY=your_together_key

# Anthropic Claude (optional)
ANTHROPIC_API_KEY=your_anthropic_key

# OpenAI GPT-4 (optional)
OPENAI_API_KEY=your_openai_key

# Moonshot AI (future)
MOONSHOT_API_KEY=your_moonshot_key
```

### 3. Run Monitoring

#### Option A: Standalone Script

```bash
./monitor_apis.sh
```

Or directly:

```bash
python3 api_monitor.py
```

#### Option B: Via API Server

Start the API server:

```bash
cd CursorDocsIndex
python api_server.py
```

Then access monitoring endpoints:

- **Full Report**: http://localhost:8000/api/monitor
- **Quick Status**: http://localhost:8000/api/status

## Usage Examples

### 1. Check All Providers

```bash
python3 api_monitor.py
```

**Output:**
```
🔍 API Integration Monitor Starting...
============================================================

📊 Checking all API providers...

============================================================
📈 STATUS REPORT
============================================================

✅ Healthy: 3
⚠️  Degraded: 1
❌ Failed: 0
❓ Unknown: 2

💰 Total Cost: $2.45
🎯 Total Tokens: 125,000
📊 Total Requests: 450

============================================================
🔧 PROVIDER DETAILS
============================================================

✅ Together AI (Kimi K2)
   Status: healthy
   Response Time: 234ms
   Success Rate: 99.2%
   Error Rate: 0.8%
   Cost: $0.06

✅ Google Gemini
   Status: healthy
   Response Time: 189ms
   Success Rate: 100.0%
   Error Rate: 0.0%
   Cost: $0.12

⚠️  OpenAI (GPT-4)
   Status: degraded
   Response Time: 1250ms
   Success Rate: 95.3%
   Error Rate: 4.7%
   Cost: $2.15
   Last Error: Rate limit exceeded

❓ Moonshot AI
   Status: unknown
   Last Error: API key not configured

============================================================
💡 COST OPTIMIZATION SUGGESTIONS
============================================================

💡 OpenAI (GPT-4) has cost $2.15. Consider switching to 
   Together AI (Kimi K2) for 80% cost savings.

⚡ OpenAI (GPT-4) has slow response time (1250ms). 
   Consider using a faster provider for better UX.
```

### 2. Integrate with Your Application

```python
from api_monitor import APIMonitor, APIProvider

# Initialize monitor
monitor = APIMonitor()

# Check if provider is healthy
healthy_providers = monitor.get_healthy_providers()

if APIProvider.TOGETHER_AI.value in healthy_providers:
    # Use Together AI
    pass
else:
    # Use failover
    failover = monitor.get_failover_provider(APIProvider.TOGETHER_AI.value)
    print(f"Together AI failed, using {failover} instead")

# Track usage
monitor.track_usage(APIProvider.TOGETHER_AI.value, tokens=500)

# Get report
report = monitor.get_status_report()
print(f"Total cost: ${report['summary']['total_cost_usd']}")
```

### 3. Continuous Monitoring

Set up a cron job to run monitoring every hour:

```bash
# Edit crontab
crontab -e

# Add this line (runs every hour)
0 * * * * cd /path/to/your/project && ./monitor_apis.sh >> api_monitor.log 2>&1
```

### 4. API Endpoint Usage

```bash
# Quick status check
curl http://localhost:8000/api/status

# Full monitoring report
curl http://localhost:8000/api/monitor

# Pretty print with jq
curl -s http://localhost:8000/api/monitor | jq '.'
```

## Understanding Metrics

### Status Types

- **Healthy** ✅ - API is responding normally, low error rate
- **Degraded** ⚠️ - API is responding but with high errors or rate limits
- **Failed** ❌ - API is not responding or authentication failed
- **Unknown** ❓ - API key not configured or never checked

### Response Time Guidelines

- **< 500ms**: Excellent ⚡
- **500ms - 1s**: Good ✅
- **1s - 3s**: Acceptable ⚠️
- **> 3s**: Slow 🐌

### Error Rate Thresholds

- **< 1%**: Excellent ✅
- **1% - 5%**: Good ⚠️
- **5% - 10%**: Concerning 🟡
- **> 10%**: Critical 🚨

### Cost Comparison (per 1K tokens)

| Provider | Cost | Use Case |
|----------|------|----------|
| Together AI | $0.0005 | 🌟 Best value - Use for most tasks |
| Google Gemini | $0.001 | Fast responses, good quality |
| OpenRouter | $0.002 | Embeddings, semantic search |
| Moonshot AI | $0.003 | Alternative option |
| Anthropic | $0.008 | High-quality, thoughtful responses |
| OpenAI | $0.01 | Industry standard, reliable |

## Alerts and Notifications

The monitor generates three types of alerts:

### 1. Critical Alerts 🚨
- API completely down
- Authentication failures
- Network errors

### 2. Warning Alerts ⚠️
- High error rates (> 10%)
- Slow response times (> 5s)
- Rate limiting issues

### 3. Info Alerts 💡
- Cost optimization suggestions
- Performance recommendations
- Failover suggestions

## Failover Strategy

The monitor implements smart failover with this priority:

1. **Together AI (Kimi K2)** - Most cost-effective
2. **Anthropic (Claude)** - High quality
3. **OpenAI (GPT-4)** - Reliable standard
4. **Google Gemini** - Fast and capable
5. **OpenRouter** - Flexible routing

Example failover flow:
```
Primary: Together AI ❌ Failed
  ↓
Failover: Anthropic ✅ Healthy
  → Use Anthropic
```

## Best Practices

### 1. Regular Monitoring

Run monitoring at least daily to catch issues early:

```bash
# Daily at 9 AM
0 9 * * * cd /path/to/project && ./monitor_apis.sh
```

### 2. Set Alerts

Monitor the `api_monitor.log` file for alerts:

```bash
# Alert on failures
tail -f api_monitor.log | grep -E "🚨|❌"
```

### 3. Cost Management

- Review cost reports weekly
- Implement the optimization suggestions
- Use Together AI for most tasks (80% cheaper than OpenAI)
- Reserve expensive providers (OpenAI, Anthropic) for critical tasks

### 4. Error Handling

Implement retry logic with exponential backoff:

```python
import time

def call_api_with_retry(provider, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Check if provider is healthy
            if monitor.metrics[provider].status == "healthy":
                return call_api(provider)
            else:
                # Use failover
                failover = monitor.get_failover_provider(provider)
                return call_api(failover)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
```

## Metrics Storage

Metrics are stored in `api_metrics.json`:

```json
{
  "together_ai": {
    "provider": "together_ai",
    "status": "healthy",
    "response_time_ms": 234.5,
    "error_count": 2,
    "success_count": 248,
    "total_requests": 250,
    "last_check": "2025-01-15T10:30:00",
    "estimated_cost_usd": 0.0625,
    "tokens_used": 125000
  }
}
```

## Troubleshooting

### Issue: "API key not configured"

**Solution:** Add the API key to your `.env` file:
```bash
echo "PROVIDER_API_KEY=your_key" >> .env
```

### Issue: "Connection timeout"

**Solution:** 
1. Check your internet connection
2. Verify the provider's status page
3. Try increasing the timeout in `api_monitor.py`

### Issue: "Rate limit exceeded"

**Solution:**
1. Wait for the rate limit to reset
2. Use a different provider temporarily
3. Consider upgrading your API plan

### Issue: High costs

**Solution:**
1. Switch to Together AI (Kimi K2) - 80% cheaper
2. Implement request caching
3. Reduce max_tokens in responses
4. Use streaming for long responses

## API Reference

### APIMonitor Class

```python
class APIMonitor:
    def __init__(self, metrics_file: str = "api_metrics.json")
    
    async def check_provider_health(self, provider: APIProvider) -> APIMetrics
    async def check_all_providers(self) -> Dict[str, APIMetrics]
    
    def get_healthy_providers(self) -> List[str]
    def get_failover_provider(self, primary_provider: str) -> Optional[str]
    
    def track_usage(self, provider: str, tokens: int)
    
    def get_status_report(self) -> Dict[str, Any]
    def get_cost_optimization_suggestions(self) -> List[str]
    def alert_on_failures(self) -> List[str]
```

### API Endpoints

**GET /api/monitor**
- Returns comprehensive monitoring report
- Includes alerts and optimization suggestions
- Checks all providers in real-time

**GET /api/status**
- Quick health check
- Returns list of healthy providers
- Lightweight, no detailed checks

## Advanced Usage

### Custom Monitoring Loop

```python
import asyncio
from api_monitor import APIMonitor

async def monitor_loop(interval=3600):
    """Run monitoring every hour"""
    monitor = APIMonitor()
    
    while True:
        print("🔍 Checking APIs...")
        await monitor.check_all_providers()
        
        # Check for failures
        alerts = monitor.alert_on_failures()
        for alert in alerts:
            print(alert)
            # Send notification (email, Slack, etc.)
        
        # Wait for next check
        await asyncio.sleep(interval)

# Run
asyncio.run(monitor_loop())
```

### Integration with Logging

```python
import logging
from api_monitor import APIMonitor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_monitor.log'),
        logging.StreamHandler()
    ]
)

monitor = APIMonitor()

# Log metrics
report = monitor.get_status_report()
logging.info(f"Healthy providers: {report['summary']['healthy_providers']}")
logging.info(f"Total cost: ${report['summary']['total_cost_usd']}")
```

## Support

For issues or questions:
1. Check this guide
2. Review the `api_monitor.log` file
3. Check provider status pages
4. Review your API key configuration

---

**Built with ❤️ for the AI Music Production Suite**

🎵 Keep your APIs healthy and your music flowing! 🎚️
