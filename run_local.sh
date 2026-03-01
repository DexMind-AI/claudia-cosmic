#!/bin/bash
# Quick local test script for Claudia's Cosmic Computation

echo "🚀 Starting Claudia's Cosmic Computation locally..."
echo "=============================================="

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn pydantic httpx
else
    source venv/bin/activate
fi

# Test horoscope generation
echo ""
echo "🧪 Testing horoscope generation..."
python3 test_scifi.py

echo ""
echo "🌐 Starting local server..."
echo "Press Ctrl+C to stop"
echo ""
echo "API endpoints:"
echo "  http://localhost:8080/          - Service info"
echo "  http://localhost:8080/health    - Health check"
echo "  http://localhost:8080/x402-info - x402 configuration"
echo ""
echo "Test with:"
echo '  curl -X POST http://localhost:8080/horoscope \'
echo '    -H "Content-Type: application/json" \'
echo '    -H "X-Mock-Payment: true" \'
echo '    -d '\''{"zodiac_sign": "aquarius", "mood": "existential"}'\'''

# Start the server
uvicorn app.main_with_x402:app --host 0.0.0.0 --port 8080 --reload