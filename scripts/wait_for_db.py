#!/usr/bin/env python3
import time
import os
import sys
from psycopg2 import connect, OperationalError

HOST = os.environ.get('POSTGRES_HOST', 'db')
DB = os.environ.get('POSTGRES_DB', 'mzdb')
USER = os.environ.get('POSTGRES_USER', 'mzuser')
PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'mzpass')

RETRIES = int(os.environ.get('DB_WAIT_RETRIES', '30'))
BACKOFF = float(os.environ.get('DB_WAIT_BACKOFF', '1'))

for attempt in range(1, RETRIES + 1):
    try:
        conn = connect(dbname=DB, user=USER, password=PASSWORD, host=HOST)
        conn.close()
        print('Postgres is available')
        sys.exit(0)
    except OperationalError as e:
        print(f'Postgres unavailable (attempt {attempt}/{RETRIES}): {e}')
        time.sleep(BACKOFF)
        BACKOFF = min(10, BACKOFF * 2)

print('Postgres not available after retries')
sys.exit(1)
