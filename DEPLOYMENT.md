# Deployment Guide for Claudia's Cosmic Guidance

## Prerequisites

1. **Python 3.11+** and **pip**
2. **Docker** (optional, for containerized deployment)
3. **Render/Fly.io/Heroku** account for hosting
4. **Base network wallet** with USDC for x402 payments
5. **x402 facilitator** access (Coinbase CDP)

## Deployment Options

### Option 1: Render (Recommended for simplicity)

1. **Create a new Web Service** on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main_with_x402:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** None required for basic version
4. Deploy!

### Option 2: Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t claudia-horoscope .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 claudia-horoscope
   ```

3. Deploy to any container registry (Docker Hub, GitHub Container Registry, etc.)

### Option 3: Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main_with_x402:app --host 0.0.0.0 --port 8080 --reload
   ```

3. Test the API:
   ```bash
   curl -X POST http://localhost:8080/horoscope \
     -H "Content-Type: application/json" \
     -H "X-Mock-Payment: true" \
     -d '{"zodiac_sign": "aquarius", "mood": "optimistic"}'
   ```

## x402 Payment Setup

### 1. Update Payment Configuration

Edit `app/x402_config.py`:

```python
# Update with your actual wallet address
"pay_to": "0xYOUR_WALLET_ADDRESS_HERE",

# Optional: Adjust price (in USDC units, 6 decimals)
"price": "10000",  # 10,000 units = $0.01
```

### 2. Register with x402 Bazaar

Once deployed, register your service with the x402 Bazaar:

1. Ensure your endpoint returns proper x402 payment requirements on 402 status
2. The Bazaar will automatically discover your service when payments are processed
3. Alternatively, manually submit your endpoint to the Bazaar discovery API

### 3. Test x402 Payments

Use the x402 SDK to test payments:

```python
from x402 import x402Client
from x402.mechanisms.evm import EthAccountSigner
from eth_account import Account

# Set up client
client = x402Client()
account = Account.from_key("YOUR_PRIVATE_KEY")
register_exact_evm_client(client, EthAccountSigner(account))

# Make paid request
import httpx
async with x402HttpxClient(client) as http:
    response = await http.post(
        "https://your-horoscope-service.com/horoscope",
        json={"zodiac_sign": "aquarius"}
    )
    print(await response.json())
```

## Environment Variables

For production, consider these environment variables:

- `X402_FACILITATOR_URL`: x402 facilitator endpoint
- `X402_PAY_TO_ADDRESS`: Your wallet address for payments
- `X402_PRICE`: Price in USDC units (default: 10000)
- `ALLOW_MOCK_PAYMENTS`: Allow testing without real payments (default: false in production)

## Monitoring & Maintenance

1. **Health checks:** The `/health` endpoint returns service status
2. **Logging:** Add structured logging for payment verification
3. **Metrics:** Track usage and payment success rates
4. **Updates:** Regularly update dependencies and x402 SDK

## Security Considerations

1. **Never expose private keys** in code or environment variables
2. **Validate all inputs** to prevent injection attacks
3. **Rate limiting** to prevent abuse
4. **CORS configuration** if serving web clients
5. **HTTPS only** in production

## Troubleshooting

### Common Issues:

1. **Payment verification fails:**
   - Check x402 facilitator connectivity
   - Verify wallet has sufficient balance
   - Confirm network configuration matches Base mainnet

2. **Service not discoverable in Bazaar:**
   - Ensure `/x402-info` endpoint returns correct schema
   - Check that payments are being processed through facilitator
   - Verify x402 version compatibility

3. **High latency:**
   - Consider caching horoscope templates
   - Use CDN for static assets
   - Optimize database queries if added

## Next Steps

1. **Add database** for horoscope history and user preferences
2. **Implement caching** for frequently requested combinations
3. **Add more customization options** (language, length, style)
4. **Create web interface** for non-technical users
5. **Integrate with other x402 services** for enhanced features