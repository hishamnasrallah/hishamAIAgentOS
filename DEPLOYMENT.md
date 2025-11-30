# HishamOS Deployment Guide

## Project Structure

HishamOS is a full-stack application with:
- **Backend**: Django REST API (Python)
- **Frontend**: React + Vite (TypeScript)
- **Database**: PostgreSQL (via Supabase)
- **Cache/Queue**: Redis + Celery

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL database
- Redis server

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database
DB_NAME=hishamos_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-supabase-host
DB_PORT=5432

# Supabase
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-anon-key

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Provider Keys
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com

# Security
SECURE_SSL_REDIRECT=True
```

## Deployment Steps

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies and build frontend
npm install
npm run build
```

### 2. Run Migrations

```bash
python manage.py migrate --settings=config.settings.production
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

### 4. Create Superuser

```bash
python manage.py createsuperuser --settings=config.settings.production
```

### 5. Start the Application

**Using Gunicorn (Production):**
```bash
gunicorn hishamAiAgentOS.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

**Using the build script:**
```bash
./build.sh
```

### 6. Start Celery Workers (Optional)

```bash
# Start Celery worker
celery -A hishamAiAgentOS worker -l info

# Start Celery beat (for scheduled tasks)
celery -A hishamAiAgentOS beat -l info
```

## Platform-Specific Deployment

### Heroku

1. Create a new Heroku app
2. Add PostgreSQL and Redis addons
3. Set environment variables in Heroku dashboard
4. Deploy:

```bash
git push heroku main
```

The `Procfile` and `runtime.txt` are already configured.

### Railway

1. Create a new project
2. Connect your GitHub repository
3. Add PostgreSQL and Redis services
4. Set environment variables
5. Railway will auto-detect and deploy

### Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `./build.sh`
4. Set start command: `gunicorn hishamAiAgentOS.wsgi --log-file -`
5. Add PostgreSQL and Redis services
6. Set environment variables

### Docker

A `Dockerfile` can be created for containerized deployment:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Build frontend
RUN npm install && npm run build

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "hishamAiAgentOS.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Post-Deployment

1. **Verify the API**: Visit `https://your-domain.com/api/`
2. **Check Admin Panel**: Visit `https://your-domain.com/admin/`
3. **Test Frontend**: Visit `https://your-domain.com/`
4. **Monitor Logs**: Check application and error logs

## Troubleshooting

### Static Files Not Loading

```bash
# Ensure static files are collected
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT directory
ls -la staticfiles/
```

### Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Run migrations
python manage.py migrate
```

### Frontend Build Errors

```bash
# Clear node_modules and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY` with a strong random value
- [ ] Set up proper `ALLOWED_HOSTS`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT=True`)
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Configure CDN for static files (optional)
- [ ] Set up CI/CD pipeline
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Set up health check endpoints

## Support

For deployment issues, check the logs or contact support.
