#!/bin/sh
set -e
cd /app
alembic upgrade head
if [ "${RUN_SEED}" = "true" ] || [ "${RUN_SEED}" = "1" ]; then
  python -m app.seed
fi
exec "$@"
