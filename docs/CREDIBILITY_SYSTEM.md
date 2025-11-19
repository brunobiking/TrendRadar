# TrendRadar Credibility & Manipulation Detection System

## Overview

The TrendRadar Credibility System is a comprehensive solution for detecting stock manipulation and rating news source credibility. It helps users identify when stocks are being artificially manipulated through coordinated news campaigns, fake sources, or pump & dump schemes.

## Features

### 1. Source Credibility Rating System

Maintains a database of news source credibility ratings organized into four tiers:

- **Tier 1 (95-100)**: Premium sources - Bloomberg, Reuters, WSJ, Financial Times, AP
- **Tier 2 (80-95)**: Reputable sources - CNBC, MarketWatch, Yahoo Finance, Seeking Alpha
- **Tier 3 (40-80)**: Smaller outlets - Medium blogs, smaller financial sites
- **Tier 4 (0-40)**: Unknown/suspicious sources - Social media, unknown blogs

### 2. Manipulation Detection Engine

Implements multiple detection algorithms:

#### A. Sentiment Anomaly Detection
- Tracks baseline sentiment for each ticker over time
- Detects sudden sentiment shifts (>30 points in 24 hours)
- Flags unusual sentiment changes without fundamental justification

#### B. Volume Spike Detection
- Monitors article frequency per ticker
- Flags when >10 articles appear in 1-2 hour window
- Detects coordinated posting patterns

#### C. Content Quality Analysis
Scans for manipulation signals:
- **Urgency words**: "NOW", "URGENT", "LAST CHANCE", "DON'T MISS"
- **Guarantee promises**: "guaranteed", "10x", "moonshot"
- **Excessive emojis**: 🚀 💎 💰 (threshold: 5+)
- **Promotional language**: "EXCLUSIVE", "LIMITED TIME", "VIP ACCESS"
- **FUD tactics**: "CRASH", "DISASTER", "GOING TO ZERO"

#### D. Cross-Reference Validation
- Compares claims across multiple sources
- Flags when only low-credibility sources report on something
- Verifies if multiple reputable sources confirm the news

#### E. Timing Pattern Analysis
- Detects if multiple sources publish simultaneously
- Checks for copy-paste content across different outlets
- Identifies potential bot/coordinated campaigns

### 3. Reality Score Calculator

Combines all detection signals into a unified "Reality Score" (0-100):

- **90-100**: Highly credible, verified by multiple top-tier sources
- **70-89**: Credible, from reputable sources
- **40-69**: Questionable, needs verification
- **20-39**: Likely biased/promotional
- **0-19**: High manipulation risk

## Installation

The credibility system is included in TrendRadar. No additional dependencies are required beyond the standard TrendRadar requirements.

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from src.credibility import SourceAnalyzer, ManipulationDetector, CredibilityScorer

# Initialize components
source_analyzer = SourceAnalyzer()
manipulation_detector = ManipulationDetector()
scorer = CredibilityScorer()

# Analyze a news article
url = "https://www.bloomberg.com/article/tsla-news"
title = "Tesla Reports Record Quarterly Earnings"
content = "Tesla Inc. reported record quarterly earnings..."

# 1. Get source credibility
source_rating = source_analyzer.get_source_rating(url)
print(f"Source: {source_rating['source_name']}")
print(f"Credibility Score: {source_rating['score']}/100")
print(f"Tier: {source_rating['tier']}")

# 2. Analyze content for manipulation
content_analysis = manipulation_detector.analyze_content_quality(content, title)
print(f"Manipulation Score: {content_analysis['manipulation_score']}/100")
print(f"Quality Level: {content_analysis['quality_level']}")
if content_analysis['flags']:
    print(f"Flags: {', '.join(content_analysis['flags'])}")

# 3. Calculate overall reality score
reality_score = scorer.calculate_reality_score(
    source_rating=source_rating,
    content_analysis=content_analysis
)
print(f"\nReality Score: {reality_score['reality_score']}/100")
print(f"Category: {reality_score['category']}")
print("\nRecommendations:")
for rec in reality_score['recommendations']:
    print(f"  - {rec}")
