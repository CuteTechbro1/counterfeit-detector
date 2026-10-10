"""
Pydantic Schemas for Scans and Verification Results
Explicitly maps trust_score, risk_level, detected_issues, authenticity_indicators, and explanation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DiscrepancyItem(BaseModel):
    checkpoint: Optional[str] = "packaging_integrity"
    severity: str
    title: str
    detail: str
    bounding_box: Optional[List[int]] = None


class CheckpointBreakdown(BaseModel):
    key: str
    title: str
    status: str
    similarity_pct: Optional[int] = None
    detected: Optional[str] = None
    expected: Optional[str] = None
    weight_pct: int


class ScoreFactorItem(BaseModel):
    category: str
    earned: int
    maximum: int
    status: str
    finding: str


class InspectionHotspot(BaseModel):
    id: str
    title: str
    detail: str
    user_box: List[int]
    ref_box: List[int]


class ThingToLookOutFor(BaseModel):
    title: str
    detail: str
    importance: str


class ProductSummary(BaseModel):
    id: str
    slug: str
    brand_name: str
    product_name: str
    manufacturer: str
    category: str
    standard_nafdac_no: str


class ScanAnalysisResponse(BaseModel):
    scan_id: str
    certificate_hash: Optional[str] = None
    
    # Core mapped fields requested
    trust_score: int = Field(ge=0, le=100)
    risk_level: str = Field(description="LOW_RISK, MEDIUM_RISK, or HIGH_RISK")
    detected_issues: List[DiscrepancyItem] = Field(default_factory=list)
    authenticity_indicators: List[str] = Field(default_factory=list)
    explanation: str

    # Engine Routing & Telemetry
    engine_used: str = Field(description="GEMINI_VISION or LOCAL_FALLBACK")
    engine_details: str
    engine_routing_log: str

    # Legacy / UI compatibility fields
    confidence_level: str
    verdict_label: str
    verdict_badge: str
    summary_explanation: str
    processing_time_ms: int
    product: ProductSummary
    quality_report: Dict[str, Any]
    nafdac_record: Optional[Dict[str, Any]] = None
    score_breakdown: Optional[List[ScoreFactorItem]] = None
    checkpoints_breakdown: List[CheckpointBreakdown]
    discrepancies: List[DiscrepancyItem]
    hotspots: Optional[List[InspectionHotspot]] = None
    reference_comparison: Dict[str, Any]
    things_to_look_out_for: List[ThingToLookOutFor]
