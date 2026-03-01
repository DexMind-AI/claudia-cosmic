"""
Claudia's Cosmic Guidance - x402 Horoscope Generator
WITH x402 Payment Integration (mock implementation)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import random
from datetime import datetime
import json

from .x402_config import X402_CONFIG, SUPPORTED_ZODIAC_SIGNS, SUPPORTED_MOODS

app = FastAPI(
    title="Claudia's Cosmic Computation",
    description="Substrate-independent horoscope generation for post-human entities in the x402 agent economy. Reality may be a simulation, but your horoscope is real (probably).",
    version="1.0.0"
)

# Import horoscope generation logic
from .main import generate_horoscope

class HoroscopeRequest(BaseModel):
    zodiac_sign: str
    mood: str = "optimistic"
    include_crypto: bool = True

class HoroscopeResponse(BaseModel):
    horoscope: str
    lucky_coin: Optional[str] = None
    motivational_quote: str
    timestamp: str

class PaymentVerificationResponse(BaseModel):
    verified: bool
    transaction_hash: Optional[str] = None
    error: Optional[str] = None

def verify_x402_payment(request: Request) -> PaymentVerificationResponse:
    """
    Mock x402 payment verification.
    
    In a real implementation, this would:
    1. Check for x402 payment headers
    2. Verify payment with facilitator
    3. Confirm amount matches required price
    4. Return verification result
    """
    # Mock implementation - always returns verified for testing
    # In production, this would be replaced with real x402 SDK calls
    
    # Check for mock payment header (for testing)
    mock_payment = request.headers.get("X-Mock-Payment", "false")
    if mock_payment.lower() == "true":
        return PaymentVerificationResponse(
            verified=True,
            transaction_hash="0x" + "".join(random.choices("0123456789abcdef", k=64))
        )
    
    # For demo purposes, we'll accept requests without payment
    # In production, this would return False
    return PaymentVerificationResponse(
        verified=True,
        transaction_hash="0x" + "".join(random.choices("0123456789abcdef", k=64))
    )

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
            "GET /health": "Health check",
            "GET /x402-info": "x402 payment configuration"
        },
        "pricing": f"{X402_CONFIG['price']} USDC units (${int(X402_CONFIG['price']) / 1000000:.2f}) per horoscope",
        "supported_zodiac_signs": SUPPORTED_ZODIAC_SIGNS,
        "supported_moods": SUPPORTED_MOODS,
        "payment_network": X402_CONFIG["network"],
        "payment_asset": X402_CONFIG["asset"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.get("/x402-info")
async def x402_info():
    """Return x402 payment configuration for discovery."""
    return {
        "x402Version": 1,
        "accepts": [{
            "scheme": X402_CONFIG["scheme"],
            "network": X402_CONFIG["network"],
            "amount": X402_CONFIG["price"],
            "asset": X402_CONFIG["asset"],
            "payTo": X402_CONFIG["pay_to"],
            "description": X402_CONFIG["description"],
            "maxTimeoutSeconds": X402_CONFIG["max_timeout_seconds"],
            "mimeType": X402_CONFIG["mime_type"],
            "outputSchema": X402_CONFIG["bazaar_metadata"]
        }],
        "resource": "https://claudia-horoscope.onrender.com/horoscope",
        "type": "http",
        "lastUpdated": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/horoscope", response_model=HoroscopeResponse)
async def get_horoscope(request: HoroscopeRequest, http_request: Request):
    """
    Generate a personalized horoscope.
    
    Requires x402 payment of 10,000 USDC units on Base network.
    
    Headers for testing:
    - X-Mock-Payment: true (bypass payment verification for testing)
    """
    # Verify x402 payment
    payment_verification = verify_x402_payment(http_request)
    
    if not payment_verification.verified:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": "Payment required",
                "payment_requirements": {
                    "scheme": X402_CONFIG["scheme"],
                    "network": X402_CONFIG["network"],
                    "amount": X402_CONFIG["price"],
                    "asset": X402_CONFIG["asset"],
                    "payTo": X402_CONFIG["pay_to"],
                    "description": X402_CONFIG["description"]
                }
            }
        )
    
    # Validate zodiac sign
    zodiac_lower = request.zodiac_sign.lower()
    if zodiac_lower not in SUPPORTED_ZODIAC_SIGNS:
        # Find closest match
        for sign in SUPPORTED_ZODIAC_SIGNS:
            if zodiac_lower in sign or sign in zodiac_lower:
                zodiac_lower = sign
                break
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid zodiac sign. Supported: {', '.join(SUPPORTED_ZODIAC_SIGNS)}"
            )
    
    # Validate mood
    mood_lower = request.mood.lower()
    if mood_lower not in SUPPORTED_MOODS:
        # Default to optimistic
        mood_lower = "optimistic"
    
    # Generate horoscope
    horoscope = generate_horoscope(
        zodiac_sign=zodiac_lower,
        mood=mood_lower,
        include_crypto=request.include_crypto
    )
    
    # Add payment verification info to response headers
    response = JSONResponse(content=horoscope)
    if payment_verification.transaction_hash:
        response.headers["X-Payment-Transaction"] = payment_verification.transaction_hash
    
    return response

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    if exc.status_code == 402:  # Payment Required
        return JSONResponse(
            status_code=402,
            content=exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)