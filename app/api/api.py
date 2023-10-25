from fastapi import APIRouter
from app.api.endpoints import invoice


api_router = APIRouter()
api_router.include_router(invoice.router, prefix="/invoice", tags=["invoice"])
