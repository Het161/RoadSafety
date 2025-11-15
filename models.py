from pydantic import BaseModel
from typing import List, Optional

class InterventionInput(BaseModel):
    type: str  # e.g., "Warning Sign"
    height_m: Optional[float] = None
    width_m: Optional[float] = None
    length_m: Optional[float] = None
    location_chainage_km: float

class EstimateRequest(BaseModel):
    road_id: str
    interventions: List[InterventionInput]

class MaterialLineItem(BaseModel):
    material_name: str
    quantity: float
    unit: str
    unit_rate: float
    total_cost: float
    source: str
    source_ref: str

class InterventionEstimate(BaseModel):
    intervention_type: str
    location_chainage_km: float
    irc_code: str
    clause_ref: str
    materials: List[MaterialLineItem]
    total_material_cost: float
    tolerance_percentage: float = 10.0

class EstimateResponse(BaseModel):
    road_id: str
    estimates: List[InterventionEstimate]
    grand_total: float
    currency: str = "INR"
