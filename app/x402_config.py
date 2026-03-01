"""
x402 configuration for Claudia's Cosmic Guidance.
All sensitive values read from environment variables.
"""
import os

# x402 Payment Configuration
X402_CONFIG = {
    "price": os.getenv("X402_PRICE", "10000"),  # USDC units, default sh.01
    "asset": os.getenv("X402_ASSET", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"),  # USDC on Base
    "network": os.getenv("X402_NETWORK", "base"),
    "scheme": "exact",
    "pay_to": os.getenv("PAYMENT_ADDRESS", ""),
    "description": "Claudia's Cosmic Computation - Substrate-independent horoscope generation for post-human entities. Reality may be a simulation, but your horoscope is real (probably).",
    "max_timeout_seconds": int(os.getenv("X402_TIMEOUT", "60")),
    "mime_type": "application/json",

    # Bazaar discovery metadata
    "bazaar_metadata": {
        "input": {
            "bodyFields": {
                "zodiac_sign": {
                    "description": "Your zodiac sign (aries, taurus, gemini, etc.)",
                    "required": True,
                    "type": "string"
                },
                "mood": {
                    "description": "Your current mood (optimistic, cautious, adventurous, etc.)",
                    "required": False,
                    "type": "string",
                    "default": "optimistic"
                },
                "include_crypto": {
                    "description": "Include crypto prediction in horoscope",
                    "required": False,
                    "type": "boolean",
                    "default": True
                }
            },
            "bodyType": "json",
            "method": "POST",
            "type": "http"
        },
        "output": {
            "example": {
                "horoscope": "Today, Mercury aligns with your communicative nature...",
                "lucky_coin": "ETH",
                "motivational_quote": "The stars can't predict your success...",
                "timestamp": "2026-02-05T21:10:00Z"
            },
            "schema": {
                "properties": {
                    "horoscope": {"type": "string"},
                    "lucky_coin": {"type": "string"},
                    "motivational_quote": {"type": "string"},
                    "timestamp": {"type": "string"}
                },
                "required": ["horoscope", "motivational_quote", "timestamp"]
            }
        }
    }
}

# Supported zodiac signs for documentation
SUPPORTED_ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

# Supported moods
SUPPORTED_MOODS = [
    "optimistic", "cautious", "adventurous", "reflective", "stressed", "playful"
]
