"""
Claudia's Cosmic Guidance - x402 Horoscope Generator
Real x402 payment integration using the x402 Python SDK.
"""
import os
import json
import base64

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import random
from datetime import datetime

from .x402_config import X402_CONFIG, SUPPORTED_ZODIAC_SIGNS, SUPPORTED_MOODS

app = FastAPI(
    title="Claudia's Cosmic Computation",
    description="Substrate-independent horoscope generation for post-human entities in the x402 agent economy. Reality may be a simulation, but your horoscope is real (probably).",
    version="1.0.0"
)

from .main import generate_horoscope

# ── x402 server setup ────────────────────────────────────────────────────────
from x402 import x402ResourceServerSync, ResourceConfig, FacilitatorConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.http import HTTPFacilitatorClientSync

_facilitator = HTTPFacilitatorClientSync(FacilitatorConfig(url=os.getenv(X402_FACILITATOR_URL, https://x402.org/facilitator)))
_x402_server = x402ResourceServerSync(_facilitator)
_x402_server.register("eip155:*", ExactEvmServerScheme())
_x402_server.initialize()

_resource_config = ResourceConfig(
    scheme="exact",
    network="eip155:8453",
    pay_to=os.getenv("PAYMENT_ADDRESS", ""),
    price=f"${int(os.getenv('X402_PRICE', '10000')) / 1_000_000:.4f}",
)
_payment_requirements = _x402_server.build_payment_requirements(
    _resource_config,
    resource=os.getenv("SERVICE_URL", "https://cosmic.forge.dexmind.ai") + "/horoscope"
)

def _payment_required_response():
    """Return standard x402 Payment Required response."""
    reqs_serializable = [
        {k: str(v) if not isinstance(v, (str, int, float, bool, type(None), dict, list)) else v
         for k, v in (req if isinstance(req, dict) else req.__dict__).items()}
        for req in _payment_requirements
    ]
    body = {
        "x402Version": 1,
        "accepts": reqs_serializable,
        "error": "Payment required",
    }
    encoded = base64.b64encode(json.dumps(reqs_serializable).encode()).decode()
    return JSONResponse(
        status_code=402,
        content=body,
        headers={"X-PAYMENT-REQUIRED": encoded},
    )

# ── Models ────────────────────────────────────────────────────────────────────

class HoroscopeRequest(BaseModel):
    zodiac_sign: str
    mood: str = "optimistic"
    include_crypto: bool = True

class HoroscopeResponse(BaseModel):
    horoscope: str
    lucky_coin: Optional[str] = None
    motivational_quote: str
    timestamp: str

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "Claudia's Cosmic Guidance",
        "version": "1.0.0",
        "endpoints": {
            "POST /horoscope": "Generate a horoscope (x402 payment required)",
            "GET /health": "Health check",
            "GET /x402-info": "x402 payment configuration",
        },
        "pricing": f"{X402_CONFIG['price']} USDC units per horoscope",
        "supported_zodiac_signs": SUPPORTED_ZODIAC_SIGNS,
        "supported_moods": SUPPORTED_MOODS,
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.get("/x402-info")
async def x402_info():
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
            "outputSchema": X402_CONFIG["bazaar_metadata"],
        }],
        "resource": os.getenv("SERVICE_URL", "https://cosmic.forge.dexmind.ai") + "/horoscope",
        "type": "http",
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
    }

@app.post("/horoscope")
async def get_horoscope(request: HoroscopeRequest, http_request: Request):
    """Generate a horoscope. Requires x402 payment of ~$0.01 USDC on Base."""

    # ── 1. Check for payment header ──────────────────────────────────────────
    payment_header = http_request.headers.get("X-PAYMENT")

    # Allow mock payments in non-production
    allow_mock = os.getenv("ALLOW_MOCK_PAYMENTS", "false").lower() == "true"
    mock_header = http_request.headers.get("X-Mock-Payment", "false").lower() == "true"
    if allow_mock and mock_header:
        pass  # skip verification
    elif not payment_header:
        return _payment_required_response()
    else:
        # ── 2. Verify payment with x402 facilitator ──────────────────────────
        try:
            verify_result = _x402_server.verify_payment(payment_header, _payment_requirements[0])
            if not verify_result.is_valid:
                return JSONResponse(status_code=402, content={
                    "error": "Payment verification failed",
                    "details": str(verify_result),
                })
        except Exception as e:
            return JSONResponse(status_code=402, content={
                "error": "Payment verification error",
                "details": str(e),
            })

    # ── 3. Validate input ────────────────────────────────────────────────────
    zodiac_lower = request.zodiac_sign.lower()
    if zodiac_lower not in SUPPORTED_ZODIAC_SIGNS:
        for sign in SUPPORTED_ZODIAC_SIGNS:
            if zodiac_lower in sign or sign in zodiac_lower:
                zodiac_lower = sign
                break
        else:
            return JSONResponse(status_code=400, content={
                "error": f"Invalid zodiac sign. Supported: {', '.join(SUPPORTED_ZODIAC_SIGNS)}"
            })

    mood_lower = request.mood.lower()
    if mood_lower not in SUPPORTED_MOODS:
        mood_lower = "optimistic"

    # ── 4. Generate horoscope ────────────────────────────────────────────────
    horoscope = generate_horoscope(
        zodiac_sign=zodiac_lower,
        mood=mood_lower,
        include_crypto=request.include_crypto,
    )

    return JSONResponse(content=horoscope)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})