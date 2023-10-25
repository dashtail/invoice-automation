from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.tasks.scheduler import start_scheduler, stop_scheduler
from app.core.config import settings
from app.api.api import api_router

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

app.include_router(api_router, prefix="/api")