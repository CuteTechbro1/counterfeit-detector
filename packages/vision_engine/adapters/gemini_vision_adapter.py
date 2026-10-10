"""
Gemini Multimodal Vision API Adapter
Connects Counterfeit Detector to Google Gemini Vision for packaging forensics.
Maps responses into trust_score, risk_level, detected_issues, authenticity_indicators, and explanation.
Provides rich routing logging for verification of Gemini vs local fallback.
"""

import os
import base64
import json
import time
import logging
from typing import Optional, Dict, Any, List
import httpx

# Dedicated vision router logger for clear console & file telemetry
logger = logging.getLogger("counterfeit_detector.vision_router")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class GeminiVisionAdapter:
    """
    Adapter for Google Gemini Vision (e.g. gemini-2.5-flash or gemini-1.5-flash).
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    @property
    def endpoint(self) -> str:
        return f"{self.base_url}/{self.model}:generateContent"

    def is_configured(self) -> bool:
        """Checks if GEMINI_API_KEY is present and non-empty."""
        key = self.api_key or os.getenv("GEMINI_API_KEY")
        return bool(key and len(key.strip()) > 8)

    async def inspect_packaging(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        product_hint: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Sends packaging image to Google Gemini Vision.
        Maps the response into:
        - trust_score
        - risk_level
        - detected_issues
        - authenticity_indicators
        - explanation
        """
        active_key = self.api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or not self.is_configured():
            logger.info(
                "[VISION_ROUTER] [LOCAL_FALLBACK] GEMINI_API_KEY not configured in environment. "
                "Routing request to Local Edge Computer Vision Engine."
            )
            return None

        t0 = time.time()
        logger.info(
            f"[VISION_ROUTER] [GEMINI_VISION] Initiating forensic verification via Google Gemini ({self.model}). "
            f"Image payload size: {len(image_bytes)} bytes | MIME: {mime_type} | Hint: '{product_hint or 'Auto-Detect'}'"
        )

        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        system_instruction = (
            "You are a forensic packaging authenticity specialist verifying consumer goods in Nigeria. "
            "You inspect packaging against official standards for: "
            "1. Panadol 500mg (Haleon / GSK Nigeria, NAFDAC: 04-0244) "
            "2. Coca-Cola 50cl PET (Nigerian Bottling Company, NAFDAC: 01-0138) "
            "3. Colgate Maximum Cavity Protection 140g (NAFDAC: 02-4019). "
            "Analyze: NAFDAC registration numbers, logo typography, color gamut, holographic seals, cap drop rings, "
            "laser dot-matrix batch neck etchings, and crimp lot debossing. "
            "Return output STRICTLY as valid JSON matching the requested schema."
        )

        prompt_text = (
            f"Forensically inspect this packaging image. Product hint: '{product_hint or 'Auto'}'\n"
            "Return JSON matching this exact structure:\n"
            "{\n"
            '  "identified_sku": "panadol-500mg-tablet" | "coca-cola-50cl-pet" | "colgate-maximum-cavity-140g" | "unknown",\n'
            '  "trust_score": <integer from 0 to 100>,\n'
            '  "risk_level": "LOW_RISK" | "MEDIUM_RISK" | "HIGH_RISK",\n'
            '  "detected_issues": [\n'
            '    {\n'
            '      "severity": "CRITICAL" | "WARNING" | "INFO",\n'
            '      "title": "<short issue title>",\n'
            '      "detail": "<forensic defect description>",\n'
            '      "bounding_box": [ymin, xmin, ymax, xmax]\n'
            '    }\n'
            '  ],\n'
            '  "authenticity_indicators": [\n'
            '    "<positive indicator observed, e.g. Valid NAFDAC Reg syntax>",\n'
            '    "<positive indicator observed, e.g. Intact cap drop ring seal>"\n'
            '  ],\n'
            '  "explanation": "<detailed summary explanation of trust score findings>",\n'
            '  "detected_nafdac": "<extracted NAFDAC number or NOT_FOUND>",\n'
            '  "tamper_seal_intact": <true or false>\n'
            "}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_instruction + "\n\n" + prompt_text},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": b64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        }

        url = f"{self.endpoint}?key={active_key}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                latency_ms = int((time.time() - t0) * 1000)

                if res.status_code == 200:
                    resp_json = res.json()
                    candidates = resp_json.get("candidates", [])
                    if candidates:
                        raw_text = candidates[0]["content"]["parts"][0]["text"]
                        parsed = json.loads(raw_text)

                        # Validate and normalize core mapped fields
                        trust_score = max(0, min(100, int(parsed.get("trust_score", 50))))
                        risk_level = str(parsed.get("risk_level", "MEDIUM_RISK")).upper()
                        if risk_level not in ["LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"]:
                            risk_level = "LOW_RISK" if trust_score >= 85 else ("MEDIUM_RISK" if trust_score >= 60 else "HIGH_RISK")

                        detected_issues = parsed.get("detected_issues", [])
                        authenticity_indicators = parsed.get("authenticity_indicators", [])
                        explanation = parsed.get("explanation", "Packaging analysis completed via Gemini Vision.")

                        logger.info(
                            f"[VISION_ROUTER] [GEMINI_VISION] Success ({latency_ms}ms). "
                            f"Model: {self.model} | Trust Score: {trust_score}/100 | Risk: {risk_level} | "
                            f"Issues Detected: {len(detected_issues)} | Indicators: {len(authenticity_indicators)}"
                        )

                        return {
                            "engine_used": "GEMINI_VISION",
                            "engine_details": f"Google Gemini Vision ({self.model})",
                            "engine_routing_log": f"GEMINI_VISION: Authenticated inspection performed by {self.model} in {latency_ms}ms.",
                            "identified_sku": parsed.get("identified_sku"),
                            "trust_score": trust_score,
                            "risk_level": risk_level,
                            "detected_issues": detected_issues,
                            "authenticity_indicators": authenticity_indicators,
                            "explanation": explanation,
                            "detected_nafdac": parsed.get("detected_nafdac"),
                            "tamper_seal_intact": parsed.get("tamper_seal_intact", True),
                            "processing_time_ms": latency_ms
                        }
                    else:
                        logger.warning(f"[VISION_ROUTER] [GEMINI_VISION] No candidates returned by Gemini: {resp_json}")
                else:
                    logger.warning(
                        f"[VISION_ROUTER] [GEMINI_VISION] API call returned HTTP {res.status_code}: {res.text}. "
                        "Falling back to Local Edge CV Engine."
                    )
        except Exception as e:
            logger.error(
                f"[VISION_ROUTER] [GEMINI_VISION] Connection/Parsing error: {str(e)}. "
                "Falling back to Local Edge CV Engine."
            )

        return None
