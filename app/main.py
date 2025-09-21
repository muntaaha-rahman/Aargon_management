# app/main.py
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth import routes as auth_routes

# Lifespan context for startup/shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup tasks...")
    # If you have a create_db_and_tables function, uncomment below
    # create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(
    lifespan=lifespan,
    title="School Management System for Autistic Students",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Custom OpenAPI with BearerAuth for JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include API routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the School Management API for Autistic Students!"}

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    return {"status": "healthy", "database": "connected"}