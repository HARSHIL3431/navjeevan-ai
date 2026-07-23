from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000, description="User query text")

    @validator("query", pre=True)
    @classmethod
    def strip_and_validate_query(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("query must be a string")
        v = v.strip()
        if len(v) < 2:
            raise ValueError("query must contain at least 2 non-whitespace characters")
        return v


class ChatResponse(BaseModel):
    status: str
    intent: str | None = None
    data: str | None = None
    response: str | None = None
    message: str | None = None
