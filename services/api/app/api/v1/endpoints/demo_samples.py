"""
Demo Samples Endpoints for Instant Competition Evaluation
"""

from fastapi import APIRouter
from typing import List, Dict, Any
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.abspath(os.path.join(current_dir, "../../../../../packages"))
if packages_dir not in sys.path:
    sys.path.insert(0, packages_dir)

from vision_engine.reference_catalog import DEMO_SAMPLES

router = APIRouter()


@router.get("", response_model=List[Dict[str, Any]])
def list_demo_samples():
    """
    Returns curated authentic and counterfeit test cases for 1-click evaluation.
    """
    return DEMO_SAMPLES
