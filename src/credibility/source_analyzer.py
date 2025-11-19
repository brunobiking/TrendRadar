"""
News Source Credibility Analyzer

This module provides functionality to rate news sources based on their credibility
and maintain a database of source ratings.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


class SourceAnalyzer:
    """Analyzes and rates news sources for credibility"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SourceAnalyzer
        
        Args:
            config_path: Path to source_ratings.json config file
        """
        if config_path is None:
            config_path = os.path.join("config", "source_ratings.json")
        
        self.config_path = Path(config_path)
        self.ratings_data = self._load_ratings()
        self.domain_cache = self._build_domain_cache()
        
    def _load_ratings(self) -> Dict:
        """Load source ratings from configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Source ratings config not found: {self.config_path}"
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _build_domain_cache(self) -> Dict[str, Dict]:
        """Build a quick lookup cache for domains"""
        cache = {}
        
        for tier_key, tier_data in self.ratings_data.get('tiers', {}).items():
            for source in tier_data.get('sources', []):
                domain = source.get('domain', '').lower()
                if domain and domain != '*':
                    cache[domain] = {
                        'name': source.get('name'),
                        'score': source.get('score'),
                        'tier': tier_key,
                        'category': source.get('category'),
                        'language': source.get('language')
                    }
        
        return cache
    
    def extract_domain(self, url: str) -> str:
        """
        Extract domain from URL
        
        Args:
            url: URL string
            
        Returns:
            Domain name
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return ""
    
    def get_source_rating(self, url: str) -> Dict:
        """
        Get credibility rating for a source based on URL
        
        Args:
            url: URL of the news article
            
        Returns:
            Dictionary with rating information including:
            - score: int (0-100)
            - tier: str
            - source_name: str
            - category: str
            - confidence: str (high/medium/low)
        """
        domain = self.extract_domain(url)
        
        if not domain:
            return self._get_default_rating("unknown")
        
        # Check exact domain match
        if domain in self.domain_cache:
            info = self.domain_cache[domain]
            return {
                'score': info['score'],
                'tier': info['tier'],
                'source_name': info['name'],
                'domain': domain,
                'category': info['category'],
                'confidence': 'high'
            }
        
        # Check for partial matches (subdomains)
        for cached_domain, info in self.domain_cache.items():
            if domain.endswith(cached_domain):
                return {
                    'score': info['score'],
                    'tier': info['tier'],
                    'source_name': info['name'],
                    'domain': domain,
                    'category': info['category'],
                    'confidence': 'medium'
                }
        
        # Unknown source
        return self._get_default_rating(domain)
    
    def _get_default_rating(self, domain: str) -> Dict:
        """Get default rating for unknown sources"""
        default_score = self.ratings_data.get('default_score', 20)
        
        return {
            'score': default_score,
            'tier': 'tier4',
            'source_name': 'Unknown Source',
            'domain': domain,
            'category': 'unknown',
            'confidence': 'low'
        }
    
    def get_tier_info(self, tier: str) -> Optional[Dict]:
        """
        Get information about a specific tier
        
        Args:
            tier: Tier identifier (e.g., 'tier1')
            
        Returns:
            Dictionary with tier information or None
        """
        return self.ratings_data.get('tiers', {}).get(tier)
    
    def add_source(self, name: str, domain: str, score: int, 
                   tier: str, category: str = "finance", 
                   language: str = "en") -> bool:
        """
        Add a new source to the ratings database
        
        Args:
            name: Source name
            domain: Source domain
            score: Credibility score (0-100)
            tier: Tier identifier (tier1-tier4)
            category: Source category
            language: Source language
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if tier not in self.ratings_data.get('tiers', {}):
                print(f"Invalid tier: {tier}")
                return False
            
            new_source = {
                'name': name,
                'domain': domain.lower(),
                'score': score,
                'category': category,
                'language': language
            }
            
            # Add to configuration
            self.ratings_data['tiers'][tier]['sources'].append(new_source)
            
            # Update cache
            self.domain_cache[domain.lower()] = {
                'name': name,
                'score': score,
                'tier': tier,
                'category': category,
                'language': language
            }
            
            # Save to file
            self._save_ratings()
            return True
            
        except Exception as e:
            print(f"Error adding source: {e}")
            return False
    
    def update_source_score(self, domain: str, new_score: int) -> bool:
        """
        Update the credibility score for a source
        
        Args:
            domain: Source domain
            new_score: New credibility score (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            domain = domain.lower()
            
            # Find and update in configuration
            for tier_data in self.ratings_data.get('tiers', {}).values():
                for source in tier_data.get('sources', []):
                    if source.get('domain', '').lower() == domain:
                        source['score'] = new_score
                        
                        # Update cache
                        if domain in self.domain_cache:
                            self.domain_cache[domain]['score'] = new_score
                        
                        # Save to file
                        self._save_ratings()
                        return True
            
            print(f"Source not found: {domain}")
            return False
            
        except Exception as e:
            print(f"Error updating source score: {e}")
            return False
    
    def _save_ratings(self) -> None:
        """Save ratings data to configuration file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.ratings_data, f, indent=2, ensure_ascii=False)
    
    def get_all_sources(self) -> List[Dict]:
        """
        Get all sources from all tiers
        
        Returns:
            List of all source dictionaries
        """
        all_sources = []
        
        for tier_key, tier_data in self.ratings_data.get('tiers', {}).items():
            for source in tier_data.get('sources', []):
                source_info = source.copy()
                source_info['tier'] = tier_key
                all_sources.append(source_info)
        
        return all_sources
    
    def get_sources_by_tier(self, tier: str) -> List[Dict]:
        """
        Get all sources in a specific tier
        
        Args:
            tier: Tier identifier
            
        Returns:
            List of source dictionaries
        """
        tier_data = self.ratings_data.get('tiers', {}).get(tier, {})
        return tier_data.get('sources', [])
    
    def get_sources_by_category(self, category: str) -> List[Dict]:
        """
        Get all sources in a specific category
        
        Args:
            category: Category name (e.g., 'finance', 'social')
            
        Returns:
            List of source dictionaries
        """
        matching_sources = []
        
        for tier_key, tier_data in self.ratings_data.get('tiers', {}).items():
            for source in tier_data.get('sources', []):
                if source.get('category') == category:
                    source_info = source.copy()
                    source_info['tier'] = tier_key
                    matching_sources.append(source_info)
        
        return matching_sources
    
    def analyze_source_distribution(self, urls: List[str]) -> Dict:
        """
        Analyze the distribution of source credibility in a list of URLs
        
        Args:
            urls: List of article URLs
            
        Returns:
            Dictionary with distribution statistics
        """
        tier_counts = {'tier1': 0, 'tier2': 0, 'tier3': 0, 'tier4': 0}
        total_score = 0
        ratings = []
        
        for url in urls:
            rating = self.get_source_rating(url)
            ratings.append(rating)
            tier_counts[rating['tier']] += 1
            total_score += rating['score']
        
        return {
            'total_sources': len(urls),
            'tier_distribution': tier_counts,
            'average_score': total_score / len(urls) if urls else 0,
            'ratings': ratings
        }
