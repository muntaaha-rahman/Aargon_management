# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi

from app.core.database import get_db
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import clients
from app.api.v1.endpoints import services
from app.api.v1.endpoints import invoice_router as invoice


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
    title="Aargon Management",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],  # This includes OPTIONS
    allow_headers=["*"],
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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(clients.router, prefix="/api/v1", tags=["Clients"])
app.include_router(services.router, prefix="/api/v1", tags=["Services"])
app.include_router(invoice.router, prefix="/api/v1", tags=["Invoices"])


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Aargon"}
