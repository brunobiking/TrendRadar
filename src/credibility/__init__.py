"""
TrendRadar Credibility System

A comprehensive system for detecting stock manipulation and rating news source credibility.
"""

from .source_analyzer import SourceAnalyzer
from .manipulation_detector import ManipulationDetector
from .scoring import CredibilityScorer

__all__ = ['SourceAnalyzer', 'ManipulationDetector', 'CredibilityScorer']
__version__ = '1.0.0'
