#!/bin/bash

echo "==================================="
echo "HishamOS Backend Setup Script"
echo "==================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠ .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your configuration."
else
    echo "✓ .env file exists"
fi

echo ""
echo "Running Django checks..."
python manage.py check
echo "✓ Django checks passed"

echo ""
echo "Creating database migrations..."
python manage.py makemigrations
echo "✓ Migrations created"

echo ""
echo "Applying migrations..."
python manage.py migrate
echo "✓ Migrations applied"

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration (database, Redis, AI API keys)"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Start Redis: redis-server"
echo "4. Run the development server: python manage.py runserver"
echo "5. Start Celery worker: celery -A hishamAiAgentOS worker -l info"
echo ""
echo "Access the API at: http://localhost:8000/api/"
echo "Access API docs at: http://localhost:8000/api/docs/"
echo ""
