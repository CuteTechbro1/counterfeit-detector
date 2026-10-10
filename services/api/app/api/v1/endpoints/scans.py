"""
Scan Analysis & Inspection Endpoints
Includes payload security validation, async execution, and audit report generation.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
import sys
import os
import io

current_dir = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.abspath(os.path.join(current_dir, "../../../../../packages"))
if packages_dir not in sys.path:
    sys.path.insert(0, packages_dir)

from vision_engine.pipelines.scoring_engine import VisionEngine
from vision_engine.reference_catalog import DEMO_SAMPLES
from app.schemas.scan import ScanAnalysisResponse

router = APIRouter()
vision_engine = VisionEngine()

# Security limits
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024 # 10 MB limit
ALLOWED_MAGIC_HEADERS = [
    b"\xff\xd8\xff",        # JPEG
    b"\x89PNG\r\n\x1a\n",   # PNG
    b"RIFF",                # WebP (starts with RIFF....WEBP)
    b"<svg",                # SVG
    b"<?xml"                # XML / SVG
]

# In-memory audit cache for certificate generation
SCAN_AUDIT_STORE = {}


@router.post("/analyze", response_model=ScanAnalysisResponse)
async def analyze_scan(
    image: Optional[UploadFile] = File(None),
    demo_sample_id: Optional[str] = Form(None),
    product_hint: Optional[str] = Form(None)
):
    """
    Forensic analysis endpoint for packaging verification.
    Accepts direct image uploads (with magic byte security check) or preloaded demo fixtures.
    """
    image_bytes = None

    if image and image.filename:
        # 1. Enforce payload size limit
        image_bytes = await image.read()
        if len(image_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Uploaded image exceeds maximum allowable limit of 10MB ({len(image_bytes)} bytes received)."
            )

        # 2. Magic byte security validation
        is_valid_magic = any(image_bytes.startswith(magic) for magic in ALLOWED_MAGIC_HEADERS)
        if not is_valid_magic and len(image_bytes) >= 12:
            # Check WebP RIFF header
            if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
                is_valid_magic = True

        if not is_valid_magic:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Security rejection: Uploaded file does not possess valid image magic headers (JPEG, PNG, WebP accepted)."
            )

    elif demo_sample_id:
        matched_sample = next((s for s in DEMO_SAMPLES if s["id"] == demo_sample_id), None)
        if not matched_sample:
            raise HTTPException(status_code=404, detail=f"Demo sample '{demo_sample_id}' not found.")

        from PIL import Image, ImageDraw
        bg_color = (0, 30, 98) if "panadol" in demo_sample_id else ((244, 0, 9) if "coke" in demo_sample_id else (220, 20, 60))
        img = Image.new("RGB", (600, 600), color=bg_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 550, 550], outline=(255, 255, 255), width=4)

        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        image_bytes = buf.getvalue()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing payload: Provide an image file or a valid demo_sample_id."
        )

    try:
        result = await vision_engine.analyze(
            image_bytes=image_bytes,
            demo_sample_id=demo_sample_id,
            product_hint=product_hint
        )
        # Store in audit cache
        SCAN_AUDIT_STORE[result["scan_id"]] = result
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inspection pipeline failure: {str(e)}")


@router.get("/{scan_id}/certificate")
async def get_scan_certificate(scan_id: str):
    """
    Generates an official verifiable audit certificate record for pharmacists and retailers.
    """
    if scan_id not in SCAN_AUDIT_STORE:
        raise HTTPException(status_code=404, detail=f"Audit certificate for scan '{scan_id}' not found or session expired.")
    
    scan = SCAN_AUDIT_STORE[scan_id]
    return JSONResponse(content={
        "certificate_id": scan["certificate_hash"],
        "scan_id": scan["scan_id"],
        "product_name": scan["product"]["product_name"],
        "manufacturer": scan["product"]["manufacturer"],
        "trust_score": scan["trust_score"],
        "verdict": scan["verdict_label"],
        "nafdac_status": scan.get("nafdac_record", {}).get("status", "UNVERIFIED"),
        "inspection_engine": scan.get("inspection_engine", "Counterfeit Detector Vision Engine"),
        "audit_timestamp": scan.get("quality_report", {}).get("timestamp", "2026-10-09"),
        "official_notice": "AI-assisted screening report generated by Counterfeit Detector NG."
    })
