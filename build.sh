#!/bin/bash
set -e

echo "=== Building HishamOS ==="

# Install Node dependencies and build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Collect static files for Django
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings.production

echo "=== Build complete ==="
