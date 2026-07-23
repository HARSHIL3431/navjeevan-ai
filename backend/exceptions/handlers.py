from fastapi import Request
from fastapi.responses import JSONResponse
from backend.exceptions.base import BaseAppException

async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
        },
    )
