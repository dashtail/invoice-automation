import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from app.tasks.scheduler import start_scheduler, stop_scheduler
from app.core.config import settings
from app.api.api import api_router
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    if settings.PROJECT_ENV == "sandbox":
        start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    if settings.PROJECT_ENV == "sandbox":
        stop_scheduler()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc.errors())
    return JSONResponse(content={"detail": exc.errors()}, status_code=422)


app.include_router(api_router, prefix="/api")
