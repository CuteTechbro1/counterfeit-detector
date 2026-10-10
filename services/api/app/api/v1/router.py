"""
API v1 Router Aggregator
"""

from fastapi import APIRouter
from .endpoints import scans, products, demo_samples, settings

api_router = APIRouter()

api_router.include_router(scans.router, prefix="/scans", tags=["Scans"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(demo_samples.router, prefix="/demo-samples", tags=["Demo Samples"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
