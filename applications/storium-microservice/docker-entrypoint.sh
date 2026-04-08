#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
python <<'PY'
import os
import sys
import time

import psycopg2

for i in range(60):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "storium_db"),
            user=os.environ.get("DB_USER", "storium_user"),
            password=os.environ.get("DB_PASSWORD", "storium_password"),
            host=os.environ.get("DB_HOST", "db"),
            port=os.environ.get("DB_PORT", "5432"),
        )
        conn.close()
        print("PostgreSQL is ready.")
        sys.exit(0)
    except Exception as exc:
        print(f"Attempt {i + 1}/60: {exc}")
        time.sleep(1)
print("Could not connect to PostgreSQL.")
sys.exit(1)
PY

export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT:-5432}/${DB_NAME}}"

alembic upgrade head

if [ "${RUN_SEED}" = "true" ] || [ "${RUN_SEED}" = "1" ]; then
  echo "Running seed..."
  export SEED_DEMO_USER="${SEED_DEMO_USER:-false}"
  python -m app.seed
fi

exec "$@"
