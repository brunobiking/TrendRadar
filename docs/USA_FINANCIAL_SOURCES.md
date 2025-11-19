# USA Financial Market News Sources Integration

## Overview

TrendRadar now supports 5 major USA financial news sources focused on publicly traded companies and stock market news. All sources are in English and can be individually enabled or disabled.

## Supported Sources

### 1. Yahoo Finance - Trending Tickers
- **Data Source**: RSS feeds
- **Update Frequency**: Real-time
- **Content**: Market news, trending stocks, top gainers/losers

### 2. Finviz - Market News Aggregator  
- **Data Source**: HTML scraping
- **Update Frequency**: Real-time
- **Content**: Aggregated market news from multiple sources

### 3. MarketWatch - Breaking Market News
- **Data Source**: RSS feeds
- **Update Frequency**: Real-time
- **Content**: Breaking news, market analysis, economic indicators

### 4. Seeking Alpha - Market Analysis
- **Data Source**: RSS/Atom feeds
- **Update Frequency**: Multiple times per day
- **Content**: Market news, analyst ratings, earnings reports

### 5. Benzinga - Real-time Financial News
- **Data Source**: RSS feeds
- **Update Frequency**: Real-time
- **Content**: Breaking news, analyst upgrades/downgrades

## Features

### Automatic Ticker Extraction
Extracts stock ticker symbols from headlines:
- `$AAPL` - Dollar sign format
- `(NASDAQ:TSLA)` - Exchange format
- `NVDA` - Standalone ticker

### Financial Keywords Filtering
Use `config/frequency_words_financial.txt` to filter by:
- Stock terms (stocks, shares, equity, trading)
- Market movements (surge, plunge, rally, crash)
- Financial events (earnings, dividend, IPO, merger)
- Major companies (Apple, Tesla, NVIDIA, Microsoft)
- Indices (S&P 500, Dow Jones, NASDAQ)

### Enable/Disable Controls
Each source can be independently controlled via config.yaml

## Quick Start

1. Sources are pre-configured in `config/config.yaml`
2. Set `enabled: true/false` for each source
3. Use financial keywords in `frequency_words_financial.txt` or standard `frequency_words.txt`
4. Run TrendRadar as usual

## Configuration Example

```yaml
platforms:
  - id: "yahoo-finance-trending"
    name: "Yahoo Finance Trending"
    enabled: true
    language: "en"
    category: "finance"
    config:
      data_type: ["trending", "gainers", "losers"]
```

## Troubleshooting

### No Financial News Showing Up
1. Check that sources are enabled in config.yaml
2. Verify frequency_words.txt contains financial keywords
3. Check console for fetch errors
4. Ensure network connectivity

### RSS Feed Errors
- HTTP 403: Site may be blocking your IP
- Timeouts: Try using a proxy
- Rate limiting: Increase request_interval in config.yaml

## Data Format

Financial news follows standard TrendRadar format with additional fields:
- `ticker`: Stock ticker symbol (e.g., "TSLA")
- `category`: News category (e.g., "earnings", "market_news")
- `source`: Source name (e.g., "Yahoo Finance")

## License

GPL-3.0 (same as TrendRadar)
