"""
Unit tests for CredibilityScorer module
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.credibility.scoring import CredibilityScorer


class TestCredibilityScorer(unittest.TestCase):
    """Test cases for CredibilityScorer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scorer = CredibilityScorer()
    
    def test_highly_credible_score(self):
        """Test calculation for highly credible content"""
        source_rating = {
            'score': 98,
            'tier': 'tier1',
            'source_name': 'Bloomberg',
            'confidence': 'high'
        }
        
        content_analysis = {
            'manipulation_score': 0,
            'quality_level': 'excellent',
            'flags': []
        }
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        self.assertGreaterEqual(result['reality_score'], 90)
        self.assertEqual(result['category'], 'highly_credible')
        self.assertIn('breakdown', result)
        self.assertIn('recommendations', result)
    
    def test_high_risk_score(self):
        """Test calculation for high risk content"""
        source_rating = {
            'score': 20,
            'tier': 'tier4',
            'source_name': 'Unknown Source',
            'confidence': 'low'
        }
        
        content_analysis = {
            'manipulation_score': 95,
            'quality_level': 'high_risk',
            'flags': [
                'Excessive urgency language',
                'Unrealistic guarantees detected',
                'Hyperbolic claims'
            ]
        }
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        self.assertLess(result['reality_score'], 40)
        self.assertIn(result['category'], ['high_risk', 'likely_biased'])
        
        # Check that warnings/recommendations are present
        self.assertGreater(len(result['recommendations']), 0)
        recommendations_text = ' '.join(result['recommendations']).lower()
        # Should contain warning indicators
        self.assertTrue(
            'bias' in recommendations_text or 
            'manipulation' in recommendations_text or
            'caution' in recommendations_text or
            'not make' in recommendations_text
        )
    
    def test_score_with_volume_spike(self):
        """Test that volume spikes reduce score"""
        source_rating = {'score': 80, 'tier': 'tier2', 'source_name': 'Test', 'confidence': 'high'}
        content_analysis = {'manipulation_score': 10, 'quality_level': 'good', 'flags': []}
        
        volume_spike_data = {
            'detected': True,
            'spikes': [{'start_time': 'test', 'article_count': 15}]
        }
        
        result_with_spike = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis,
            volume_spike_data=volume_spike_data
        )
        
        result_without_spike = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis,
            volume_spike_data=None
        )
        
        # Score with spike should be lower
        self.assertLess(
            result_with_spike['reality_score'],
            result_without_spike['reality_score']
        )
    
    def test_score_with_coordination(self):
        """Test that coordinated posting reduces score"""
        source_rating = {'score': 80, 'tier': 'tier2', 'source_name': 'Test', 'confidence': 'high'}
        content_analysis = {'manipulation_score': 10, 'quality_level': 'good', 'flags': []}
        
        coordination_data = {
            'detected': True,
            'coordinated_groups': [
                {'sources': ['source1', 'source2', 'source3']}
            ]
        }
        
        result_with_coord = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis,
            coordination_data=coordination_data
        )
        
        result_without_coord = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis,
            coordination_data=None
        )
        
        # Score with coordination should be lower
        self.assertLess(
            result_with_coord['reality_score'],
            result_without_coord['reality_score']
        )
    
    def test_score_breakdown_weights(self):
        """Test that score breakdown shows correct weights"""
        source_rating = {'score': 80, 'tier': 'tier2', 'source_name': 'Test', 'confidence': 'high'}
        content_analysis = {'manipulation_score': 20, 'quality_level': 'good', 'flags': []}
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        breakdown = result['breakdown']
        
        # Check all components are present
        self.assertIn('source_credibility', breakdown)
        self.assertIn('content_quality', breakdown)
        self.assertIn('cross_reference', breakdown)
        self.assertIn('volume_patterns', breakdown)
        self.assertIn('sentiment_patterns', breakdown)
        
        # Check weights sum to 1.0
        total_weight = (
            breakdown['source_credibility']['weight'] +
            breakdown['content_quality']['weight'] +
            breakdown['cross_reference']['weight'] +
            breakdown['volume_patterns']['weight'] +
            breakdown['sentiment_patterns']['weight']
        )
        self.assertAlmostEqual(total_weight, 1.0, places=2)
    
    def test_cross_reference_multiple_sources(self):
        """Test cross-reference scoring with multiple reputable sources"""
        source_rating = {'score': 80, 'tier': 'tier2', 'source_name': 'Test', 'confidence': 'high'}
        content_analysis = {'manipulation_score': 10, 'quality_level': 'good', 'flags': []}
        
        # Multiple reputable sources confirm the news
        cross_ref_data = {
            'reputable_sources': 3,
            'total_sources': 5
        }
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis,
            cross_reference_data=cross_ref_data
        )
        
        # Should have high cross-reference score
        self.assertGreaterEqual(
            result['breakdown']['cross_reference']['score'],
            85
        )
    
    def test_batch_calculate_scores(self):
        """Test batch scoring of multiple articles"""
        articles = [
            {
                'id': 'article1',
                'title': 'Test Article 1',
                'url': 'http://example.com/1',
                'source_rating': {'score': 90, 'tier': 'tier1', 'source_name': 'Test1', 'confidence': 'high'},
                'content_analysis': {'manipulation_score': 5, 'quality_level': 'excellent', 'flags': []}
            },
            {
                'id': 'article2',
                'title': 'Test Article 2',
                'url': 'http://example.com/2',
                'source_rating': {'score': 30, 'tier': 'tier4', 'source_name': 'Test2', 'confidence': 'low'},
                'content_analysis': {'manipulation_score': 80, 'quality_level': 'high_risk', 'flags': ['test']}
            }
        ]
        
        results = self.scorer.batch_calculate_scores(articles)
        
        self.assertEqual(len(results), 2)
        self.assertIn('article_id', results[0])
        self.assertIn('reality_score', results[0])
        self.assertIn('category', results[0])
    
    def test_risk_summary(self):
        """Test generation of risk summary statistics"""
        scores = [
            {'reality_score': 95, 'category': 'highly_credible'},
            {'reality_score': 75, 'category': 'credible'},
            {'reality_score': 25, 'category': 'likely_biased'},
            {'reality_score': 15, 'category': 'high_risk'}
        ]
        
        summary = self.scorer.get_risk_summary(scores)
        
        self.assertEqual(summary['total_articles'], 4)
        self.assertGreater(summary['average_score'], 0)
        self.assertIn('category_distribution', summary)
        self.assertEqual(summary['high_risk_count'], 2)  # likely_biased + high_risk
        self.assertEqual(summary['high_risk_percentage'], 50.0)
    
    def test_score_within_bounds(self):
        """Test that scores are always within 0-100 range"""
        # Test with extreme values
        source_rating = {'score': 150, 'tier': 'tier1', 'source_name': 'Test', 'confidence': 'high'}
        content_analysis = {'manipulation_score': -50, 'quality_level': 'test', 'flags': []}
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        self.assertGreaterEqual(result['reality_score'], 0)
        self.assertLessEqual(result['reality_score'], 100)
    
    def test_recommendations_present(self):
        """Test that recommendations are always generated"""
        source_rating = {'score': 60, 'tier': 'tier3', 'source_name': 'Test', 'confidence': 'medium'}
        content_analysis = {'manipulation_score': 40, 'quality_level': 'questionable', 'flags': ['test flag']}
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        self.assertIn('recommendations', result)
        self.assertGreater(len(result['recommendations']), 0)
        self.assertIsInstance(result['recommendations'], list)


class TestCredibilityScorerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scorer = CredibilityScorer()
    
    def test_empty_risk_summary(self):
        """Test risk summary with empty score list"""
        summary = self.scorer.get_risk_summary([])
        
        self.assertEqual(summary['total_articles'], 0)
        self.assertEqual(summary['average_score'], 0)
    
    def test_minimal_input(self):
        """Test scoring with minimal input data"""
        source_rating = {'score': 50, 'tier': 'tier3', 'source_name': 'Test', 'confidence': 'low'}
        content_analysis = {'manipulation_score': 30, 'quality_level': 'questionable', 'flags': []}
        
        result = self.scorer.calculate_reality_score(
            source_rating=source_rating,
            content_analysis=content_analysis
        )
        
        # Should complete without error
        self.assertIn('reality_score', result)
        self.assertIn('category', result)


if __name__ == '__main__':
    unittest.main()