```

### Batch Processing

```python
# Process multiple articles
articles = [
    {
        'id': 'article1',
        'title': 'Market Analysis',
        'url': 'https://www.reuters.com/article1',
        'source_rating': source_analyzer.get_source_rating('https://www.reuters.com/article1'),
        'content_analysis': manipulation_detector.analyze_content_quality('content1')
    },
    # ... more articles
]

# Calculate scores for all articles
results = scorer.batch_calculate_scores(articles)

# Get risk summary
summary = scorer.get_risk_summary(results)
print(f"Total Articles: {summary['total_articles']}")
print(f"Average Score: {summary['average_score']}")
print(f"High Risk Count: {summary['high_risk_count']}")
```

## Configuration

### Source Ratings

Edit `config/source_ratings.json` to customize source ratings:

```json
{
  "tiers": {
    "tier1": {
      "sources": [
        {
          "name": "Your Trusted Source",
          "domain": "trustedsource.com",
          "score": 96,
          "category": "finance",
          "language": "en"
        }
      ]
    }
  }
}
```

### Manipulation Patterns

Edit `config/manipulation_patterns.json` to customize detection patterns:

```json
{
  "urgency_keywords": {
    "weight": 15,
    "keywords": ["NOW", "URGENT", "CUSTOM_KEYWORD"]
  },
  "volume_spike_threshold": {
    "articles_per_hour": 10
  }
}
```

## Advanced Usage

### Volume Spike Detection

```python
from datetime import datetime, timedelta

# Collect article timestamps for a ticker
now = datetime.now()
timestamps = [
    now,
    now + timedelta(minutes=10),
    now + timedelta(minutes=20),
    # ... more timestamps
]

# Detect volume spikes
spike_result = manipulation_detector.detect_volume_spike(timestamps, "AAPL")
if spike_result['detected']:
    print(f"Volume spike detected for AAPL!")
    print(f"Number of spikes: {len(spike_result['spikes'])}")
```

### Coordinated Posting Detection

```python
# Analyze articles for coordinated campaigns
articles = [
    {
        'timestamp': datetime.now(),
        'source': 'blog1.com',
        'title': 'Stock X is going to moon'
    },
    {
        'timestamp': datetime.now() + timedelta(minutes=5),
        'source': 'blog2.com',
        'title': 'Stock X going to the moon'
    },
    # ... more articles
]

coordination_result = manipulation_detector.detect_coordinated_posting(articles)
if coordination_result['detected']:
    print("Coordinated posting detected!")
    for group in coordination_result['coordinated_groups']:
        print(f"Sources: {group['sources']}")
        print(f"Similarity: {group['similarity_score']}")
```

### Sentiment Anomaly Detection

```python
# Track sentiment over time
sentiment_history = [
    {'timestamp': datetime.now() - timedelta(days=2), 'sentiment_score': 50},
    {'timestamp': datetime.now() - timedelta(days=1), 'sentiment_score': 55},
    {'timestamp': datetime.now(), 'sentiment_score': 90},  # Sudden jump
]

anomaly_result = manipulation_detector.detect_sentiment_anomaly(sentiment_history)
if anomaly_result['detected']:
    print("Sentiment anomaly detected!")
    for anomaly in anomaly_result['anomalies']:
        print(f"Change: {anomaly['max_change']} points")
        print(f"Direction: {anomaly['direction']}")
