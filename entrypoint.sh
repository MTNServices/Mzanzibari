do
done
#!/bin/sh
set -e

echo "Waiting for Postgres via scripts/wait_for_db.py..."
python scripts/wait_for_db.py

echo "Postgres is up - running migrations"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
