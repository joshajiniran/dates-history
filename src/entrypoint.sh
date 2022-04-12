#!/bin/sh

echo "Waiting for postgres..."
# Ensure the DB start
while ! nc -z db 5432; do
    sleep 0.1
done

echo "Postgresql started"

# Run migrations
alembic upgrade head

# Start the server
uvicorn api.main:app --workers 1 --host 0.0.0.0 --port 8000