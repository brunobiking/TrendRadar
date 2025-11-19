"""
Manipulation Score Calculator

This module combines various detection signals into a unified "Reality Score"
that represents the overall credibility and manipulation risk of news content.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


class CredibilityScorer:
    """Calculates unified credibility/reality scores for news content"""
    
    def __init__(self):
        """Initialize the CredibilityScorer"""
        self.score_ranges = {
            'highly_credible': (90, 100),
            'credible': (70, 89),
            'questionable': (40, 69),
            'likely_biased': (20, 39),
            'high_risk': (0, 19)
        }
    
    def calculate_reality_score(
        self,
        source_rating: Dict,
        content_analysis: Dict,
        cross_reference_data: Optional[Dict] = None,
        volume_spike_data: Optional[Dict] = None,
        sentiment_anomaly_data: Optional[Dict] = None,
        coordination_data: Optional[Dict] = None
    ) -> Dict:
        """
        Calculate comprehensive Reality Score (0-100)
        
        Args:
            source_rating: Dict from SourceAnalyzer.get_source_rating()
            content_analysis: Dict from ManipulationDetector.analyze_content_quality()
            cross_reference_data: Optional cross-reference validation data
            volume_spike_data: Optional volume spike detection data
            sentiment_anomaly_data: Optional sentiment anomaly data
            coordination_data: Optional coordinated posting data
            
        Returns:
            Dictionary with reality score and breakdown
        """
        # Start with source credibility (40% weight)
        source_score = source_rating.get('score', 20)
        source_weight = 0.4
        weighted_source = source_score * source_weight
        
        # Content quality (30% weight)
        # Invert manipulation score (high manipulation = low quality)
        manipulation_score = content_analysis.get('manipulation_score', 0)
        content_quality_score = 100 - manipulation_score
        content_weight = 0.3
        weighted_content = content_quality_score * content_weight
        
        # Cross-reference validation (15% weight)
        cross_ref_score = self._calculate_cross_reference_score(cross_reference_data)
        cross_ref_weight = 0.15
        weighted_cross_ref = cross_ref_score * cross_ref_weight
        
        # Volume/timing patterns (10% weight)
        volume_score = self._calculate_volume_score(volume_spike_data, coordination_data)
        volume_weight = 0.10
        weighted_volume = volume_score * volume_weight
        
        # Sentiment patterns (5% weight)
        sentiment_score = self._calculate_sentiment_score(sentiment_anomaly_data)
        sentiment_weight = 0.05
        weighted_sentiment = sentiment_score * sentiment_weight
        
        # Calculate final score
        reality_score = (
            weighted_source +
            weighted_content +
            weighted_cross_ref +
            weighted_volume +
            weighted_sentiment
        )
        
        # Ensure score is within bounds
        reality_score = max(0, min(100, reality_score))
        
        # Determine category
        category = self._get_score_category(reality_score)
        
        # Generate detailed breakdown
        breakdown = {
            'source_credibility': {
                'score': source_score,
                'weight': source_weight,
                'contribution': weighted_source,
                'details': {
                    'source_name': source_rating.get('source_name'),
                    'tier': source_rating.get('tier'),
                    'confidence': source_rating.get('confidence')
                }
            },
            'content_quality': {
                'score': content_quality_score,
                'weight': content_weight,
                'contribution': weighted_content,
                'manipulation_score': manipulation_score,
                'quality_level': content_analysis.get('quality_level'),
                'flags': content_analysis.get('flags', [])
            },
            'cross_reference': {
                'score': cross_ref_score,
                'weight': cross_ref_weight,
                'contribution': weighted_cross_ref
            },
            'volume_patterns': {
                'score': volume_score,
                'weight': volume_weight,
                'contribution': weighted_volume
            },
            'sentiment_patterns': {
                'score': sentiment_score,
                'weight': sentiment_weight,
                'contribution': weighted_sentiment
            }
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            reality_score, category, breakdown, content_analysis
        )
        
        return {
            'reality_score': round(reality_score, 2),
            'category': category,
            'category_range': self.score_ranges[category],
            'breakdown': breakdown,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_cross_reference_score(self, data: Optional[Dict]) -> float:
        """Calculate score from cross-reference validation"""
        if not data:
            return 50  # Neutral score if no data
        
        reputable_source_count = data.get('reputable_sources', 0)
        total_source_count = data.get('total_sources', 1)
        
        if total_source_count == 0:
            return 50
        
        # Higher score if more reputable sources confirm
        ratio = reputable_source_count / total_source_count
        
        if reputable_source_count >= 3:
            return 90  # Multiple reputable sources
        elif reputable_source_count >= 2:
            return 75  # Two reputable sources
        elif reputable_source_count == 1:
            return 60  # One reputable source
        else:
            return 30  # No reputable sources
    
    def _calculate_volume_score(
        self, 
        spike_data: Optional[Dict],
        coordination_data: Optional[Dict]
    ) -> float:
        """Calculate score from volume and coordination patterns"""
        score = 100  # Start with perfect score
        
        # Penalize for volume spikes
        if spike_data and spike_data.get('detected'):
            spike_count = len(spike_data.get('spikes', []))
            score -= min(spike_count * 20, 40)  # Up to -40 for spikes
        
        # Penalize for coordinated posting
        if coordination_data and coordination_data.get('detected'):
            coord_count = len(coordination_data.get('coordinated_groups', []))
            score -= min(coord_count * 25, 50)  # Up to -50 for coordination
        
        return max(0, score)
    
    def _calculate_sentiment_score(self, anomaly_data: Optional[Dict]) -> float:
        """Calculate score from sentiment anomaly patterns"""
        if not anomaly_data or not anomaly_data.get('detected'):
            return 100  # Perfect score if no anomalies
        
        anomaly_count = len(anomaly_data.get('anomalies', []))
        
        # More anomalies = lower score
        penalty = min(anomaly_count * 30, 70)
        return max(30, 100 - penalty)
    
    def _get_score_category(self, score: float) -> str:
        """Determine category based on score"""
        for category, (low, high) in self.score_ranges.items():
            if low <= score <= high:
                return category
        return 'questionable'
    
    def _generate_recommendations(
        self,
        score: float,
        category: str,
        breakdown: Dict,
        content_analysis: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Category-based recommendations
        if category == 'highly_credible':
            recommendations.append("✅ Content appears highly credible from reputable sources")
            recommendations.append("Safe to share and use for decision-making")
        
        elif category == 'credible':
            recommendations.append("✅ Content appears credible but verify key claims")
            recommendations.append("Generally reliable for informational purposes")
        
        elif category == 'questionable':
            recommendations.append("⚠️ Exercise caution - content needs verification")
            recommendations.append("Cross-reference with multiple reputable sources before acting")
        
        elif category == 'likely_biased':
            recommendations.append("⚠️ High likelihood of bias or promotional content")
            recommendations.append("Do not make investment decisions based solely on this content")
            recommendations.append("Seek independent analysis from trusted sources")
        
        elif category == 'high_risk':
            recommendations.append("🚨 HIGH MANIPULATION RISK DETECTED")
            recommendations.append("Do NOT make investment decisions based on this content")
            recommendations.append("Content shows signs of pump & dump or manipulation tactics")
            recommendations.append("Report suspicious content to appropriate authorities")
        
        # Source-specific recommendations
        source_score = breakdown['source_credibility']['score']
        if source_score < 50:
            recommendations.append(
                f"⚠️ Source credibility is low ({source_score}/100) - "
                "verify information independently"
            )
        
        # Content-specific recommendations
        flags = content_analysis.get('flags', [])
        if flags:
            recommendations.append("🚩 Content quality issues detected:")
            for flag in flags[:3]:  # Limit to top 3 flags
                recommendations.append(f"  • {flag}")
        
        # Volume-specific recommendations
        volume_score = breakdown['volume_patterns']['score']
        if volume_score < 70:
            recommendations.append(
                "⚠️ Unusual article volume or coordinated posting detected - "
                "may indicate manipulation campaign"
            )
        
        return recommendations
    
    def batch_calculate_scores(
        self,
        articles: List[Dict]
    ) -> List[Dict]:
        """
        Calculate reality scores for multiple articles
        
        Args:
            articles: List of article dictionaries with analysis data
            
        Returns:
            List of score results
        """
        results = []
        
        for article in articles:
            score_result = self.calculate_reality_score(
                source_rating=article.get('source_rating', {}),
                content_analysis=article.get('content_analysis', {}),
                cross_reference_data=article.get('cross_reference_data'),
                volume_spike_data=article.get('volume_spike_data'),
                sentiment_anomaly_data=article.get('sentiment_anomaly_data'),
                coordination_data=article.get('coordination_data')
            )
            
            results.append({
                'article_id': article.get('id'),
                'title': article.get('title'),
                'url': article.get('url'),
                **score_result
            })
        
        return results
    
    def get_risk_summary(self, scores: List[Dict]) -> Dict:
        """
        Generate summary statistics for multiple scores
        
        Args:
            scores: List of score result dictionaries
            
        Returns:
            Dictionary with summary statistics
        """
        if not scores:
            return {
                'total_articles': 0,
                'average_score': 0,
                'category_distribution': {},
                'high_risk_count': 0
            }
        
        total = len(scores)
        avg_score = sum(s['reality_score'] for s in scores) / total
        
        category_counts = {}
        for score in scores:
            category = score['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        high_risk_count = sum(
            1 for s in scores 
            if s['category'] in ['high_risk', 'likely_biased']
        )
        
        return {
            'total_articles': total,
            'average_score': round(avg_score, 2),
            'category_distribution': category_counts,
            'high_risk_count': high_risk_count,
            'high_risk_percentage': round((high_risk_count / total) * 100, 2)
        }
