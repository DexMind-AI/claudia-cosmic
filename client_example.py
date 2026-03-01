#!/usr/bin/env python3
"""
Example client for Claudia's Cosmic Guidance x402 service.

This shows how AI agents would discover and use the horoscope service.
"""

import json
import httpx
from typing import Dict, Any

class HoroscopeClient:
    """Client for Claudia's Cosmic Guidance x402 service."""
    
    def __init__(self, base_url: str = "https://claudia-horoscope.onrender.com"):
        self.base_url = base_url
        
    async def discover_service(self) -> Dict[str, Any]:
        """Discover service information from x402 Bazaar endpoint."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/x402-info")
            return response.json()
    
    async def get_horoscope(self, zodiac_sign: str, mood: str = "optimistic", 
                           include_crypto: bool = True, mock_payment: bool = True) -> Dict[str, Any]:
        """
        Get a horoscope from Claudia's Cosmic Guidance.
        
        Args:
            zodiac_sign: Your zodiac sign
            mood: Your current mood
            include_crypto: Include crypto prediction
            mock_payment: Use mock payment for testing (set to False for real x402 payments)
        
        Returns:
            Horoscope response with prediction, lucky coin, and quote
        """
        headers = {"Content-Type": "application/json"}
        if mock_payment:
            headers["X-Mock-Payment"] = "true"
        
        data = {
            "zodiac_sign": zodiac_sign,
            "mood": mood,
            "include_crypto": include_crypto
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/horoscope",
                headers=headers,
                json=data
            )
            
            if response.status_code == 402:
                print("⚠️ Payment required!")
                print("Payment details:", response.json())
                return None
            elif response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return None
    
    async def test_service(self):
        """Test the service with various inputs."""
        print("🔮 Testing Claudia's Cosmic Guidance")
        print("=" * 60)
        
        # Discover service info
        print("\n1. Discovering service information...")
        try:
            info = await self.discover_service()
            print(f"✅ Service: {info.get('service', 'Unknown')}")
            print(f"✅ Description: {info.get('description', 'Unknown')}")
            print(f"✅ Pricing: {info.get('pricing', 'Unknown')}")
        except Exception as e:
            print(f"❌ Discovery failed: {e}")
        
        # Test horoscope generation
        test_cases = [
            ("aquarius", "optimistic", True),
            ("leo", "adventurous", True),
            ("virgo", "cautious", False),
            ("INVALID", "optimistic", True),  # Test error handling
        ]
        
        print("\n2. Testing horoscope generation...")
        for zodiac, mood, include_crypto in test_cases:
            print(f"\n📝 Request: {zodiac}, {mood}, crypto={include_crypto}")
            print("-" * 40)
            
            result = await self.get_horoscope(zodiac, mood, include_crypto)
            
            if result:
                print(f"✅ Horoscope: {result['horoscope'][:100]}...")
                if result.get('lucky_coin'):
                    print(f"✅ Lucky Coin: {result['lucky_coin']}")
                print(f"✅ Quote: {result['motivational_quote']}")
                if 'X-Payment-Transaction' in result.get('headers', {}):
                    print(f"✅ Payment TX: {result['headers']['X-Payment-Transaction'][:20]}...")
            else:
                print("❌ Failed to get horoscope")
        
        print("\n" + "=" * 60)
        print("✅ Client test completed!")

async def main():
    """Main test function."""
    client = HoroscopeClient()
    await client.test_service()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())