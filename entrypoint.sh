#!/bin/sh
set -e

echo "Starting entrypoint"

# Try migrations (retry until DB available)
count=0
until python manage.py migrate --noinput; do
  count=$((count+1))
  if [ "$count" -gt 30 ]; then
    echo "Migrations failed after 30 attempts"
    break
  fi
  echo "Waiting for database to be ready..."
  sleep 1
done

exec python manage.py runserver 0.0.0.0:8000
