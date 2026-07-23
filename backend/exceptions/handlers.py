from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.exceptions.base import BaseAppException


async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Returns field-level 422 errors in a consistent, readable format."""
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err["loc"] if loc != "body")
        errors.append({
            "field": field or "request",
            "message": err["msg"],
            "invalid_value": err.get("input"),
        })
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation failed. Check the 'errors' field for details.",
            "errors": errors,
        },
    )
