"""
Stock Manipulation Detection Engine

This module implements detection algorithms for identifying coordinated news campaigns,
pump & dump schemes, and other forms of market manipulation through news content.
"""

import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import os


class ManipulationDetector:
    """Detects potential manipulation patterns in news articles"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ManipulationDetector
        
        Args:
            config_path: Path to manipulation_patterns.json config file
        """
        if config_path is None:
            config_path = os.path.join("config", "manipulation_patterns.json")
        
        self.config_path = Path(config_path)
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict:
        """Load manipulation patterns from configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Manipulation patterns config not found: {self.config_path}"
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def detect_urgency_language(self, text: str) -> Dict:
        """
        Detect urgency keywords in text
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        text_upper = text.upper()
        keywords = self.patterns['urgency_keywords']['keywords']
        weight = self.patterns['urgency_keywords']['weight']
        
        found_keywords = []
        count = 0
        
        for keyword in keywords:
            if keyword in text_upper:
                found_keywords.append(keyword)
                count += text_upper.count(keyword)
        
        score = min(count * weight, 100)
        
        return {
            'detected': len(found_keywords) > 0,
            'count': count,
            'keywords_found': found_keywords,
            'score': score,
            'weight': weight
        }
    
    def detect_guarantee_promises(self, text: str) -> Dict:
        """
        Detect guarantee/promise keywords in text
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        text_upper = text.upper()
        keywords = self.patterns['guarantee_keywords']['keywords']
        weight = self.patterns['guarantee_keywords']['weight']
        
        found_keywords = []
        count = 0
        
        for keyword in keywords:
            if keyword in text_upper:
                found_keywords.append(keyword)
                count += text_upper.count(keyword)
        
        score = min(count * weight, 100)
        
        return {
            'detected': len(found_keywords) > 0,
            'count': count,
            'keywords_found': found_keywords,
            'score': score,
            'weight': weight
        }
    
    def detect_hyperbolic_language(self, text: str) -> Dict:
        """
        Detect hyperbolic/exaggerated language
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        text_upper = text.upper()
        keywords = self.patterns['hyperbolic_keywords']['keywords']
        weight = self.patterns['hyperbolic_keywords']['weight']
        
        found_keywords = []
        count = 0
        
        for keyword in keywords:
            if keyword in text_upper:
                found_keywords.append(keyword)
                count += text_upper.count(keyword)
        
        score = min(count * weight, 100)
        
        return {
            'detected': len(found_keywords) > 0,
            'count': count,
            'keywords_found': found_keywords,
            'score': score,
            'weight': weight
        }
    
    def detect_promotional_language(self, text: str) -> Dict:
        """
        Detect promotional language
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        text_upper = text.upper()
        keywords = self.patterns['promotional_language']['keywords']
        weight = self.patterns['promotional_language']['weight']
        
        found_keywords = []
        count = 0
        
        for keyword in keywords:
            if keyword in text_upper:
                found_keywords.append(keyword)
                count += text_upper.count(keyword)
        
        score = min(count * weight, 100)
        
        return {
            'detected': len(found_keywords) > 0,
            'count': count,
            'keywords_found': found_keywords,
            'score': score,
            'weight': weight
        }
    
    def detect_fud_language(self, text: str) -> Dict:
        """
        Detect FUD (Fear, Uncertainty, Doubt) language
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        text_upper = text.upper()
        keywords = self.patterns['fud_keywords']['keywords']
        weight = self.patterns['fud_keywords']['weight']
        
        found_keywords = []
        count = 0
        
        for keyword in keywords:
            if keyword in text_upper:
                found_keywords.append(keyword)
                count += text_upper.count(keyword)
        
        score = min(count * weight, 100)
        
        return {
            'detected': len(found_keywords) > 0,
            'count': count,
            'keywords_found': found_keywords,
            'score': score,
            'weight': weight
        }
    
    def detect_excessive_emojis(self, text: str) -> Dict:
        """
        Detect excessive emoji usage
        
        Args:
            text: Article text content
            
        Returns:
            Dictionary with detection results
        """
        common_emojis = self.patterns['emoji_patterns']['common_emojis']
        threshold = self.patterns['emoji_patterns']['threshold']
        weight = self.patterns['emoji_patterns']['weight']
        
        emoji_count = 0
        found_emojis = []
        
        for emoji in common_emojis:
            count = text.count(emoji)
            if count > 0:
                emoji_count += count
                found_emojis.append(emoji)
        
        # General emoji detection (Unicode ranges)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        
        all_emojis = emoji_pattern.findall(text)
        total_emoji_count = len(all_emojis)
        
        detected = total_emoji_count >= threshold
        score = min((total_emoji_count / threshold) * weight, 100) if detected else 0
        
        return {
            'detected': detected,
            'count': total_emoji_count,
            'common_emojis_found': found_emojis,
            'score': score,
            'weight': weight,
            'threshold': threshold
        }
    
    def analyze_content_quality(self, text: str, title: str = "") -> Dict:
        """
        Comprehensive content quality analysis
        
        Args:
            text: Article text content
            title: Article title (optional)
            
        Returns:
            Dictionary with quality score and breakdown
        """
        combined_text = f"{title} {text}"
        
        # Run all detections
        urgency = self.detect_urgency_language(combined_text)
        guarantees = self.detect_guarantee_promises(combined_text)
        hyperbolic = self.detect_hyperbolic_language(combined_text)
        promotional = self.detect_promotional_language(combined_text)
        fud = self.detect_fud_language(combined_text)
        emojis = self.detect_excessive_emojis(combined_text)
        
        # Calculate total manipulation score
        total_score = (
            urgency['score'] + 
            guarantees['score'] + 
            hyperbolic['score'] + 
            promotional['score'] + 
            fud['score'] + 
            emojis['score']
        )
        
        # Cap at 100
        total_score = min(total_score, 100)
        
        # Determine quality level
        thresholds = self.patterns['content_quality_thresholds']
        if total_score >= thresholds['high_risk']:
            quality_level = 'high_risk'
        elif total_score >= thresholds['suspicious']:
            quality_level = 'suspicious'
        elif total_score >= thresholds['questionable']:
            quality_level = 'questionable'
        elif total_score >= thresholds['good']:
            quality_level = 'good'
        else:
            quality_level = 'excellent'
        
        return {
            'manipulation_score': total_score,
            'quality_level': quality_level,
            'detections': {
                'urgency': urgency,
                'guarantees': guarantees,
                'hyperbolic': hyperbolic,
                'promotional': promotional,
                'fud': fud,
                'emojis': emojis
            },
            'flags': self._generate_flags(
                urgency, guarantees, hyperbolic, promotional, fud, emojis
            )
        }
    
    def _generate_flags(self, urgency: Dict, guarantees: Dict, hyperbolic: Dict,
                       promotional: Dict, fud: Dict, emojis: Dict) -> List[str]:
        """Generate human-readable flags for detected issues"""
        flags = []
        
        if urgency['detected']:
            flags.append(f"Excessive urgency language ({urgency['count']} instances)")
        if guarantees['detected']:
            flags.append(f"Unrealistic guarantees detected ({guarantees['count']} instances)")
        if hyperbolic['detected']:
            flags.append(f"Hyperbolic claims ({hyperbolic['count']} instances)")
        if promotional['detected']:
            flags.append(f"Promotional content ({promotional['count']} instances)")
        if fud['detected']:
            flags.append(f"FUD tactics detected ({fud['count']} instances)")
        if emojis['detected']:
            flags.append(f"Excessive emojis ({emojis['count']} found, threshold: {emojis['threshold']})")
        
        return flags
    
    def detect_volume_spike(self, article_timestamps: List[datetime], 
                           ticker: str) -> Dict:
        """
        Detect unusual volume of articles in short time window
        
        Args:
            article_timestamps: List of article publication timestamps
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with spike detection results
        """
        threshold = self.patterns['volume_spike_threshold']['articles_per_hour']
        
        if not article_timestamps:
            return {
                'detected': False,
                'ticker': ticker,
                'article_count': 0,
                'threshold': threshold
            }
        
        # Sort timestamps
        sorted_timestamps = sorted(article_timestamps)
        
        # Check for spikes in 1-2 hour windows
        spikes = []
        
        for i, timestamp in enumerate(sorted_timestamps):
            window_end = timestamp + timedelta(hours=2)
            articles_in_window = [
                ts for ts in sorted_timestamps[i:]
                if ts <= window_end
            ]
            
            if len(articles_in_window) >= threshold:
                spikes.append({
                    'start_time': timestamp,
                    'end_time': window_end,
                    'article_count': len(articles_in_window),
                    'timestamps': articles_in_window
                })
        
        return {
            'detected': len(spikes) > 0,
            'ticker': ticker,
            'spikes': spikes,
            'threshold': threshold,
            'total_articles': len(article_timestamps)
        }
    
    def detect_coordinated_posting(self, articles: List[Dict]) -> Dict:
        """
        Detect coordinated posting patterns
        
        Args:
            articles: List of article dictionaries with 'timestamp', 'source', 'title'
            
        Returns:
            Dictionary with coordination detection results
        """
        config = self.patterns['coordinated_posting']
        time_window = timedelta(minutes=config['time_window_minutes'])
        min_sources = config['min_sources']
        
        coordinated_groups = []
        
        # Group articles by time windows
        for i, article in enumerate(articles):
            timestamp = article.get('timestamp')
            if not timestamp:
                continue
            
            window_end = timestamp + time_window
            
            # Find articles in time window
            articles_in_window = [
                a for a in articles[i:]
                if a.get('timestamp') and a['timestamp'] <= window_end
            ]
            
            # Check for unique sources
            sources = set(a.get('source', '') for a in articles_in_window if a.get('source'))
            
            if len(sources) >= min_sources and len(articles_in_window) >= min_sources:
                # Check for similar content
                titles = [a.get('title', '') for a in articles_in_window]
                similarity = self._calculate_content_similarity(titles)
                
                if similarity > 0.6:  # 60% similarity threshold
                    coordinated_groups.append({
                        'start_time': timestamp,
                        'end_time': window_end,
                        'sources': list(sources),
                        'article_count': len(articles_in_window),
                        'similarity_score': similarity,
                        'articles': articles_in_window
                    })
        
        return {
            'detected': len(coordinated_groups) > 0,
            'coordinated_groups': coordinated_groups,
            'time_window_minutes': config['time_window_minutes'],
            'min_sources': min_sources
        }
    
    def _calculate_content_similarity(self, titles: List[str]) -> float:
        """
        Calculate similarity between article titles
        
        Args:
            titles: List of article titles
            
        Returns:
            Similarity score (0-1)
        """
        if len(titles) < 2:
            return 0.0
        
        # Simple word-based similarity
        word_sets = [set(title.lower().split()) for title in titles]
        
        # Calculate average pairwise similarity
        similarities = []
        for i in range(len(word_sets)):
            for j in range(i + 1, len(word_sets)):
                if not word_sets[i] or not word_sets[j]:
                    continue
                intersection = len(word_sets[i] & word_sets[j])
                union = len(word_sets[i] | word_sets[j])
                if union > 0:
                    similarities.append(intersection / union)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def detect_sentiment_anomaly(self, sentiment_history: List[Dict]) -> Dict:
        """
        Detect sudden sentiment shifts
        
        Args:
            sentiment_history: List of dicts with 'timestamp' and 'sentiment_score'
            
        Returns:
            Dictionary with anomaly detection results
        """
        threshold = self.patterns['sentiment_change_threshold']['points_24h']
        
        if len(sentiment_history) < 2:
            return {
                'detected': False,
                'change': 0,
                'threshold': threshold
            }
        
        # Sort by timestamp
        sorted_history = sorted(sentiment_history, key=lambda x: x['timestamp'])
        
        # Check for large changes in 24-hour windows
        anomalies = []
        
        for i in range(len(sorted_history) - 1):
            current = sorted_history[i]
            window_end = current['timestamp'] + timedelta(hours=24)
            
            # Find sentiment values in 24-hour window
            future_values = [
                h['sentiment_score'] for h in sorted_history[i+1:]
                if h['timestamp'] <= window_end
            ]
            
            if future_values:
                max_change = max(abs(v - current['sentiment_score']) for v in future_values)
                
                if max_change >= threshold:
                    anomalies.append({
                        'start_time': current['timestamp'],
                        'start_sentiment': current['sentiment_score'],
                        'max_change': max_change,
                        'direction': 'positive' if max(future_values) > current['sentiment_score'] else 'negative'
                    })
        
        return {
            'detected': len(anomalies) > 0,
            'anomalies': anomalies,
            'threshold': threshold
        }
