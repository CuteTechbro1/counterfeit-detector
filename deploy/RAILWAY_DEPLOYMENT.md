# Railway Production Deployment Guide

This guide details how to deploy the **Counterfeit Detector** platform to [Railway](https://railway.app/).

---

## 1. Architecture Summary

| Property | Value |
| :--- | :--- |
| **Service Model** | Monorepo Unified Web Service (Backend + Static Frontend) |
| **Frontend Framework** | Semantic HTML5 SPA + Tailwind CSS (CDN) + Lucide Icons + Modern ES6+ JS |
| **Backend Framework** | FastAPI (Python 3.11) + Uvicorn ASGI |
| **Vision Engine** | Multi-factor CV Engine + Google Gemini Multimodal Vision Adapter |
| **Entrypoint File** | `services/api/app/main.py` (`app.main:app`) |
| **Startup Command** | `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2` |
| **Health Check Path** | `/api/v1/health` (HTTP 200 OK) |

---

## 2. Environment Variables

Configure these variables in your Railway project settings (**Settings** &rarr; **Variables**):

### Required Variables
| Variable | Value / Description | Default / Example |
| :--- | :--- | :--- |
| `PORT` | Web server listening port (injected automatically by Railway) | `8000` |
| `PYTHONPATH` | Python import resolution path for monorepo modules | `/app/services/api:/app/packages` (Docker) or `services/api:packages` (Nixpacks) |
| `PYTHONUNBUFFERED` | Ensures standard output is logged in real-time | `1` |

### Recommended Variables (Google Gemini Vision Integration)
| Variable | Value / Description | Default / Example |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio Gemini API Key for cloud multimodal vision | `AIzaSy...` (optional: platform falls back to Local CV if absent) |
| `GEMINI_MODEL` | Gemini vision model identifier | `gemini-2.5-flash` |
| `ENV` | Environment identifier | `production` |
| `SECRET_KEY` | Random cryptographic secret for security headers | Generate with `openssl rand -hex 32` |

---

## 3. Deployment Methods

### Option A: Deploy via GitHub (Recommended)

1. Push this repository to GitHub.
2. Log into [Railway.app](https://railway.app/).
3. Click **"New Project"** &rarr; **"Deploy from GitHub repo"**.
4. Select your `counterfeit-detector` repository.
5. Railway will detect `railway.toml` and `Dockerfile` automatically.
6. Under **Variables**, add:
   - `GEMINI_API_KEY`: `<your-gemini-key>` (optional, for Gemini Vision)
   - `PYTHONPATH`: `/app/services/api:/app/packages`
   - `PYTHONUNBUFFERED`: `1`
7. Click **Deploy**.
8. Go to **Settings** &rarr; **Networking** &rarr; click **"Generate Domain"** to obtain your live public URL (e.g. `https://counterfeit-detector-production.up.railway.app`).

---

### Option B: Deploy via Railway CLI

If deploying directly from the command line:

```bash
# 1. Install Railway CLI (if not already installed)
npm install -g @railway/cli   # or via brew install railway

# 2. Login to Railway
railway login

# 3. Link or create a new project
railway init

# 4. Set environment variables
railway variables --set PYTHONPATH="/app/services/api:/app/packages"
railway variables --set PYTHONUNBUFFERED="1"
railway variables --set GEMINI_API_KEY="AIzaSy..."

# 5. Deploy the application
railway up
```

---

## 4. Post-Deployment Verification

1. **Health Telemetry**:
   Open `https://<your-app>.up.railway.app/api/v1/health` in your browser. You should receive:
   ```json
   {
     "status": "online",
     "service": "counterfeit-detector-api",
     "version": "1.1.0-production",
     "ai_engine": {
       "gemini_vision_ready": true,
       "gemini_model": "gemini-2.5-flash",
       "active_mode": "Google Gemini Vision (gemini-2.5-flash)",
       "nafdac_database_records": 4
     }
   }
   ```

2. **Web Frontend**:
   Navigate to `https://<your-app>.up.railway.app/`. You should see the complete corporate Blue & White Product Authentication Shield.

3. **Interactive API Documentation**:
   Navigate to `https://<your-app>.up.railway.app/docs` to view Swagger UI endpoints.
