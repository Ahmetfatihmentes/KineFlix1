#!/usr/bin/env sh
set -e

# Kalıcı SQLite dizini (docker-compose volume ile eşlenir)
mkdir -p /app/data

if [ -z "${DATABASE_URL:-}" ]; then
  export DATABASE_URL="sqlite:////app/data/kineflix.db"
fi

echo "Applying database migrations (alembic upgrade head)..."
alembic upgrade head

echo "Starting application..."
exec "$@"
