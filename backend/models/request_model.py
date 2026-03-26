from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=2)

    @validator("query")
    def validate_query(cls, value: str) -> str:
        text = (value or "").strip()
        if len(text) < 2:
            raise ValueError("Query must contain at least 2 characters")
        return text


class ChatResponse(BaseModel):
    status: str
    intent: str | None = None
    data: str | None = None
    response: str | None = None
    message: str | None = None
