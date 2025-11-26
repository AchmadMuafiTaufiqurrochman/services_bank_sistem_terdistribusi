#!/usr/bin/env sh
set -e

echo "[entrypoint] starting..."

# Helper: wait for DB port to be available. Try nc, otherwise fallback to Python socket check.
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

echo "[entrypoint] waiting for database at ${DB_HOST}:${DB_PORT}..."
tries=0
wait_ok=1
until (
  command -v nc >/dev/null 2>&1 && nc -z ${DB_HOST} ${DB_PORT}
) || (
  python - <<PY
import socket, sys
try:
    s = socket.create_connection(("${DB_HOST}", int(${DB_PORT})), timeout=1)
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
); do
  tries=$((tries+1))
  if [ $tries -gt 60 ]; then
    echo "[entrypoint] database did not become ready in time"
    wait_ok=0
    break
  fi
  sleep 1
done

if [ "$wait_ok" -ne 1 ]; then
  echo "[entrypoint] continuing even though DB wait timed out"
fi

# Run manual migration script if present
if [ -f /app/app/schemas/migration.py ]; then
  echo "[entrypoint] running manual migration script: app/schemas/migration.py"
  # use python to run the migration script
  python -u /app/app/schemas/migration.py || echo "[entrypoint] migration script failed (continuing)"
else
  echo "[entrypoint] manual migration script not found; skipping"
fi

echo "[entrypoint] starting uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
