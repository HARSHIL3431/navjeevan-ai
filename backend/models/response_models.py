from typing import Any, Dict, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="success or error")
    message: str = Field(default="", description="Message to user")
    data: Optional[T] = Field(default=None, description="Response payload")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    version: str = Field(default="1.0", description="API version")

class AdvisoryResponsePayload(BaseModel):
    decision_data: Dict[str, Any] = Field(..., description="Raw DTO output from Decision Engine")
    ai_advice: str = Field(..., description="AI Formatted natural language advice")
