# API Reference

**⏱️ Time Estimate: 10 minutes to understand**

Technical reference for TrendRadar's dependencies, external services, and data sources.

## Table of Contents
- [Overview](#overview)
- [Python Dependencies](#python-dependencies)
- [External Services](#external-services)
- [API Keys & Authentication](#api-keys--authentication)
- [Data Sources](#data-sources)
- [Rate Limits](#rate-limits)
- [MCP Protocol](#mcp-protocol)
- [Development](#development)

---

## Overview

TrendRadar is designed to be **free and open** with minimal external dependencies:

✅ **No paid subscriptions required**  
✅ **No API keys needed for news data**  
✅ **Self-hostable notification services**  
✅ **All dependencies are free and open-source**  

---

## Python Dependencies

TrendRadar requires Python 3.10+ with the following packages:

### Core Dependencies

#### requests (≥2.32.5, <3.0.0)

**Purpose:** HTTP client for making API requests to news sources and webhooks.

**Usage in TrendRadar:**
- Fetching news data from newsnow API
- Sending webhook notifications (Telegram, WeWork, Feishu, DingTalk)
- Sending email via SMTP

**Installation:**
```bash
pip install "requests>=2.32.5,<3.0.0"
```

**License:** Apache 2.0

**Documentation:** https://requests.readthedocs.io/

---

#### pytz (≥2025.2, <2026.0)

**Purpose:** Timezone library for accurate time handling.

**Usage in TrendRadar:**
- Converting timestamps to Beijing time (Asia/Shanghai)
- Push time window calculations
- Logging timestamps
- News publication time formatting

**Installation:**
```bash
pip install "pytz>=2025.2,<2026.0"
```

**License:** MIT

**Documentation:** https://pythonhosted.org/pytz/

**Example usage:**
```python
import pytz
from datetime import datetime

beijing_tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(beijing_tz)
```

---

#### PyYAML (≥6.0.3, <7.0.0)

**Purpose:** YAML parser for configuration files.

**Usage in TrendRadar:**
- Loading `config/config.yaml`
- Parsing configuration settings
- Validating config structure

**Installation:**
```bash
pip install "PyYAML>=6.0.3,<7.0.0"
```

**License:** MIT

**Documentation:** https://pyyaml.org/

**Example usage:**
```python
import yaml

with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
```

---

#### fastmcp (≥2.12.0, <2.14.0)

**Purpose:** Model Context Protocol (MCP) server framework for AI integration.

**Usage in TrendRadar:**
- MCP server implementation (`mcp_server/server.py`)
- Exposing news data to AI clients
- Handling AI tool calls
- WebSocket and HTTP transport

**Installation:**
```bash
pip install "fastmcp>=2.12.0,<2.14.0"
```

**License:** MIT

**Documentation:** https://github.com/jlowin/fastmcp

**MCP Features:**
- 13 AI analysis tools
- Natural language query interface
- Conversational trend analysis

**Note:** Only required for AI analysis features, not needed for basic news aggregation.

---

#### websockets (≥13.0, <14.0)

**Purpose:** WebSocket client and server library.

**Usage in TrendRadar:**
- MCP WebSocket transport mode
- Real-time bidirectional communication with AI clients
- Streaming responses

**Installation:**
```bash
pip install "websockets>=13.0,<14.0"
```

**License:** BSD-3-Clause

**Documentation:** https://websockets.readthedocs.io/

**Note:** Only required for MCP features, not for core functionality.

---

### Dependency Management

**requirements.txt:**
```txt
requests>=2.32.5,<3.0.0
pytz>=2025.2,<2026.0
PyYAML>=6.0.3,<7.0.0
fastmcp>=2.12.0,<2.14.0
websockets>=13.0,<14.0
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Version constraints rationale:**
- **Lower bound:** Ensures required features are available
- **Upper bound:** Prevents breaking changes from future major versions

---

## External Services

TrendRadar integrates with several external services, all available for free.

### 1. NewsNow API (Primary Data Source)

**Service:** News aggregation API  
**URL:** https://newsnow.busiyi.world/  
**Cost:** Free  
**Authentication:** None required  

**What it provides:**
- Real-time trending news from 35+ platforms
- Chinese news sources (Zhihu, Weibo, Baidu, etc.)
- USA financial markets (Yahoo Finance, MarketWatch, etc.)
- Ranking data and metadata

**API Endpoint:**
```
https://newsnow.busiyi.world/api/data
```

**Response format:** JSON

**Example response structure:**
```json
{
  "zhihu": [
    {
      "title": "News title",
      "url": "https://...",
      "rank": 1,
      "timestamp": "2025-01-15T10:30:00Z"
    }
  ],
  "weibo": [...]
}
```

**Rate limits:** Not officially documented, but TrendRadar uses 1-second intervals between requests.

**Attribution:** Thanks to [ourongxing/newsnow](https://github.com/ourongxing/newsnow) project.

---

### 2. GitHub Actions (Execution Platform)

**Service:** CI/CD and automation platform  
**URL:** https://github.com/features/actions  
**Cost:** Free for public repositories (2,000 minutes/month)  
**Authentication:** GitHub account  

**What it provides:**
- Automated workflow execution
- Scheduled cron jobs
- Free compute resources
- Version control integration

**Usage in TrendRadar:**
- `.github/workflows/crawler.yml` defines automation
- Runs on schedule (default: hourly)
- Commits output to repository
- Deploys to GitHub Pages

**Free tier limits:**
- 2,000 minutes/month for private repos
- Unlimited for public repos
- 500 MB storage for artifacts

---

### 3. GitHub Pages (Web Hosting)

**Service:** Static site hosting  
**URL:** https://pages.github.com/  
**Cost:** Free  
**Authentication:** GitHub account  

**What it provides:**
- Free static website hosting
- Automatic deployment from repository
- Custom domain support
- HTTPS enabled

**Usage in TrendRadar:**
- Hosts generated HTML reports
- Mobile-responsive news dashboard
- Direct links to news sources
- Image export functionality

**Site URL format:**
```
https://USERNAME.github.io/TrendRadar/
```

---

### 4. Notification Services

All notification platforms are free for basic use:

#### Telegram Bot API

**Service:** Bot platform  
**URL:** https://core.telegram.org/bots  
**Cost:** Free  
**Authentication:** Bot token from @BotFather  

**Limits:**
- 30 messages/second per bot
- 20 messages/minute per group

---

#### WeWork Bot API

**Service:** Enterprise messaging  
**URL:** https://work.weixin.qq.com/  
**Cost:** Free  
**Authentication:** Webhook URL  

**Limits:**
- 20 messages/minute per webhook

---

#### Feishu Bot API

**Service:** Enterprise collaboration  
**URL:** https://www.feishu.cn/  
**Cost:** Free  
**Authentication:** Webhook URL  

**Limits:**
- Message size: ~30KB per message

---

#### DingTalk Bot API

**Service:** Enterprise communication  
**URL:** https://www.dingtalk.com/  
**Cost:** Free  
**Authentication:** Webhook URL  

**Limits:**
- 20KB per message
- Security keywords required

---

#### Email (SMTP)

**Service:** Various providers  
**Cost:** Free with existing email account  
**Authentication:** App password or authorization code  

**Supported providers:**
- Gmail, QQ Mail, Outlook, Hotmail
- 163, 126, Sina, Sohu Mail
- Any SMTP-compatible service

**Limits:** Provider-dependent (typically 500-2000 emails/day for free tiers)

---

#### ntfy

**Service:** Open-source notification service  
**URL:** https://ntfy.sh/  
**Cost:** Free (public service) or self-hosted  
**Authentication:** None (public topics) or token (private topics)  

**Public service limits:**
- 250 messages/day per topic
- No account required

**Self-hosted:** Unlimited, full control

**License:** Apache 2.0 + GPLv2

---

## API Keys & Authentication

### No Keys Required for Core Features

**TrendRadar's core news aggregation requires NO API keys:**

✅ News data from NewsNow API - **No authentication**  
✅ Trend calculation and analysis - **Runs locally**  
✅ Report generation - **Runs locally**  
✅ GitHub Actions execution - **Built-in GitHub auth**  

### Keys Required ONLY for Notifications

You only need credentials for **notification channels you choose to use**:

| Service | Required Credentials | Where to Get |
|---------|---------------------|--------------|
| Telegram | Bot Token + Chat ID | @BotFather in Telegram |
| WeWork | Webhook URL | Group settings in app |
| Feishu | Webhook URL | Bot Builder website |
| DingTalk | Webhook URL | PC client bot settings |
| Email | Email + App Password | Email provider settings |
| ntfy | Topic name (+ optional token) | Choose your own / ntfy.sh |

**All notification services above are free!**

### Optional Services

**MCP AI Analysis:**
- **No keys required** for MCP server itself
- **AI model API key required** to use AI features:
  - OpenAI API (ChatGPT, Claude via OpenAI-compatible)
  - Anthropic API (Claude)
  - Local AI models (free, open-source)
  - 302.AI ($1 free credit for new users)

**See:** [README-Cherry-Studio.md](../README-Cherry-Studio.md) for AI setup.

---

## Data Sources

### News Platforms Monitored

TrendRadar aggregates data from 35+ platforms:

**Chinese News Sources (11):**
1. **Toutiao** (今日头条) - General news
2. **Baidu Hot Search** (百度热搜) - Search trends
3. **Zhihu** (知乎) - Q&A platform trends
4. **Weibo** (微博) - Social media trends
5. **Douyin** (抖音) - Short video trends
6. **Bilibili** (哔哩哔哩) - Video platform trends
7. **Tieba** (贴吧) - Forum trends
8. **Wallstreetcn** (华尔街见闻) - Financial news
9. **Yicai** (财联社) - Financial news
10. **Thepaper** (澎湃新闻) - News media
11. **Ifeng** (凤凰网) - News portal

**USA Financial Sources (5):**
1. **Yahoo Finance** - Trending tickers, gainers, losers
2. **MarketWatch** - Breaking market news
3. **Seeking Alpha** - Market analysis, earnings
4. **Benzinga** - Real-time financial news
5. **Finviz** - Market news aggregator

**Data updates:** Every 5-10 minutes on source platforms

**See:** [USA_FINANCIAL_SOURCES.md](USA_FINANCIAL_SOURCES.md) for detailed documentation.

---

### Adding Custom Platforms

TrendRadar supports any platform available in the NewsNow API.

**To find available platforms:**
1. Visit: https://newsnow.busiyi.world/
2. Click "More" (更多) to see all sources
3. Check source code: https://github.com/ourongxing/newsnow/tree/main/server/sources

**Add to `config/config.yaml`:**
```yaml
platforms:
  - id: "platform-id"  # From NewsNow source code
    name: "Display Name"
    enabled: true  # Optional: default true
```

**Example - Adding a new platform:**
```yaml
platforms:
  # ... existing platforms ...
  
  - id: "36kr"
    name: "36Kr Tech News"
    enabled: true
```

---

## Rate Limits

### NewsNow API

**Official limits:** Not publicly documented

**TrendRadar defaults:**
- Request interval: 1000ms (1 second) between platforms
- Configurable in `config/config.yaml`:
  ```yaml
  crawler:
    request_interval: 1000  # milliseconds
  ```

**Recommended settings:**
- Light use: 1000ms (default)
- Moderate: 2000ms
- Heavy use: 3000-5000ms

**Signs of rate limiting:**
- HTTP 429 errors
- Empty responses
- Connection timeouts

**Solutions:**
- Increase `request_interval`
- Reduce number of monitored platforms
- Decrease execution frequency

---

### Notification Services

| Service | Rate Limit | TrendRadar Handling |
|---------|------------|---------------------|
| Telegram | 30 msg/sec, 20 msg/min per group | Batch splitting |
| WeWork | 20 msg/min | Batch splitting |
| Feishu | ~30KB per message | Message chunking |
| DingTalk | 20KB per message | Message chunking |
| Email | Provider-dependent (500-2000/day) | Single combined email |
| ntfy | 250 msg/day (public) | No batching needed |

**Batch configuration:**
```yaml
notification:
  message_batch_size: 4000  # Telegram/WeWork
  dingtalk_batch_size: 20000
  feishu_batch_size: 29000
  batch_send_interval: 3  # seconds between batches
```

---

## MCP Protocol

### Model Context Protocol (MCP)

**Version:** 1.0  
**Specification:** https://modelcontextprotocol.io/  
**License:** Open standard  

**What is MCP?**
A protocol for connecting AI assistants to external data sources and tools.

**TrendRadar MCP Implementation:**
- Server located in `mcp_server/server.py`
- Exposes 13 analysis tools
- Supports both HTTP and STDIO transport
- Compatible with Claude Desktop, Cursor, Cherry Studio, etc.

---

### Available Tools

TrendRadar's MCP server provides these tools to AI clients:

#### Basic Query Tools

1. **get_latest_news**
   - Get recent news from output folder
   - Parameters: platforms, limit

2. **get_news_by_date**
   - Get news for specific date
   - Parameters: date (YYYY-MM-DD), platforms

3. **get_trending_topics**
   - Get trending topics overview
   - Parameters: start_date, end_date, platforms

#### Search Tools

4. **search_news**
   - Search news by keywords
   - Parameters: query, date_range, platforms

5. **search_related_news_history**
   - Find related historical news
   - Parameters: keywords, lookback_days

#### Analysis Tools

6. **analyze_topic_trend**
   - Analyze topic popularity over time
   - Parameters: topic, date_range

7. **analyze_data_insights**
   - Platform comparison and statistics
   - Parameters: date_range, platforms

8. **analyze_sentiment**
   - Sentiment analysis of news
   - Parameters: topics, date_range

9. **find_similar_news**
   - Find similar news items
   - Parameters: reference_news_id

10. **generate_summary_report**
    - Generate summary of trending topics
    - Parameters: date_range, format

#### System Tools

11. **get_current_config**
    - View current TrendRadar configuration

12. **get_system_status**
    - Check system status and data availability

13. **trigger_crawl**
    - Manually trigger news crawling

---

### MCP Transport Modes

#### STDIO Transport (Recommended)

**Best for:** Desktop AI clients (Claude Desktop, Cursor)

**Configuration:**
```json
{
  "command": "uv",
  "args": [
    "--directory",
    "/path/to/TrendRadar",
    "run",
    "python",
    "-m",
    "mcp_server.server"
  ]
}
```

**Pros:**
- Direct process communication
- No network setup
- More secure

---

#### HTTP Transport

**Best for:** Web-based clients, remote access

**Start server:**
```bash
uv run python -m mcp_server.server --transport http --port 3333
```

**Configuration:**
```json
{
  "url": "http://localhost:3333/mcp"
}
```

**Pros:**
- Works over network
- Multiple clients can connect
- Browser-based debugging

---

## Development

### Project Structure

```
TrendRadar/
├── main.py                 # Main execution script
├── config/
│   ├── config.yaml         # Configuration file
│   └── frequency_words.txt # Keyword filters
├── src/                    # Core source code
│   ├── crawler/            # News fetching
│   ├── analyzer/           # Trend analysis
│   ├── notifier/           # Notification sending
│   └── utils/              # Helper functions
├── mcp_server/             # MCP server implementation
│   ├── server.py           # MCP server
│   └── tools/              # AI analysis tools
├── output/                 # Generated reports
├── docs/                   # Documentation
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

---

### Adding New Dependencies

**When adding a new package:**

1. **Update requirements.txt:**
   ```txt
   new-package>=1.0.0,<2.0.0
   ```

2. **Specify version constraints:**
   - Lower bound: First version with required features
   - Upper bound: Next major version (may have breaking changes)

3. **Test compatibility:**
   ```bash
   pip install -r requirements.txt
   python -m pytest tests/
   ```

4. **Update this documentation:**
   - Add to [Python Dependencies](#python-dependencies)
   - Explain usage
   - Provide license info

---

### API Response Caching

TrendRadar doesn't implement caching by default to ensure fresh data.

**To add caching (custom modification):**

```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_platform_cached(platform_id, ttl=300):
    """Cache API responses for 5 minutes"""
    return fetch_platform(platform_id)
```

**Consider caching for:**
- Reducing API calls during development
- Backup data source when API is down
- Offline testing

---

### Testing

**Run test suite:**
```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_crawler.py

# Run with coverage
python -m pytest --cov=src tests/
```

**Test structure:**
```
tests/
├── test_crawler.py        # Crawler tests
├── test_analyzer.py       # Analysis tests
├── test_notifier.py       # Notification tests
├── test_config.py         # Configuration tests
└── fixtures/              # Test data
```

---

### Environment Variables

**All configuration can be overridden via environment variables:**

```bash
# Core settings
export ENABLE_CRAWLER=true
export ENABLE_NOTIFICATION=true
export REPORT_MODE=daily

# Notification channels
export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id

# Docker-specific
export CRON_SCHEDULE="*/30 * * * *"
export RUN_MODE=cron
```

**Priority:** `Environment Variables > config.yaml > Defaults`

**See:** [CONFIGURATION.md](CONFIGURATION.md#environment-variable-override) for full list.

---

### Docker Image

**Official image:** `wantcat/trendradar:latest`

**Multi-architecture support:**
- linux/amd64 (x86_64)
- linux/arm64 (Apple Silicon, ARM64 servers)
- linux/arm/v7 (Raspberry Pi)

**Base image:** python:3.10-slim

**Installed software:**
- Python 3.10
- TrendRadar and dependencies
- Cron (for scheduling)
- Timezone data (for Beijing time)

**Build locally:**
```bash
docker build -t trendradar:local .
```

---

## Version History

### Current Version: v3.0.5

**Major features:**
- Multi-platform news aggregation (35+ sources)
- Three push modes (daily, current, incremental)
- Six notification channels
- Push time window control
- MCP AI analysis (v1.0.2)
- USA financial sources
- Docker deployment
- GitHub Actions automation

**Changelog:** See [README-EN.md](../README-EN.md#-changelog)

---

## License

**TrendRadar:** GPL-3.0 License

**Dependencies:**
- requests: Apache 2.0
- pytz: MIT
- PyYAML: MIT
- fastmcp: MIT
- websockets: BSD-3-Clause

**Data source:**
- NewsNow API: Attribution required

**All components are open-source and free to use.**

---

## Contributing

Want to improve TrendRadar's integrations?

**Areas for contribution:**
- Additional notification channels
- New news platform integrations
- Enhanced AI analysis tools
- Performance optimizations
- Documentation improvements

**See:** [CONTRIBUTING.md](../CONTRIBUTING.md) (if exists) or open an issue to discuss.

---

## Related Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Configuration Guide](CONFIGURATION.md)** - All configuration options
- **[Deployment Guide](DEPLOYMENT.md)** - Deployment methods
- **[Troubleshooting](TROUBLESHOOTING.md)** - Problem solving

---

[← Back to Troubleshooting](TROUBLESHOOTING.md) | [Back to README →](../README-EN.md)
