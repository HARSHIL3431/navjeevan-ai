import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routes.chat import router as chat_router
from backend.services.data_service import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Navjeevan AI Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Starting Navjeevan AI backend")
    load_data()


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "navjeevan-ai-backend"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid request payload",
        },
    )


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
