from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .settings import settings

# -------------------------
# Database URL
# -------------------------
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

# -------------------------
# SQLAlchemy Engine & Session
# -------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # avoid "server closed connection" errors
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------
# Base class for models
# -------------------------
Base = declarative_base()
