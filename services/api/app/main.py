"""
Counterfeit Detector Backend API Entrypoint
Serves REST API v1 and Mounts Web Frontend Application
Includes Security Headers Middleware and Gemini Readiness Telemetry.
"""

import sys
import os
from dotenv import load_dotenv

# Ensure packages directory is discoverable and load environment variables
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PACKAGES_DIR = os.path.join(PROJECT_ROOT, "packages")
if PACKAGES_DIR not in sys.path:
    sys.path.insert(0, PACKAGES_DIR)

# Load .env from project root or local api directory
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from app.api.v1.router import api_router
from vision_engine.adapters.gemini_vision_adapter import GeminiVisionAdapter
from vision_engine.nafdac_registry import NAFDAC_DATABASE

app = FastAPI(
    title="Counterfeit Detector API",
    description="AI and Computer Vision API for verifying Nigerian pharmaceuticals and FMCG products.",
    version="1.1.0-production"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# Include v1 API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/api/v1/health", tags=["Health"])
def health_check():
    gemini_adapter = GeminiVisionAdapter()
    is_ready = gemini_adapter.is_configured()
    return {
        "status": "online",
        "service": "counterfeit-detector-api",
        "version": "1.1.0-production",
        "ai_engine": {
            "gemini_vision_ready": is_ready,
            "gemini_model": gemini_adapter.model,
            "active_mode": f"Google Gemini Vision ({gemini_adapter.model})" if is_ready else "Hybrid Edge Computer Vision (Local Fallback)",
            "nafdac_database_records": len(NAFDAC_DATABASE)
        },
        "supported_products": [
            "Panadol 500mg Tablets (GSK/Haleon)",
            "Coca-Cola 50cl PET (NBC)",
            "Colgate Maximum Cavity 140g"
        ]
    }


# Path to web frontend static files
WEB_PUBLIC_DIR = os.path.abspath(
    os.path.join(PROJECT_ROOT, "apps/web/public")
)

if os.path.exists(WEB_PUBLIC_DIR):
    assets_dir = os.path.join(WEB_PUBLIC_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_spa():
        index_file = os.path.join(WEB_PUBLIC_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Counterfeit Detector API is active. Web frontend index.html not yet built."}
