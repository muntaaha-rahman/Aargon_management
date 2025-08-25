#!/bin/sh
set -e

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."

# Wait until Postgres is ready
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  echo "Postgres is unavailable - sleeping 2s"
  sleep 2
done

echo "Postgres is up - running migrations"
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
