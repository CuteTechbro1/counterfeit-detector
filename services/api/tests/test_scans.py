"""
Automated Test Suite for Counterfeit Detector API & Vision Engine
Verifies health, product endpoints, demo fixtures, and full analysis pipeline.
Tests Gemini Vision integration, response mapping, and local fallback logging.
"""

import pytest
import io
import json
import asyncio
from unittest.mock import patch, MagicMock
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from vision_engine.adapters.gemini_vision_adapter import GeminiVisionAdapter

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert any("Panadol" in p for p in data["supported_products"])
    assert "ai_engine" in data
    assert "gemini_vision_ready" in data["ai_engine"]
    assert "active_mode" in data["ai_engine"]


def test_list_products():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    slugs = [p["slug"] for p in data]
    assert "panadol-500mg-tablet" in slugs
    assert "coca-cola-50cl-pet" in slugs
    assert "colgate-maximum-cavity-140g" in slugs


def test_get_single_product():
    response = client.get("/api/v1/products/panadol-500mg-tablet")
    assert response.status_code == 200
    data = response.json()
    assert data["brand_name"] == "Panadol"
    assert data["standard_nafdac_no"] == "04-0244"
    assert len(data["things_to_look_out_for"]) >= 3


def test_list_demo_samples():
    response = client.get("/api/v1/demo-samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    sample_ids = [s["id"] for s in data]
    assert "sample-panadol-authentic" in sample_ids
    assert "sample-panadol-counterfeit" in sample_ids


def test_scan_panadol_authentic_and_mapped_fields():
    response = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-panadol-authentic"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # 1. Verify Core Mapped Fields required by specification
    assert "trust_score" in data
    assert "risk_level" in data
    assert "detected_issues" in data
    assert "authenticity_indicators" in data
    assert "explanation" in data
    assert "engine_used" in data

    assert data["product"]["slug"] == "panadol-500mg-tablet"
    assert data["trust_score"] >= 85
    assert data["risk_level"] == "LOW_RISK"
    assert len(data["detected_issues"]) == 0
    assert len(data["authenticity_indicators"]) >= 2
    assert "Panadol" in data["explanation"]
    assert data["nafdac_record"]["status"] == "VALID_ACTIVE"

    # Test audit certificate generation
    cert_res = client.get(f"/api/v1/scans/{data['scan_id']}/certificate")
    assert cert_res.status_code == 200
    assert "certificate_id" in cert_res.json()


def test_scan_panadol_counterfeit_mapped_fields():
    response = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-panadol-counterfeit"}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["trust_score"] < 60
    assert data["risk_level"] == "HIGH_RISK"
    assert len(data["detected_issues"]) >= 2
    assert any("NAFDAC" in d["title"] for d in data["detected_issues"])
    assert data["nafdac_record"]["status"] == "UNREGISTERED_COUNTERFEIT"
    assert "CRITICAL WARNING" in data["explanation"]


def test_scan_coca_cola_samples():
    # Authentic Coke
    res_auth = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-coke-authentic"}
    )
    assert res_auth.status_code == 200
    assert res_auth.json()["risk_level"] == "LOW_RISK"

    # Counterfeit Coke
    res_fake = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-coke-counterfeit"}
    )
    assert res_fake.status_code == 200
    assert res_fake.json()["risk_level"] == "HIGH_RISK"
    assert len(res_fake.json()["detected_issues"]) >= 2


def test_scan_colgate_samples():
    res_auth = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-colgate-authentic"}
    )
    assert res_auth.status_code == 200
    assert res_auth.json()["risk_level"] == "LOW_RISK"

    res_fake = client.post(
        "/api/v1/scans/analyze",
        data={"demo_sample_id": "sample-colgate-counterfeit"}
    )
    assert res_fake.status_code == 200
    assert res_fake.json()["risk_level"] == "HIGH_RISK"


def test_scan_uploaded_image_file():
    img = Image.new("RGB", (400, 400), color=(0, 24, 69))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/api/v1/scans/analyze",
        files={"image": ("test_panadol.png", buf, "image/png")},
        data={"product_hint": "panadol-500mg-tablet"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["slug"] == "panadol-500mg-tablet"
    assert data["engine_used"] == "LOCAL_FALLBACK"
    assert "LOCAL_FALLBACK" in data["engine_routing_log"]
    assert "trust_score" in data
    assert "risk_level" in data
    assert "detected_issues" in data
    assert "authenticity_indicators" in data
    assert "explanation" in data


def test_gemini_vision_adapter_mapping_and_routing():
    """
    Tests Gemini Vision adapter response mapping and router logging via asyncio.
    Mocks Google AI Studio HTTP response.
    """
    async def _run():
        mock_gemini_payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "identified_sku": "panadol-500mg-tablet",
                                    "trust_score": 93,
                                    "risk_level": "LOW_RISK",
                                    "detected_nafdac": "04-0244",
                                    "tamper_seal_intact": True,
                                    "explanation": "Forensic verification by Gemini Vision: packaging geometry, NAFDAC registration, and Haleon tamper seals match authentic standards.",
                                    "detected_issues": [],
                                    "authenticity_indicators": [
                                        "NAFDAC Reg. No. 04-0244 syntax matches registered Haleon standard",
                                        "Sharp offset typography with no color bleed",
                                        "Haleon holographic security seal intact and light-reflective"
                                    ]
                                })
                            }
                        ]
                    }
                }
            ]
        }

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_gemini_payload

        adapter = GeminiVisionAdapter(api_key="mock_test_key_12345")
        assert adapter.is_configured() is True

        with patch("httpx.AsyncClient.post", return_value=mock_resp):
            res = await adapter.inspect_packaging(
                image_bytes=b"\xff\xd8\xff\xe0mock_image_data",
                mime_type="image/jpeg",
                product_hint="panadol-500mg-tablet"
            )

            assert res is not None
            assert res["engine_used"] == "GEMINI_VISION"
            assert res["trust_score"] == 93
            assert res["risk_level"] == "LOW_RISK"
            assert len(res["detected_issues"]) == 0
            assert len(res["authenticity_indicators"]) == 3
            assert "Gemini Vision" in res["explanation"]
            assert "GEMINI_VISION" in res["engine_routing_log"]

    asyncio.run(_run())
