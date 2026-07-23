from typing import Optional
from pydantic import BaseModel, Field

class AdvisoryRequest(BaseModel):
    crop: str = Field(..., description="Name of the crop")
    location: str = Field(..., description="Location of the farm")
    sowing_date: Optional[str] = Field(None, description="Date of sowing (YYYY-MM-DD)")

class MarketDecisionRequest(BaseModel):
    crop: str = Field(..., description="Name of the crop")
    location: str = Field(..., description="Current location")
    quantity_qtl: float = Field(..., gt=0, description="Quantity in quintals")
