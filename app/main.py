# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.endpoints import api_router

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

# Create FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title="School Management System",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc", 
    openapi_url="/api/openapi.json"
)

# Include API routers
app.include_router(api_router, prefix="/api/v1", tags=["API v1"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "School Management API is running!"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}