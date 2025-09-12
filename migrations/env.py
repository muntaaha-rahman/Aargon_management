from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base   # ✅ use your project's Base
from app.auth import models          # import all your models
from app.core.settings import settings

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = Base.metadata

# DB URL
def get_url():
    return (
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url()
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
