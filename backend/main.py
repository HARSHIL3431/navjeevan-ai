import logging
import uuid
from typing import Any, Dict, List, Optional

import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.routes.chat import router as chat_router
from backend.routes.advisory import router as advisory_router
from backend.routes.weather import router as weather_router
from backend.services.data_service import load_data
from backend.decision_engine.providers import WeatherProvider, RuleProvider
from backend.exceptions.base import BaseAppException
from backend.exceptions.handlers import app_exception_handler, validation_exception_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    invalid_value: Optional[Any] = None


class ValidationErrorResponse(BaseModel):
    status: str = "error"
    message: str = "Validation failed. Check the 'errors' field for details."
    errors: List[ValidationErrorDetail]


app = FastAPI(
    title="Navjeevan AI Backend",
    version="2.0.0",
    responses={
        422: {
            "description": "Validation Error",
            "model": ValidationErrorResponse,
        }
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("frontend/dist/assets"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Starting Navjeevan AI backend")
    load_data()
    # Singleton providers — cache persists across all requests
    app.state.weather_provider = WeatherProvider()
    app.state.rule_provider = RuleProvider()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "navjeevan-ai-backend"}


@app.get("/", response_class=FileResponse)
@app.get("/app", response_class=FileResponse)
@app.get("/ui", response_class=FileResponse)
def serve_ui():
    if os.path.exists("frontend/public/navjeevan-ai.html"):
        return FileResponse("frontend/public/navjeevan-ai.html")
    return FileResponse("frontend/dist/index.html")


@app.get("/react", response_class=FileResponse)
def serve_react():
    return FileResponse("frontend/dist/index.html")





# Security headers on every response
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    return response


# Register custom exception handlers
app.add_exception_handler(BaseAppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Something went wrong",
        },
    )


app.include_router(chat_router, tags=["chat"])
app.include_router(advisory_router)
app.include_router(weather_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

