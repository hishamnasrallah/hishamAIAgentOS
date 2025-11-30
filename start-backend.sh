#!/bin/bash

echo "🚀 Starting HishamOS Backend Server..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Set Django settings
export DJANGO_SETTINGS_MODULE=config.settings.local

# Start Django development server
echo "✅ Virtual environment activated"
echo "✅ Using local settings (SQLite database)"
echo ""
echo "Starting Django server on http://localhost:8000"
echo "Admin panel: http://localhost:8000/admin/"
echo ""
echo "Credentials:"
echo "  Username: admin"
echo "  Password: Amman123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python manage.py runserver 8000
