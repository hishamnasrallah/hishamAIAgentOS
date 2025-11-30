#!/bin/bash
set -e

echo "=== HishamOS Backend Setup ==="

# Check if running in production
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.production" ]; then
    echo "🚀 Running in PRODUCTION mode"
else
    echo "🔧 Running in DEVELOPMENT mode"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node dependencies and build frontend
echo "📦 Installing Node dependencies..."
npm install

echo "🏗️  Building frontend..."
npm run build

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create cache table
echo "💾 Creating cache table..."
python manage.py createcachetable || true

echo "✅ Setup complete!"
