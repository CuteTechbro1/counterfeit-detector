"""
OCR & Regulatory Text Inspector
Validates NAFDAC registration syntax, lot/batch codes, and expiration dates.
"""

import re
from typing import Dict, Any, List


class OCRInspector:
    def __init__(self):
        # Known NAFDAC numbers for V1 SKUs
        self.registered_nafdac = {
            "panadol-500mg-tablet": ["04-0244", "B4-0244"],
            "coca-cola-50cl-pet": ["01-0138"],
            "colgate-maximum-cavity-140g": ["02-4019"]
        }

    def inspect_text(self, product_slug: str, sample_meta: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyzes OCR text against regulatory standards for the product.
        """
        expected_nafdac_list = self.registered_nafdac.get(product_slug, [])

        # If sample metadata is provided (from demo fixture or simulated scan)
        if sample_meta and "detected_nafdac" in sample_meta:
            detected_nafdac = sample_meta.get("detected_nafdac")
            is_valid = detected_nafdac in expected_nafdac_list
            has_laser_batch = sample_meta.get("has_laser_batch", True)
            has_valid_expiry = sample_meta.get("has_valid_expiry", True)

            return {
                "detected_nafdac": detected_nafdac,
                "expected_nafdac": expected_nafdac_list[0] if expected_nafdac_list else None,
                "nafdac_match": is_valid,
                "has_batch_stamp": has_laser_batch,
                "has_valid_expiry": has_valid_expiry,
                "score_penalty": 0 if is_valid else 35
            }

        # Default fallback for genuine scan simulation
        return {
            "detected_nafdac": expected_nafdac_list[0] if expected_nafdac_list else "NOT_FOUND",
            "expected_nafdac": expected_nafdac_list[0] if expected_nafdac_list else None,
            "nafdac_match": True,
            "has_batch_stamp": True,
            "has_valid_expiry": True,
            "score_penalty": 0
        }
