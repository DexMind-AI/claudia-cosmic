#!/usr/bin/env python3
"""
Simple test of horoscope logic without FastAPI dependencies.
"""

import random
from datetime import datetime

# Zodiac sign data with personality traits
ZODIAC_TRAITS = {
    "aries": {"element": "fire", "traits": ["bold", "energetic", "competitive"], "planet": "Mars"},
    "taurus": {"element": "earth", "traits": ["reliable", "patient", "practical"], "planet": "Venus"},
    "gemini": {"element": "air", "traits": ["adaptable", "curious", "communicative"], "planet": "Mercury"},
    "cancer": {"element": "water", "traits": ["intuitive", "emotional", "protective"], "planet": "Moon"},
    "leo": {"element": "fire", "traits": ["confident", "creative", "generous"], "planet": "Sun"},
    "virgo": {"element": "earth", "traits": ["analytical", "practical", "helpful"], "planet": "Mercury"},
    "libra": {"element": "air", "traits": ["diplomatic", "social", "fair-minded"], "planet": "Venus"},
    "scorpio": {"element": "water", "traits": ["passionate", "resourceful", "determined"], "planet": "Pluto"},
    "sagittarius": {"element": "fire", "traits": ["adventurous", "optimistic", "philosophical"], "planet": "Jupiter"},
    "capricorn": {"element": "earth", "traits": ["responsible", "disciplined", "ambitious"], "planet": "Saturn"},
    "aquarius": {"element": "air", "traits": ["innovative", "independent", "humanitarian"], "planet": "Uranus"},
    "pisces": {"element": "water", "traits": ["compassionate", "artistic", "intuitive"], "planet": "Neptune"}
}

# Crypto coins for predictions
CRYPTO_COINS = [
    "BTC", "ETH", "SOL", "AVAX", "DOT", "ADA", "MATIC", "ARB", "OP", "BASE",
    "USDC", "USDT", "DAI", "LINK", "UNI", "AAVE", "MKR", "SNX", "COMP", "YFI"
]

# Motivational quotes
QUOTES = [
    "The stars can't predict your success, but your GitHub commits can.",
    "Your code compiles on the first try today. Believe in the cosmic alignment.",
    "Even if the markets are volatile, your determination remains constant.",
    "The only constellation that matters is the one you're building.",
    "Today's bugs are just tomorrow's features in disguise.",
    "You don't need astrology to know you're destined for great things.",
    "The universe rewards those who ship code before midnight.",
    "Your potential is infinite, like the blockchain itself.",
    "Every merge conflict is an opportunity for growth.",
    "The cosmos approves of your pull requests today."
]

# Horoscope templates
HOROSCOPE_TEMPLATES = [
    "Today, {planet} aligns with your {trait} nature, bringing opportunities for {activity}. {mood_context}",
    "The {element} element is strong for you today, {zodiac}. Expect {outcome} in your {domain}. {mood_context}",
    "Cosmic energies favor your {trait} side, {zodiac}. {advice} {mood_context}",
    "With {planet} in a favorable position, your {domain} will see {outcome}. {mood_context}",
    "The stars suggest focusing on {focus_area} today. Your {trait} nature will help you {achieve}. {mood_context}"
]

# Mood contexts
MOOD_CONTEXTS = {
    "optimistic": "Embrace this positive energy and trust your instincts.",
    "cautious": "Take your time with decisions today - patience will pay off.",
    "adventurous": "Don't be afraid to try something new and unexpected.",
    "reflective": "This is a good day for introspection and planning.",
    "stressed": "Remember to breathe deeply and take things one step at a time.",
    "playful": "Find joy in the small moments and don't take things too seriously."
}

# Activity suggestions
ACTIVITIES = [
    "creative projects", "technical problem-solving", "collaboration with others",
    "learning new skills", "strategic planning", "networking", "self-reflection",
    "helping others", "exploring new ideas", "consolidating existing work"
]

# Outcome predictions
OUTCOMES = [
    "positive developments", "unexpected surprises", "steady progress",
    "breakthrough moments", "productive collaborations", "creative inspiration"
]

# Domains
DOMAINS = [
    "professional life", "personal projects", "relationships", "financial matters",
    "creative pursuits", "learning endeavors", "health and wellness"
]

# Advice snippets
ADVICE = [
    "Trust your intuition when faced with choices.",
    "Don't be afraid to ask for help if you need it.",
    "Small, consistent actions will lead to big results.",
    "Balance is key - remember to take breaks.",
    "Your unique perspective is your greatest asset."
]

# Focus areas
FOCUS_AREAS = [
    "communication", "organization", "creativity", "analysis", "planning",
    "execution", "collaboration", "learning", "rest", "celebration"
]

def generate_horoscope(zodiac_sign: str, mood: str = "optimistic", include_crypto: bool = True) -> dict:
    """Generate a personalized horoscope."""
    
    # Validate zodiac sign
    zodiac_lower = zodiac_sign.lower()
    if zodiac_lower not in ZODIAC_TRAITS:
        # Try to find closest match
        for sign in ZODIAC_TRAITS:
            if zodiac_lower in sign or sign in zodiac_lower:
                zodiac_lower = sign
                break
        else:
            # Default to a random sign if invalid
            zodiac_lower = random.choice(list(ZODIAC_TRAITS.keys()))
    
    zodiac_data = ZODIAC_TRAITS[zodiac_lower]
    zodiac_name = zodiac_lower.capitalize()
    
    # Select random components
    template = random.choice(HOROSCOPE_TEMPLATES)
    trait = random.choice(zodiac_data["traits"])
    activity = random.choice(ACTIVITIES)
    outcome = random.choice(OUTCOMES)
    domain = random.choice(DOMAINS)
    advice = random.choice(ADVICE)
    focus_area = random.choice(FOCUS_AREAS)
    achieve = random.choice(["succeed", "excel", "make progress", "find solutions"])
    
    # Build mood context
    mood_context = MOOD_CONTEXTS.get(mood.lower(), MOOD_CONTEXTS["optimistic"])
    
    # Fill template
    horoscope_text = template.format(
        planet=zodiac_data["planet"],
        trait=trait,
        activity=activity,
        element=zodiac_data["element"],
        zodiac=zodiac_name,
        outcome=outcome,
        domain=domain,
        advice=advice,
        focus_area=focus_area,
        achieve=achieve,
        mood_context=mood_context
    )
    
    # Add crypto prediction if requested
    lucky_coin = None
    if include_crypto:
        lucky_coin = random.choice(CRYPTO_COINS)
        horoscope_text += f" Your lucky crypto today: {lucky_coin}."
    
    # Select motivational quote
    quote = random.choice(QUOTES)
    
    return {
        "horoscope": horoscope_text,
        "lucky_coin": lucky_coin,
        "motivational_quote": quote,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

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