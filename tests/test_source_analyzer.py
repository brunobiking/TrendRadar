"""
Unit tests for SourceAnalyzer module
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.credibility.source_analyzer import SourceAnalyzer


class TestSourceAnalyzer(unittest.TestCase):
    """Test cases for SourceAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = SourceAnalyzer()
    
    def test_extract_domain(self):
        """Test domain extraction from URLs"""
        test_cases = [
            ("https://www.bloomberg.com/article", "bloomberg.com"),
            ("http://reuters.com/news", "reuters.com"),
            ("https://finance.yahoo.com/quote", "finance.yahoo.com"),
            ("www.wsj.com/article", ""),  # Invalid URL
        ]
        
        for url, expected_domain in test_cases:
            with self.subTest(url=url):
                domain = self.analyzer.extract_domain(url)
                self.assertEqual(domain, expected_domain)
    
    def test_tier1_source_rating(self):
        """Test rating for Tier 1 (premium) sources"""
        tier1_urls = [
            "https://www.bloomberg.com/article",
            "https://www.reuters.com/news",
            "https://www.wsj.com/article",
            "https://www.ft.com/content",
        ]
        
        for url in tier1_urls:
            with self.subTest(url=url):
                rating = self.analyzer.get_source_rating(url)
                self.assertEqual(rating['tier'], 'tier1')
                self.assertGreaterEqual(rating['score'], 95)
                self.assertLessEqual(rating['score'], 100)
    
    def test_tier2_source_rating(self):
        """Test rating for Tier 2 (reputable) sources"""
        tier2_urls = [
            "https://www.cnbc.com/article",
            "https://www.marketwatch.com/story",
            "https://finance.yahoo.com/news",
        ]
        
        for url in tier2_urls:
            with self.subTest(url=url):
                rating = self.analyzer.get_source_rating(url)
                self.assertEqual(rating['tier'], 'tier2')
                self.assertGreaterEqual(rating['score'], 80)
                self.assertLess(rating['score'], 95)
    
    def test_unknown_source_rating(self):
        """Test rating for unknown sources"""
        unknown_urls = [
            "https://www.unknown-blog.com/article",
            "https://random-site.net/news",
        ]
        
        for url in unknown_urls:
            with self.subTest(url=url):
                rating = self.analyzer.get_source_rating(url)
                self.assertEqual(rating['tier'], 'tier4')
                self.assertEqual(rating['confidence'], 'low')
                self.assertEqual(rating['score'], 20)  # Default score
    
    def test_get_tier_info(self):
        """Test retrieving tier information"""
        tier_info = self.analyzer.get_tier_info('tier1')
        
        self.assertIsNotNone(tier_info)
        self.assertIn('name', tier_info)
        self.assertIn('score_range', tier_info)
        self.assertIn('sources', tier_info)
    
    def test_get_all_sources(self):
        """Test retrieving all sources"""
        all_sources = self.analyzer.get_all_sources()
        
        self.assertIsInstance(all_sources, list)
        self.assertGreater(len(all_sources), 0)
        
        # Check that each source has required fields
        for source in all_sources:
            self.assertIn('name', source)
            self.assertIn('domain', source)
            self.assertIn('score', source)
            self.assertIn('tier', source)
    
    def test_get_sources_by_category(self):
        """Test filtering sources by category"""
        finance_sources = self.analyzer.get_sources_by_category('finance')
        
        self.assertIsInstance(finance_sources, list)
        self.assertGreater(len(finance_sources), 0)
        
        for source in finance_sources:
            self.assertEqual(source['category'], 'finance')
    
    def test_analyze_source_distribution(self):
        """Test source distribution analysis"""
        test_urls = [
            "https://www.bloomberg.com/article1",
            "https://www.bloomberg.com/article2",
            "https://www.cnbc.com/article",
            "https://unknown-site.com/article",
        ]
        
        distribution = self.analyzer.analyze_source_distribution(test_urls)
        
        self.assertEqual(distribution['total_sources'], 4)
        self.assertIn('tier_distribution', distribution)
        self.assertIn('average_score', distribution)
        
        # Bloomberg is tier1, CNBC is tier2, unknown is tier4
        self.assertEqual(distribution['tier_distribution']['tier1'], 2)
        self.assertEqual(distribution['tier_distribution']['tier2'], 1)
        self.assertEqual(distribution['tier_distribution']['tier4'], 1)
    
    def test_subdomain_matching(self):
        """Test that subdomains are properly matched"""
        # Test with finance.yahoo.com (subdomain)
        rating = self.analyzer.get_source_rating("https://finance.yahoo.com/article")
        
        self.assertIn(rating['tier'], ['tier2', 'tier3', 'tier4'])
        self.assertGreater(rating['score'], 0)


class TestSourceAnalyzerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = SourceAnalyzer()
    
    def test_empty_url(self):
        """Test handling of empty URL"""
        rating = self.analyzer.get_source_rating("")
        
        self.assertEqual(rating['tier'], 'tier4')
        self.assertEqual(rating['confidence'], 'low')
    
    def test_malformed_url(self):
        """Test handling of malformed URLs"""
        malformed_urls = [
            "not-a-url",
            "http://",
            "ftp://invalid",
        ]
        
        for url in malformed_urls:
            with self.subTest(url=url):
                rating = self.analyzer.get_source_rating(url)
                # Should return default rating without crashing
                self.assertIn('score', rating)
                self.assertIn('tier', rating)
    
    def test_empty_distribution(self):
        """Test distribution analysis with empty list"""
        distribution = self.analyzer.analyze_source_distribution([])
        
        self.assertEqual(distribution['total_sources'], 0)
        self.assertEqual(distribution['average_score'], 0)


if __name__ == '__main__':
    unittest.main()
