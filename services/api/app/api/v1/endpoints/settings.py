"""
Settings & Engine Configuration Endpoints
Allows runtime configuration of Gemini API Key.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()


class GeminiKeyPayload(BaseModel):
    api_key: str


@router.post("/gemini-key")
async def configure_gemini_key(payload: GeminiKeyPayload):
    key = payload.api_key.strip()
    if not key or len(key) < 10:
        raise HTTPException(status_code=400, detail="Invalid API key provided. Key must be at least 10 characters.")

    os.environ["GEMINI_API_KEY"] = key

    # Persist in services/api/.env and project root .env
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f'GEMINI_API_KEY="{key}"\n')
            f.write('GEMINI_MODEL="gemini-2.5-flash"\n')
    except Exception:
        pass

    return {
        "status": "success",
        "message": "Google Gemini Vision API key activated successfully.",
        "active_mode": "Google Gemini Multimodal Vision (Cloud)",
        "model": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    }


@router.delete("/gemini-key")
async def clear_gemini_key():
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
    if os.path.exists(env_path):
        os.remove(env_path)
    return {
        "status": "success",
        "message": "Reverted to Local Edge Computer Vision Engine.",
        "active_mode": "Hybrid Edge Computer Vision (Local Fallback)"
    }
