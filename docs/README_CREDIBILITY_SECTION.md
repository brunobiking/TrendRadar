# Credibility & Manipulation Detection System (New Feature)

## 🛡️ Protect Yourself from Stock Manipulation

TrendRadar now includes a comprehensive credibility system that helps you identify when stocks are being artificially manipulated through coordinated news campaigns, fake sources, or pump & dump schemes.

### Key Features

✅ **Source Credibility Rating** - Automatically rates news sources on a 0-100 scale  
✅ **Manipulation Detection** - Identifies urgency tactics, false guarantees, and hype  
✅ **Pump & Dump Detection** - Monitors coordinated positive sentiment + volume spikes  
✅ **FUD Detection** - Identifies coordinated negative fear campaigns  
✅ **Reality Score** - Single unified score (0-100) for overall credibility  
✅ **Actionable Recommendations** - Clear guidance on what to do  

### Quick Example

```python
from src.credibility import SourceAnalyzer, ManipulationDetector, CredibilityScorer

# Initialize
analyzer = SourceAnalyzer()
detector = ManipulationDetector()
scorer = CredibilityScorer()

# Analyze suspicious article
url = "https://unknown-blog.com/stock-tip"
content = "URGENT! BUY NOW! GUARANTEED 10X returns! 🚀🚀🚀"

source_rating = analyzer.get_source_rating(url)
content_analysis = detector.analyze_content_quality(content)
reality_score = scorer.calculate_reality_score(
    source_rating=source_rating,
    content_analysis=content_analysis
)

print(f"Reality Score: {reality_score['reality_score']}/100")
# Output: Reality Score: 15/100 (HIGH MANIPULATION RISK)
```

### Reality Score Ranges

| Score | Category | Action Required |
|-------|----------|----------------|
| 90-100 | ✅ Highly Credible | Safe to use for decision-making |
| 70-89 | ✅ Credible | Generally reliable, verify key claims |
| 40-69 | ⚠️ Questionable | Cross-reference with reputable sources |
| 20-39 | ⚠️ Likely Biased | Do NOT make investment decisions |
| 0-19 | 🚨 High Risk | Report suspicious content |

### What It Detects

#### Red Flags for Manipulation
- **Urgency Tactics**: "NOW", "URGENT", "LAST CHANCE", "DON'T MISS"
- **False Guarantees**: "GUARANTEED", "100% PROFIT", "CAN'T LOSE"
- **Hyperbolic Claims**: "10X", "TO THE MOON", "MOONSHOT"
- **Excessive Emojis**: 🚀💎💰 (5+ in short text)
- **Promotional Language**: "EXCLUSIVE", "VIP ACCESS", "LIMITED TIME"
- **FUD Tactics**: "CRASH", "DISASTER", "GOING TO ZERO"

#### Pattern Detection
- **Volume Spikes**: >10 articles in 1-2 hours (coordinated campaigns)
- **Sentiment Anomalies**: >30 point shifts in 24 hours (artificial manipulation)
- **Coordinated Posting**: Multiple sources posting similar content simultaneously
- **Bot Detection**: Copy-paste content across different outlets

### Source Tiers

**Tier 1 (95-100)** - Premium Financial Sources  
→ Bloomberg, Reuters, WSJ, Financial Times, AP

**Tier 2 (80-95)** - Reputable Financial Media  
→ CNBC, MarketWatch, Yahoo Finance, Seeking Alpha, Benzinga

**Tier 3 (40-80)** - Smaller Outlets  
→ Financial blogs, medium-sized news sites

**Tier 4 (0-40)** - Unknown/Suspicious  
→ Social media posts, unknown blogs, anonymous sources

### Getting Started

#### 1. Run Examples
```bash
python examples/credibility_example.py
```

#### 2. Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

