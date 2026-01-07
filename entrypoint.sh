#!/bin/sh
set -e

echo "Waiting for Postgres..."
# loop until DB is ready
until python - <<'PY'
import sys
import os
import psycopg2
try:
    conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB','mzdb'), user=os.environ.get('POSTGRES_USER','mzuser'), password=os.environ.get('POSTGRES_PASSWORD','mzpass'), host=os.environ.get('POSTGRES_HOST','db'))
    conn.close()
except Exception:
    sys.exit(1)
sys.exit(0)
PY
do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - running migrations"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
