# Quick Start Guide: Credibility & Manipulation Detection

## 5-Minute Quick Start

### Installation
No additional dependencies needed beyond TrendRadar's standard requirements:
```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from src.credibility import SourceAnalyzer, ManipulationDetector, CredibilityScorer

# Initialize
analyzer = SourceAnalyzer()
detector = ManipulationDetector()
scorer = CredibilityScorer()

# Analyze a news article
url = "https://www.bloomberg.com/article/stock-news"
content = "Company reports strong earnings..."

# Get results
source_rating = analyzer.get_source_rating(url)
content_analysis = detector.analyze_content_quality(content)
reality_score = scorer.calculate_reality_score(
    source_rating=source_rating,
    content_analysis=content_analysis
)

# Check the score
print(f"Reality Score: {reality_score['reality_score']}/100")
print(f"Category: {reality_score['category']}")
```

### Understanding the Reality Score

| Score Range | Category | Meaning |
|-------------|----------|---------|
| 90-100 | Highly Credible | Verified by top-tier sources, safe to use |
| 70-89 | Credible | From reputable sources, generally reliable |
| 40-69 | Questionable | Needs verification, use caution |
| 20-39 | Likely Biased | Promotional content, don't trust |
| 0-19 | High Risk | Manipulation detected, avoid completely |

### Running Examples

```bash
# Run comprehensive examples
python examples/credibility_example.py
```

### Common Use Cases

#### 1. Check if news is from a reputable source
```python
analyzer = SourceAnalyzer()
rating = analyzer.get_source_rating("https://www.reuters.com/article")
print(f"Source credibility: {rating['score']}/100")
```

#### 2. Detect pump & dump schemes
```python
detector = ManipulationDetector()
content = "BUY NOW! GUARANTEED 10X! 🚀🚀🚀"
analysis = detector.analyze_content_quality(content)
if analysis['quality_level'] == 'high_risk':
    print("⚠️ Manipulation detected!")
```

#### 3. Monitor for coordinated campaigns
```python
# Check if multiple articles are part of a coordinated campaign
articles = [
    {'timestamp': datetime.now(), 'source': 'blog1', 'title': 'Stock X to moon'},
    {'timestamp': datetime.now(), 'source': 'blog2', 'title': 'Stock X mooning'},
]
result = detector.detect_coordinated_posting(articles)
if result['detected']:
    print("⚠️ Coordinated campaign detected!")
```

## Next Steps

- Read the [full documentation](CREDIBILITY_SYSTEM.md)
- Run `python examples/credibility_example.py` for more examples
- Customize `config/source_ratings.json` for your needs
- Adjust detection thresholds in `config/manipulation_patterns.json`

## Key Features

✅ **Source Credibility Rating** - Automatic rating of 15+ major news sources  
✅ **Manipulation Detection** - Detects urgency, guarantees, hype, FUD  
✅ **Volume Spike Detection** - Identifies coordinated pump campaigns  
✅ **Sentiment Anomaly Detection** - Flags suspicious sentiment shifts  
✅ **Reality Score** - Single 0-100 score combining all signals  

## Need Help?

- Check [CREDIBILITY_SYSTEM.md](CREDIBILITY_SYSTEM.md) for full API reference
- Run tests: `python -m unittest discover -s tests -p "test_*.py"`
- View examples: `python examples/credibility_example.py`
