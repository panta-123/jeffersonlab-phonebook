#!/bin/bash
set -e

# Optional: Run DB migrations here if needed
# echo "Running database migrations..."
# alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn jeffersonlab_phonebook.main:app --host 0.0.0.0 --port 8000
