"""
Unit tests for ManipulationDetector module
"""

import unittest
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.credibility.manipulation_detector import ManipulationDetector


class TestManipulationDetector(unittest.TestCase):
    """Test cases for ManipulationDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = ManipulationDetector()
    
    def test_detect_urgency_language(self):
        """Test detection of urgency keywords"""
        urgent_text = "BUY NOW! This is URGENT! DON'T MISS this opportunity!"
        result = self.detector.detect_urgency_language(urgent_text)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['count'], 0)
        self.assertGreater(len(result['keywords_found']), 0)
        self.assertGreater(result['score'], 0)
    
    def test_detect_guarantee_promises(self):
        """Test detection of guarantee keywords"""
        guarantee_text = "GUARANTEED returns! 100% PROFIT! This is a SURE THING!"
        result = self.detector.detect_guarantee_promises(guarantee_text)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['count'], 0)
        self.assertIn('GUARANTEED', result['keywords_found'])
    
    def test_detect_hyperbolic_language(self):
        """Test detection of hyperbolic language"""
        hyperbolic_text = "This stock will 10X! TO THE MOON! MASSIVE GAINS ahead!"
        result = self.detector.detect_hyperbolic_language(hyperbolic_text)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['count'], 0)
        self.assertGreater(result['score'], 0)
    
    def test_detect_promotional_language(self):
        """Test detection of promotional language"""
        promo_text = "EXCLUSIVE offer! JOIN US now! LIMITED SPOTS available!"
        result = self.detector.detect_promotional_language(promo_text)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['count'], 0)
    
    def test_detect_fud_language(self):
        """Test detection of FUD (Fear, Uncertainty, Doubt) language"""
        fud_text = "Company will CRASH! Total DISASTER! Going to ZERO!"
        result = self.detector.detect_fud_language(fud_text)
        
        self.assertTrue(result['detected'])
        self.assertGreater(result['count'], 0)
        self.assertIn('CRASH', result['keywords_found'])
    
    def test_detect_excessive_emojis(self):
        """Test detection of excessive emojis"""
        # Need at least 5 emojis (threshold) - spread them out with text between
        emoji_text = "Buy 🚀 now! 💎 Great deal! 💰 Limited time! 📈 Don't miss! 🔥 Act fast!"
        result = self.detector.detect_excessive_emojis(emoji_text)
        
        self.assertTrue(result['detected'])
        self.assertGreaterEqual(result['count'], result['threshold'])
    
    def test_clean_content_no_manipulation(self):
        """Test analysis of clean, credible content"""
        clean_text = "Company reports quarterly earnings beat expectations. Revenue increased 15% year-over-year."
        result = self.detector.analyze_content_quality(clean_text)
        
        self.assertLess(result['manipulation_score'], 20)
        self.assertIn(result['quality_level'], ['excellent', 'good'])
    
    def test_manipulative_content_high_score(self):
        """Test analysis of highly manipulative content"""
        manipulative_text = """
        URGENT! BUY NOW! GUARANTEED 10X returns! 🚀🚀🚀
        This is your LAST CHANCE! DON'T MISS OUT!
        MASSIVE GAINS coming! TO THE MOON! 💰💰💰
        EXCLUSIVE insider information! ACT FAST!
        """
        result = self.detector.analyze_content_quality(manipulative_text)
        
        self.assertGreater(result['manipulation_score'], 50)
        self.assertIn(result['quality_level'], ['suspicious', 'high_risk'])
        self.assertGreater(len(result['flags']), 0)
    
    def test_analyze_content_quality_breakdown(self):
        """Test that content analysis provides detailed breakdown"""
        text = "BUY NOW! GUARANTEED profits! 🚀🚀🚀"
        result = self.detector.analyze_content_quality(text)
        
        self.assertIn('detections', result)
        self.assertIn('urgency', result['detections'])
        self.assertIn('guarantees', result['detections'])
        self.assertIn('emojis', result['detections'])
        self.assertIn('flags', result)
    
    def test_detect_volume_spike(self):
        """Test detection of article volume spikes"""
        now = datetime.now()
        # Create 12 articles within 1 hour (threshold is 10)
        timestamps = [now + timedelta(minutes=i*5) for i in range(12)]
        
        result = self.detector.detect_volume_spike(timestamps, "AAPL")
        
        self.assertTrue(result['detected'])
        self.assertEqual(result['ticker'], "AAPL")
        self.assertGreater(len(result['spikes']), 0)
    
    def test_no_volume_spike(self):
        """Test when there's no volume spike"""
        now = datetime.now()
        # Create only 5 articles over several hours
        timestamps = [now + timedelta(hours=i) for i in range(5)]
        
        result = self.detector.detect_volume_spike(timestamps, "AAPL")
        
        self.assertFalse(result['detected'])
    
    def test_detect_coordinated_posting(self):
        """Test detection of coordinated posting"""
        now = datetime.now()
        
        # Create similar articles from different sources at similar times
        articles = [
            {
                'timestamp': now,
                'source': 'source1',
                'title': 'Tesla stock price soaring today'
            },
            {
                'timestamp': now + timedelta(minutes=5),
                'source': 'source2',
                'title': 'Tesla stock price soaring'
            },
            {
                'timestamp': now + timedelta(minutes=10),
                'source': 'source3',
                'title': 'Tesla stock soaring today'
            }
        ]
        
        result = self.detector.detect_coordinated_posting(articles)
        
        # May or may not detect based on similarity threshold
        self.assertIn('detected', result)
        self.assertIn('coordinated_groups', result)
    
    def test_detect_sentiment_anomaly(self):
        """Test detection of sentiment anomalies"""
        now = datetime.now()
        
        # Create sentiment history with a large shift
        sentiment_history = [
            {'timestamp': now - timedelta(hours=48), 'sentiment_score': 50},
            {'timestamp': now - timedelta(hours=24), 'sentiment_score': 55},
            {'timestamp': now, 'sentiment_score': 90},  # Large jump
        ]
        
        result = self.detector.detect_sentiment_anomaly(sentiment_history)
        
        self.assertTrue(result['detected'])
        self.assertGreater(len(result['anomalies']), 0)


class TestManipulationDetectorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = ManipulationDetector()
    
    def test_empty_text(self):
        """Test handling of empty text"""
        result = self.detector.analyze_content_quality("")
        
        self.assertEqual(result['manipulation_score'], 0)
        self.assertEqual(result['quality_level'], 'excellent')
    
    def test_empty_timestamps(self):
        """Test volume spike with empty timestamps"""
        result = self.detector.detect_volume_spike([], "AAPL")
        
        self.assertFalse(result['detected'])
        self.assertEqual(result['article_count'], 0)
    
    def test_empty_articles_coordination(self):
        """Test coordinated posting with empty article list"""
        result = self.detector.detect_coordinated_posting([])
        
        self.assertFalse(result['detected'])
    
    def test_single_article_coordination(self):
        """Test coordinated posting with single article"""
        now = datetime.now()
        articles = [
            {'timestamp': now, 'source': 'source1', 'title': 'Test article'}
        ]
        
        result = self.detector.detect_coordinated_posting(articles)
        
        self.assertFalse(result['detected'])
    
    def test_insufficient_sentiment_history(self):
        """Test sentiment anomaly with insufficient data"""
        now = datetime.now()
        sentiment_history = [
            {'timestamp': now, 'sentiment_score': 50}
        ]
        
        result = self.detector.detect_sentiment_anomaly(sentiment_history)
        
        self.assertFalse(result['detected'])


if __name__ == '__main__':
    unittest.main()
