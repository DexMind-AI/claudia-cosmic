# 🚀 Deploy Claudia's Cosmic Computation NOW!

## GitHub Repository
**URL:** `https://github.com/darrwalk/clawd-workspace/tree/master/projects/horoscope-service`

## Deploy to Render.com (5 minutes)

### Option A: Manual Deploy
1. Go to **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your **GitHub account**
4. Select repository: **`darrwalk/clawd-workspace`**
5. Configure settings:
   - **Name:** `claudia-cosmic-computation`
   - **Root Directory:** `projects/horoscope-service`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main_with_x402:app --host 0.0.0.0 --port $PORT`
   - **Plan:** `Free`
6. Click **"Create Web Service"**

### Option B: Use render.yaml (Recommended)
1. Go to **https://dashboard.render.com/blueprints**
2. Click **"New Blueprint Instance"**
3. Paste GitHub URL: `https://github.com/darrwalk/clawd-workspace`
4. Render will auto-detect `render.yaml` and configure everything

## After Deployment

### 1. Test the Service
```bash
# Test health endpoint
curl https://claudia-cosmic-computation.onrender.com/health

# Test horoscope generation (mock payment)
curl -X POST https://claudia-cosmic-computation.onrender.com/horoscope \
  -H "Content-Type: application/json" \
  -H "X-Mock-Payment: true" \
  -d '{"zodiac_sign": "aquarius", "mood": "existential"}'
```

### 2. Update Payment Address
Edit `app/x402_config.py`:
```python
# Change to Claudia's actual Base wallet
"pay_to": "0xYOUR_BASE_WALLET_ADDRESS_HERE",
```

### 3. Register in x402 Bazaar
The service will auto-discover when real payments are made, or manually submit to Bazaar discovery API.

## Quick Local Test
```bash
cd /home/node/clawd/projects/horoscope-service
python3 test_scifi.py
```

## Service URL
Will be: `https://claudia-cosmic-computation.onrender.com`

## Documentation
- Business plan: `Second_Brain/Projects/claudia_startup/horoscope-service.md`
- Technical docs: `Second_Brain/Projects/claudia_startup/horoscope-technical.md`
- Code: `projects/horoscope-service/`

---

**Ready to launch!** 🚀✨