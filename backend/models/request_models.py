from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, validator


class AdvisoryRequest(BaseModel):
    crop: str = Field(..., min_length=2, max_length=100, description="Name of the crop")
    location: str = Field(..., min_length=2, max_length=100, description="Location of the farm")
    sowing_date: Optional[str] = Field(None, description="Date of sowing (YYYY-MM-DD)")

    @validator("crop", "location", pre=True)
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("must be a string")
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @validator("sowing_date", pre=True, always=True)
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            date.fromisoformat(str(v))
        except ValueError:
            raise ValueError("sowing_date must be in YYYY-MM-DD format")
        return v


class MarketDecisionRequest(BaseModel):
    crop: str = Field(..., min_length=2, max_length=100, description="Name of the crop")
    location: str = Field(..., min_length=2, max_length=100, description="Current location")
    quantity_qtl: float = Field(..., gt=0, le=100000, description="Quantity in quintals")

    @validator("crop", "location", pre=True)
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("must be a string")
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v
