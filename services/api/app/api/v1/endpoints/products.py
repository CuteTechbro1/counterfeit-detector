"""
Product Catalog Endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.abspath(os.path.join(current_dir, "../../../../../packages"))
if packages_dir not in sys.path:
    sys.path.insert(0, packages_dir)

from vision_engine.reference_catalog import PRODUCTS_CATALOG

router = APIRouter()


@router.get("", response_model=List[Dict[str, Any]])
def list_supported_products():
    """
    Returns list of all products supported by the Counterfeit Detector V1 pilot.
    """
    return list(PRODUCTS_CATALOG.values())


@router.get("/{slug}", response_model=Dict[str, Any])
def get_product_details(slug: str):
    """
    Returns detailed specifications, checkpoints, and recommendations for a single product.
    """
    if slug not in PRODUCTS_CATALOG:
        raise HTTPException(status_code=404, detail=f"Product with slug '{slug}' not found.")
    return PRODUCTS_CATALOG[slug]
