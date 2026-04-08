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
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
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

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Idempotent katalog seed (DJANGO_RUN_SEED=true|1). Üretimde ürün güncellemesi yapmaması için varsayılan kapalı.
if [ "${DJANGO_RUN_SEED}" = "true" ] || [ "${DJANGO_RUN_SEED}" = "1" ]; then
  echo "Running seed_catalog..."
  SEED_EXTRA=""
  if [ "${DJANGO_SEED_DEMO_USER}" = "true" ] || [ "${DJANGO_SEED_DEMO_USER}" = "1" ]; then
    SEED_EXTRA="--with-demo-user"
  fi
  python manage.py seed_catalog ${SEED_EXTRA}
fi

exec "$@"