```

## API Reference

### SourceAnalyzer

#### Methods

- `get_source_rating(url: str) -> Dict`: Get credibility rating for a URL
- `get_all_sources() -> List[Dict]`: Get all configured sources
- `get_sources_by_tier(tier: str) -> List[Dict]`: Get sources in a tier
- `get_sources_by_category(category: str) -> List[Dict]`: Get sources by category
- `add_source(name, domain, score, tier, category, language) -> bool`: Add new source
- `update_source_score(domain: str, new_score: int) -> bool`: Update source score
- `analyze_source_distribution(urls: List[str]) -> Dict`: Analyze distribution stats

### ManipulationDetector

#### Methods

- `detect_urgency_language(text: str) -> Dict`: Detect urgency keywords
- `detect_guarantee_promises(text: str) -> Dict`: Detect guarantee promises
- `detect_hyperbolic_language(text: str) -> Dict`: Detect exaggerations
- `detect_promotional_language(text: str) -> Dict`: Detect promotional content
- `detect_fud_language(text: str) -> Dict`: Detect FUD tactics
- `detect_excessive_emojis(text: str) -> Dict`: Detect excessive emoji usage
- `analyze_content_quality(text: str, title: str = "") -> Dict`: Full content analysis
- `detect_volume_spike(timestamps: List[datetime], ticker: str) -> Dict`: Detect spikes
- `detect_coordinated_posting(articles: List[Dict]) -> Dict`: Detect coordination
- `detect_sentiment_anomaly(history: List[Dict]) -> Dict`: Detect sentiment changes

### CredibilityScorer

#### Methods

- `calculate_reality_score(...) -> Dict`: Calculate comprehensive reality score
- `batch_calculate_scores(articles: List[Dict]) -> List[Dict]`: Batch processing
- `get_risk_summary(scores: List[Dict]) -> Dict`: Generate summary statistics

## Examples

### Example 1: Pump & Dump Detection

```python
# Detect potential pump & dump scheme
url = "https://unknown-blog.com/stock-tip"
content = """
URGENT! BUY NOW! GUARANTEED 10X returns! 🚀🚀🚀
This stock is going TO THE MOON! Don't miss this LAST CHANCE!
MASSIVE GAINS ahead! ACT FAST! 💰💰💰
"""

source_rating = source_analyzer.get_source_rating(url)
content_analysis = manipulation_detector.analyze_content_quality(content)

reality_score = scorer.calculate_reality_score(
    source_rating=source_rating,
    content_analysis=content_analysis
)

# Expected: Low reality score (0-19), high_risk category
print(f"Reality Score: {reality_score['reality_score']}")  # e.g., 12
print(f"Category: {reality_score['category']}")  # "high_risk"
```

### Example 2: Credible News Verification

```python
# Verify credible news from reputable source
url = "https://www.bloomberg.com/news/articles/2024-01-15/company-earnings"
content = """
Company XYZ reported quarterly earnings that exceeded analyst expectations.
Revenue increased 15% year-over-year to $2.5 billion. The company cited
strong demand in international markets as a key driver of growth.
"""

source_rating = source_analyzer.get_source_rating(url)
content_analysis = manipulation_detector.analyze_content_quality(content)

reality_score = scorer.calculate_reality_score(
    source_rating=source_rating,
    content_analysis=content_analysis
)

# Expected: High reality score (90-100), highly_credible category
print(f"Reality Score: {reality_score['reality_score']}")  # e.g., 96
print(f"Category: {reality_score['category']}")  # "highly_credible"
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test module
python -m unittest tests.test_source_analyzer -v
python -m unittest tests.test_manipulation_detector -v
python -m unittest tests.test_scoring -v
```

## Best Practices

1. **Always cross-reference**: Don't rely on a single source, even if highly rated
2. **Monitor patterns**: Look for volume spikes and coordinated campaigns
3. **Update ratings**: Keep source ratings current based on performance
4. **Use full context**: Combine source, content, and timing analysis
5. **Set thresholds**: Customize detection thresholds for your use case

## Troubleshooting

### Issue: Source not recognized
**Solution**: Add the source to `config/source_ratings.json`

### Issue: False positives in emoji detection
**Solution**: Adjust `emoji_patterns.threshold` in `config/manipulation_patterns.json`

### Issue: Missing volume spikes
**Solution**: Lower `volume_spike_threshold.articles_per_hour` in config

## Contributing

To add new detection patterns:

1. Edit `config/manipulation_patterns.json`
2. Add corresponding detection method in `ManipulationDetector`
3. Update tests in `tests/test_manipulation_detector.py`
4. Update documentation

## License

Same as TrendRadar main project (GPL-3.0)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for usage examples
