#!/usr/bin/env python3
"""
Example script demonstrating the TrendRadar Credibility System

This script shows how to use the credibility system to analyze news articles
for potential manipulation and source credibility.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.credibility import SourceAnalyzer, ManipulationDetector, CredibilityScorer
from datetime import datetime, timedelta


def example_basic_analysis():
    """Example 1: Basic article credibility analysis"""
    print("="*80)
    print("EXAMPLE 1: Basic Article Credibility Analysis")
    print("="*80)
    
    # Initialize components
    source_analyzer = SourceAnalyzer()
    manipulation_detector = ManipulationDetector()
    scorer = CredibilityScorer()
    
    # Example article from reputable source
    print("\n--- Analyzing Article from Bloomberg ---")
    url1 = "https://www.bloomberg.com/news/articles/tesla-earnings"
    title1 = "Tesla Reports Strong Quarterly Earnings"
    content1 = """
    Tesla Inc. reported quarterly earnings that exceeded analyst expectations.
    Revenue increased 18% year-over-year, driven by strong vehicle deliveries
    and energy storage products. The company maintained its production guidance
    for the full year.
    """
    
    source_rating1 = source_analyzer.get_source_rating(url1)
    content_analysis1 = manipulation_detector.analyze_content_quality(content1, title1)
    reality_score1 = scorer.calculate_reality_score(
        source_rating=source_rating1,
        content_analysis=content_analysis1
    )
    
    print(f"Source: {source_rating1['source_name']}")
    print(f"Source Credibility: {source_rating1['score']}/100 ({source_rating1['tier']})")
    print(f"Manipulation Score: {content_analysis1['manipulation_score']}/100")
    print(f"Reality Score: {reality_score1['reality_score']}/100")
    print(f"Category: {reality_score1['category']}")
    print(f"\nRecommendations:")
    for rec in reality_score1['recommendations'][:3]:
        print(f"  • {rec}")
    
    # Example article from unknown/suspicious source
    print("\n--- Analyzing Article from Unknown Blog ---")
    url2 = "https://unknown-stockblog.com/tesla-tip"
    title2 = "URGENT: Tesla Stock About to EXPLODE! 🚀🚀🚀"
    content2 = """
    BUY TESLA NOW! This is your LAST CHANCE for GUARANTEED profits!
    Stock will 10X in days! TO THE MOON! 💰💰💰
    MASSIVE GAINS ahead! Don't miss this EXCLUSIVE opportunity!
    ACT FAST before it's too late! 🚀🚀🚀
    """
    
    source_rating2 = source_analyzer.get_source_rating(url2)
    content_analysis2 = manipulation_detector.analyze_content_quality(content2, title2)
    reality_score2 = scorer.calculate_reality_score(
        source_rating=source_rating2,
        content_analysis=content_analysis2
    )
    
    print(f"Source: {source_rating2['source_name']}")
    print(f"Source Credibility: {source_rating2['score']}/100 ({source_rating2['tier']})")
    print(f"Manipulation Score: {content_analysis2['manipulation_score']}/100")
    print(f"Quality Level: {content_analysis2['quality_level']}")
    if content_analysis2['flags']:
        print(f"Flags detected: {len(content_analysis2['flags'])}")
        for flag in content_analysis2['flags'][:3]:
            print(f"  • {flag}")
    print(f"Reality Score: {reality_score2['reality_score']}/100")
    print(f"Category: {reality_score2['category']}")
    print(f"\nRecommendations:")
    for rec in reality_score2['recommendations'][:3]:
        print(f"  • {rec}")


def example_volume_spike_detection():
    """Example 2: Detecting volume spikes for pump & dump schemes"""
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Volume Spike Detection (Pump & Dump Alert)")
    print("="*80)
    
    manipulation_detector = ManipulationDetector()
    
    # Simulate 15 articles about AAPL in 1 hour (suspicious!)
    now = datetime.now()
    timestamps = [now + timedelta(minutes=i*4) for i in range(15)]
    
    print(f"\nAnalyzing article volume for ticker: AAPL")
    print(f"Time window: Last hour")
    print(f"Articles detected: {len(timestamps)}")
    
    spike_result = manipulation_detector.detect_volume_spike(timestamps, "AAPL")
    
    if spike_result['detected']:
        print(f"\n⚠️  VOLUME SPIKE DETECTED!")
        print(f"Number of spikes: {len(spike_result['spikes'])}")
        print(f"Threshold: {spike_result['threshold']} articles/hour")
        print(f"\nThis could indicate:")
        print("  • Coordinated pump campaign")
        print("  • Bot-generated content")
        print("  • Artificial hype generation")
        print("\nRecommendation: Be extremely cautious before making investment decisions")
    else:
        print(f"\n✓ Normal article volume (below threshold)")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print(" "*20 + "TrendRadar Credibility System Examples")
    print("="*80)
    
    try:
        # Run examples
        example_basic_analysis()
        example_volume_spike_detection()
        
        print("\n\n" + "="*80)
        print("Examples completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
