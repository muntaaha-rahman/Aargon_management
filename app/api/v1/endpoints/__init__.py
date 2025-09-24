from fastapi import APIRouter
from .auth import router as auth_router  # Fix this line

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])