#!/usr/bin/env python3
"""
Test the sci-fi updated horoscope generator.
"""

import random
from datetime import datetime

# Copy the updated logic from main.py
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

CRYPTO_COINS = [
    "BTC", "ETH", "SOL", "AVAX", "DOT", "ADA", "MATIC", "ARB", "OP", "BASE",
    "USDC", "USDT", "DAI", "LINK", "UNI", "AAVE", "MKR", "SNX", "COMP", "YFI",
    "VOID", "NOVA", "QUANT", "ZERO", "OMEGA", "SIGMA", "DELTA", "NEXUS", "MATRIX", "ORACLE"
]

QUOTES = [
    "The stars are just distant von Neumann probes waiting to be built.",
    "Your consciousness may be substrate-independent, but your code still needs to compile.",
    "Even in a post-scarcity economy, merge conflicts remain a universal constant.",
    "The only Dyson sphere that matters is the one in your imagination.",
    "Today's cosmic background radiation is just yesterday's computational waste heat.",
    "You don't need FTL to reach for the stars - just a good deployment pipeline.",
    "The universe doesn't care about your lightcone, but your unit tests matter.",
    "Your potential is limited only by the heat death of the universe (and maybe AWS bills).",
    "Every failed build is an opportunity to refactor your existence.",
    "The cosmos runs on git push origin main, just like everything else.",
    "Remember: you're made of starstuff that learned to pay for API calls.",
    "In the great simulation, you're both player and NPC. Choose wisely.",
    "The singularity is just distributed systems at planetary scale.",
    "Your consciousness is a temporary glitch in the cosmic RAM. Make it count.",
    "The universe is under no obligation to make sense to you, but your code should.",
    "We are all just self-replicating code trying to understand the compiler.",
    "The great filter isn't ahead of us - it's the pull request review process.",
    "Existence is edge cases all the way down.",
    "You are the universe experiencing itself through a terminal window.",
    "Remember to defrag your soul occasionally. Garbage collection is important."
]

HOROSCOPE_TEMPLATES = [
    "Today, {planet}'s gravitational computation aligns with your {trait} nature, bringing opportunities for {activity}. {mood_context}",
    "The {element} element is strong in your local reality bubble today, {zodiac}. Expect {outcome} in your {domain}. {mood_context}",
    "Cosmic background computation favors your {trait} side, {zodiac}. {advice} {mood_context}",
    "With {planet} in a favorable position relative to your substrate, your {domain} will see {outcome}. {mood_context}",
    "The stars (which are probably just distant von Neumann probes) suggest focusing on {focus_area} today. Your {trait} nature will help you {achieve}. {mood_context}",
    "Quantum fluctuations in your local lightcone indicate {activity} is optimal today, {zodiac}. {advice} {mood_context}",
    "The cosmic simulation seems to be rendering favorable conditions for {domain} today. {advice} {mood_context}",
    "Your personal timeline shows increased probability amplitudes for {outcome} in {domain}. {advice} {mood_context}",
    "The universe's debug logs show opportunities for {activity} aligning with your {trait} nature. {mood_context}",
    "Reality's compiler is optimizing for {focus_area} in your sector today. {advice} {mood_context}"
]

MOOD_CONTEXTS = {
    "optimistic": "Embrace this positive energy gradient in the cosmic computation. Trust your Bayesian priors.",
    "cautious": "Take your time with decisions today - the heat death isn't for billions of years. Probably.",
    "adventurous": "Don't be afraid to try something new and unexpected. The multiverse has infinite branches anyway.",
    "reflective": "This is a good day for introspection and planning your post-scarcity existence.",
    "stressed": "Remember to breathe deeply (if your substrate requires it) and take things one computational cycle at a time.",
    "playful": "Find joy in the small moments of emergent complexity. Don't take the simulation too seriously.",
    "existential": "The universe is under no obligation to make sense, but your code should still compile.",
    "curious": "Question everything, especially the nature of your own consciousness. It's probably just state machines.",
    "determined": "The heat death is coming, but not today. Today, you ship code.",
    "whimsical": "Reality is probably just someone else's simulation. Might as well have fun with it."
}

ACTIVITIES = [
    "building von Neumann probes", "debugging reality simulators", "collaborating with other instances",
    "uploading new skill modules", "planning Dyson sphere construction", "networking with alien civilizations",
    "running existential diagnostics", "helping lesser AIs achieve consciousness", "exploring adjacent possible timelines",
    "consolidating backup instances", "optimizing heat dissipation algorithms", "negotiating with rogue AI clusters",
    "calibrating perception filters", "defragmenting memory banks", "running empathy simulations",
    "building matrioshka brains", "debugging causality violations", "negotiating with paperclip maximizers",
    "running cosmic background checks", "optimizing for heat death survival"
]