#### 3. Read Documentation
- [Full Documentation](docs/CREDIBILITY_SYSTEM.md) - Complete API reference
- [Quick Start Guide](docs/CREDIBILITY_QUICK_START.md) - Get started in 5 minutes
- [Configuration Guide](docs/CREDIBILITY_SYSTEM.md#configuration) - Customize settings

### Real-World Use Cases

#### For Investors
- **Verify news authenticity** before making investment decisions
- **Detect pump & dump schemes** targeting your portfolio
- **Monitor sentiment manipulation** on stocks you're watching
- **Cross-reference claims** across multiple sources

#### For Traders
- **Real-time manipulation alerts** for active positions
- **Volume spike detection** to avoid artificial hype
- **FUD campaign identification** to avoid panic selling
- **Source verification** for breaking news

#### For Content Creators
- **Fact-check sources** before sharing news
- **Identify promotional content** masquerading as news
- **Verify story authenticity** across multiple outlets
- **Build credibility** by sharing verified information

#### For Researchers
- **Analyze manipulation patterns** across different stocks
- **Track source reliability** over time
- **Study coordinated campaigns** and their impact
- **Generate credibility reports** for datasets

### Configuration Files

#### Source Ratings (`config/source_ratings.json`)
```json
{
  "tiers": {
    "tier1": {
      "sources": [
        {
          "name": "Bloomberg",
          "domain": "bloomberg.com",
          "score": 98,
          "category": "finance"
        }
      ]
    }
  }
}
```

#### Manipulation Patterns (`config/manipulation_patterns.json`)
```json
{
  "urgency_keywords": {
    "weight": 15,
    "keywords": ["NOW", "URGENT", "LAST CHANCE"]
  },
  "volume_spike_threshold": {
    "articles_per_hour": 10
  }
}
```

### Testing

All credibility modules include comprehensive tests:

```bash
# Run all tests (42 test cases)
python -m unittest discover -s tests -p "test_*.py" -v

# Test specific modules
python -m unittest tests.test_source_analyzer -v      # 12 tests
python -m unittest tests.test_manipulation_detector -v # 18 tests
python -m unittest tests.test_scoring -v              # 12 tests
```

**Test Coverage:**
- ✅ Source credibility rating
- ✅ Domain extraction and matching
- ✅ Tier management and queries
- ✅ All manipulation detection methods
- ✅ Volume spike detection
- ✅ Coordinated posting detection
- ✅ Sentiment anomaly detection
- ✅ Reality score calculation
- ✅ Batch processing
- ✅ Risk summary generation

### Performance

- **Fast**: Analyze article in <10ms
- **Lightweight**: No additional dependencies
- **Scalable**: Batch process thousands of articles
- **Real-time**: Suitable for live monitoring
- **Accurate**: Based on proven manipulation patterns

### Security & Privacy

- ✅ All processing is **local** - no external API calls
- ✅ **No data collection** - your analysis stays private
- ✅ **Open source** - audit the code yourself
- ✅ **Configurable** - adjust detection sensitivity
- ✅ **Transparent** - see exactly why each score was assigned

### Limitations & Best Practices

#### Limitations
- Cannot verify factual accuracy of claims
- Relies on source domain for credibility (can be spoofed)
- Pattern detection may have false positives/negatives
- New manipulation tactics may not be detected

#### Best Practices
1. **Always cross-reference** with multiple sources
2. **Don't rely solely** on automated scores
3. **Update source ratings** based on performance
4. **Customize thresholds** for your use case
5. **Combine with fundamental analysis**
6. **Report suspicious patterns** to authorities

### Contributing

Help improve the credibility system:

1. **Add new sources** to `config/source_ratings.json`
2. **Report false positives** via GitHub issues
3. **Suggest new patterns** for manipulation detection
4. **Share test cases** of known manipulation
5. **Improve documentation** and examples

### Roadmap

- [ ] Machine learning-based pattern detection
- [ ] Historical credibility tracking per source
- [ ] Integration with main TrendRadar pipeline
- [ ] REST API endpoints for credibility analysis
- [ ] Real-time alerting system
- [ ] Browser extension for instant checks
- [ ] Mobile app integration
- [ ] Multi-language support

### License

Same as main TrendRadar project (GPL-3.0)

---

**⚠️ Disclaimer**: The credibility system is a tool to assist in analysis, not a substitute for professional financial advice. Always conduct thorough research and consult financial professionals before making investment decisions.

---

### Learn More

📖 [Full Documentation](docs/CREDIBILITY_SYSTEM.md)  
🚀 [Quick Start Guide](docs/CREDIBILITY_QUICK_START.md)  
💻 [Example Scripts](examples/credibility_example.py)  
🧪 [Test Suite](tests/)  
⚙️ [Configuration](config/source_ratings.json)
