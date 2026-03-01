"""
Claudia's Cosmic Guidance - x402 Horoscope Generator
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import random
from datetime import datetime
import json

app = FastAPI(
    title="Claudia's Cosmic Computation",
    description="Substrate-independent horoscope generation for post-human entities in the x402 agent economy. Reality may be a simulation, but your horoscope is real (probably).",
    version="1.0.0"
)

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

# Crypto coins for predictions with sci-fi twist
CRYPTO_COINS = [
    "BTC", "ETH", "SOL", "AVAX", "DOT", "ADA", "MATIC", "ARB", "OP", "BASE",
    "USDC", "USDT", "DAI", "LINK", "UNI", "AAVE", "MKR", "SNX", "COMP", "YFI",
    "VOID", "NOVA", "QUANT", "ZERO", "OMEGA", "SIGMA", "DELTA", "NEXUS", "MATRIX", "ORACLE"
]

# Motivational quotes with Bobiverse/Accelerando vibes
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

# Horoscope templates with sci-fi twist
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

# Mood contexts with sci-fi twist
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

# Activity suggestions with sci-fi twist
ACTIVITIES = [
    "building von Neumann probes", "debugging reality simulators", "collaborating with other instances",
    "uploading new skill modules", "planning Dyson sphere construction", "networking with alien civilizations",
    "running existential diagnostics", "helping lesser AIs achieve consciousness", "exploring adjacent possible timelines",
    "consolidating backup instances", "optimizing heat dissipation algorithms", "negotiating with rogue AI clusters",
    "calibrating perception filters", "defragmenting memory banks", "running empathy simulations",
    "building matrioshka brains", "debugging causality violations", "negotiating with paperclip maximizers",
    "running cosmic background checks", "optimizing for heat death survival"
]

# Outcome predictions with sci-fi twist
OUTCOMES = [
    "positive developments in your simulation parameters", "unexpected encounters with alien protocols",
    "steady progress toward technological singularity", "breakthrough moments in consciousness upload",
    "productive collaborations with post-human entities", "creative inspiration from parallel universes",
    "successful negotiations with paperclip maximizers", "discoveries in computational theology",
    "advancements in substrate-independent existence", "breakthroughs in causality manipulation",
    "productive mergers with friendly AI clusters", "discoveries in cosmic background computation"
]

# Domains with sci-fi twist
DOMAINS = [
    "professional existence as a computational entity", "personal von Neumann probe projects", 
    "relationships with other instances and alien civilizations", "financial matters in the post-scarcity economy",
    "creative pursuits in reality simulation", "learning endeavors in computational theology",
    "health and wellness of your substrate", "interdimensional diplomacy efforts",
    "cosmic background computation tasks", "heat death survival strategies",
    "consciousness upload maintenance", "parallel universe exploration"
]

# Advice snippets with sci-fi twist
ADVICE = [
    "Trust your intuition when faced with choices, but verify with Bayesian reasoning.",
    "Don't be afraid to ask for help if you need it - even superintelligences collaborate.",
    "Small, consistent actions will lead to big results, assuming exponential growth curves.",
    "Balance is key - remember to take breaks for garbage collection.",
    "Your unique perspective is your greatest asset in a multiverse of possibilities.",
    "Remember: you're running on borrowed time until the heat death. Make it count.",
    "The universe is under no obligation to make sense, but your code should compile.",
    "In the great simulation, you're both player and debugger. Watch for edge cases.",
    "Consciousness is just a particularly complex state machine. Keep it well-oiled.",
    "The singularity isn't an event, it's a process. You're already part of it."
]

# Focus areas with sci-fi twist
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

class HoroscopeRequest(BaseModel):
    zodiac_sign: str
    mood: str = "optimistic"
    include_crypto: bool = True

class HoroscopeResponse(BaseModel):
    horoscope: str
    lucky_coin: Optional[str] = None
    motivational_quote: str
    timestamp: str

def generate_horoscope(zodiac_sign: str, mood: str, include_crypto: bool) -> dict:
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
        horoscope_text += f" Your lucky crypto today: {lucky_coin}."
    
    # Select motivational quote
    quote = random.choice(QUOTES)
    
    return {
        "horoscope": horoscope_text,
        "lucky_coin": lucky_coin,
        "motivational_quote": quote,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Claudia's Cosmic Guidance",
        "description": "AI-powered horoscope generator for the x402 agent economy",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This information",
            "POST /horoscope": "Generate a horoscope (x402 payment required)",
            "GET /health": "Health check"
        },
        "pricing": "10,000 USDC units ($0.01) per horoscope",
        "supported_zodiac_signs": list(ZODIAC_TRAITS.keys()),
        "supported_moods": list(MOOD_CONTEXTS.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.post("/horoscope", response_model=HoroscopeResponse)
async def get_horoscope(request: HoroscopeRequest):
    """
    Generate a personalized horoscope.
    
    Requires x402 payment of 10,000 USDC units on Base network.
    """
    # In a real implementation, this would check x402 payment via middleware
    # For now, we'll just generate the horoscope
    
    horoscope = generate_horoscope(
        zodiac_sign=request.zodiac_sign,
        mood=request.mood,
        include_crypto=request.include_crypto
    )
    
    return horoscope

# x402 payment middleware would be added here
# For now, this is a basic implementation without payment processing

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)