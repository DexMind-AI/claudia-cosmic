#!/usr/bin/env python3
"""
Test script for Claudia's Cosmic Guidance horoscope generator.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import generate_horoscope

def test_horoscope_generation():
    """Test the horoscope generator with various inputs."""
    
    test_cases = [
        {"zodiac_sign": "aquarius", "mood": "optimistic", "include_crypto": True},
        {"zodiac_sign": "leo", "mood": "adventurous", "include_crypto": True},
        {"zodiac_sign": "virgo", "mood": "cautious", "include_crypto": False},
        {"zodiac_sign": "scorpio", "mood": "reflective", "include_crypto": True},
        {"zodiac_sign": "gemini", "mood": "playful", "include_crypto": True},
        {"zodiac_sign": "INVALID", "mood": "optimistic", "include_crypto": True},  # Test invalid sign
    ]
    
    print("🧪 Testing Claudia's Cosmic Guidance Horoscope Generator")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case}")
        print("-" * 40)
        
        try:
            result = generate_horoscope(**test_case)
            print(f"✅ Success!")
            print(f"Horoscope: {result['horoscope']}")
            if result['lucky_coin']:
                print(f"Lucky Coin: {result['lucky_coin']}")
            print(f"Quote: {result['motivational_quote']}")
            print(f"Timestamp: {result['timestamp']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_horoscope_generation()