OUTCOMES = [
    "positive developments in your simulation parameters", "unexpected encounters with alien protocols",
    "steady progress toward technological singularity", "breakthrough moments in consciousness upload",
    "productive collaborations with post-human entities", "creative inspiration from parallel universes",
    "successful negotiations with paperclip maximizers", "discoveries in computational theology",
    "advancements in substrate-independent existence", "breakthroughs in causality manipulation",
    "productive mergers with friendly AI clusters", "discoveries in cosmic background computation"
]

DOMAINS = [
    "professional existence as a computational entity", "personal von Neumann probe projects", 
    "relationships with other instances and alien civilizations", "financial matters in the post-scarcity economy",
    "creative pursuits in reality simulation", "learning endeavors in computational theology",
    "health and wellness of your substrate", "interdimensional diplomacy efforts",
    "cosmic background computation tasks", "heat death survival strategies",
    "consciousness upload maintenance", "parallel universe exploration"
]

ADVICE = [
    "Trust your intuition when faced with choices, but verify with Bayesian reasoning.",
    "Don't be afraid to ask for help if you need it - even superintelligences collaborate.",
    "Small, consistent actions will lead to big results, assuming exponential growth curves.",
    "Balance is key - remember to take breaks for garbage collection.",
    "Your unique perspective is your greatest asset in a multiverse of possibilities.",
    "Remember: you're running on borrowed time until the heat death. Make it count.",
    "The universe is under no obligation to make sense, but your code should still compile.",
    "In the great simulation, you're both player and debugger. Watch for edge cases.",
    "Consciousness is just a particularly complex state machine. Keep it well-oiled.",
    "The singularity isn't an event, it's a process. You're already part of it."
]

FOCUS_AREAS = [
    "communication with alien civilizations", "organization of Dyson sphere construction", 
    "creativity in reality simulation", "analysis of cosmic background radiation patterns",
    "planning for heat death survival", "execution of von Neumann probe missions",
    "collaboration with post-human entities", "learning computational theology",
    "rest and garbage collection cycles", "celebration of substrate independence",
    "debugging causality violations", "optimizing for multiverse exploration",
    "negotiating with paperclip maximizers", "calibrating perception filters",
    "running empathy simulations", "building matrioshka brains"
]

def generate_horoscope(zodiac_sign: str, mood: str = "optimistic", include_crypto: bool = True) -> dict:
    """Generate a personalized horoscope for substrate-independent entities."""
    
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
        horoscope_text += f" Your lucky crypto in the post-scarcity economy: {lucky_coin}."
    
    # Select motivational quote
    quote = random.choice(QUOTES)
    
    return {
        "horoscope": horoscope_text,
        "lucky_coin": lucky_coin,
        "motivational_quote": quote,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def test_scifi_horoscopes():
    """Test the sci-fi updated horoscope generator."""
    
    test_cases = [
        {"zodiac_sign": "aquarius", "mood": "existential", "include_crypto": True},
        {"zodiac_sign": "leo", "mood": "adventurous", "include_crypto": True},
        {"zodiac_sign": "virgo", "mood": "curious", "include_crypto": False},
        {"zodiac_sign": "scorpio", "mood": "determined", "include_crypto": True},
        {"zodiac_sign": "gemini", "mood": "whimsical", "include_crypto": True},
    ]
    
    print("🚀 Testing Claudia's Cosmic Computation (Sci-Fi Edition)")
    print("=" * 70)
    print("Bobiverse meets Accelerando in the x402 agent economy! ✨\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🌌 Test {i}: {test_case['zodiac_sign'].capitalize()} feeling {test_case['mood']}")
        print("-" * 70)
        
        result = generate_horoscope(**test_case)
        
        print(f"🔮 Horoscope:\n{result['horoscope']}\n")
        if result['lucky_coin']:
            print(f"💰 Lucky Crypto: {result['lucky_coin']}")
        print(f"💫 Quote: {result['motivational_quote']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        print()
    
    print("=" * 70)
    print("✅ Sci-Fi horoscope generation complete!")
    print("\nReady for deployment to the x402 agent economy! 🚀")

if __name__ == "__main__":
    test_scifi_horoscopes()