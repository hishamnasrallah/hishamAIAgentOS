# HishamOS Backend Deployment Guide

## Overview

The HishamOS backend is a Django REST API with:
- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL (via Supabase)
- **Task Queue**: Celery with Redis
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise

## Quick Start

### 1. Environment Variables

Required environment variables:

```bash
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=your-domain.com

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql://postgres:password@host:5432/postgres?sslmode=require

# Redis (for Celery)
REDIS_URL=redis://host:6379/0

# CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com

# AI APIs (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-key
```

### 2. Deployment Commands

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Build frontend
npm run build

# Setup database and static files
python manage.py migrate
python manage.py collectstatic --noinput

# Start the server
gunicorn hishamAiAgentOS.wsgi --bind 0.0.0.0:8000
```

## Platform-Specific Guides

### Heroku Deployment

1. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

2. **Add Addons**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   heroku addons:create heroku-redis:mini
   ```

3. **Set Environment Variables**:
   ```bash
   heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
   heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   heroku config:set OPENAI_API_KEY=your-key
   heroku config:set ANTHROPIC_API_KEY=your-key
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Create Superuser**:
   ```bash
   heroku run python manage.py createsuperuser
   ```

6. **Scale Workers** (Optional):
   ```bash
   heroku ps:scale worker=1 beat=1
   ```

### Railway Deployment

1. **Connect Repository**:
   - Go to Railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Add Services**:
   - Add PostgreSQL database
   - Add Redis service

3. **Set Environment Variables**:
   - Go to project settings
   - Add all required environment variables
   - Railway will auto-set `DATABASE_URL` and `REDIS_URL`

4. **Deploy**:
   - Railway auto-deploys on git push
   - Or manually trigger deployment

### Render Deployment

1. **Create Web Service**:
   - Go to Render.com
   - Click "New +" → "Web Service"
   - Connect your repository

2. **Configure Build**:
   - **Build Command**: `./setup.sh`
   - **Start Command**: `gunicorn hishamAiAgentOS.wsgi --bind 0.0.0.0:$PORT`

3. **Add PostgreSQL**:
   - Create PostgreSQL database
   - Copy `DATABASE_URL`

4. **Add Redis**:
   - Create Redis instance
   - Copy `REDIS_URL`

5. **Set Environment Variables**:
   - Add all required variables in Environment section

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

# Install Node.js
RUN apt-get update && apt-get install -y \
    nodejs npm \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install Node dependencies and build frontend
RUN npm install && npm run build

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "hishamAiAgentOS.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: hishamos_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: gunicorn hishamAiAgentOS.wsgi --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:your_password@db:5432/hishamos_db
      - REDIS_URL=redis://redis:6379/0
      - DJANGO_SETTINGS_MODULE=config.settings.production

  celery:
    build: .
    command: celery -A hishamAiAgentOS worker --loglevel=info
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:your_password@db:5432/hishamos_db
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
```

Deploy with:
```bash
docker-compose up -d
```

## Post-Deployment

### 1. Verify Deployment

Check these endpoints:
- `https://your-domain.com/api/` - API Root
- `https://your-domain.com/admin/` - Admin Panel
- `https://your-domain.com/api/schema/` - API Schema

### 2. Create Admin User

```bash
# Heroku
heroku run python manage.py createsuperuser

# Railway
railway run python manage.py createsuperuser

# Render
render run python manage.py createsuperuser

# Docker
docker-compose exec web python manage.py createsuperuser
```

### 3. Test API

```bash
# Health check
curl https://your-domain.com/api/

# Get JWT token
curl -X POST https://your-domain.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

### 4. Monitor Logs

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Render
# Check dashboard logs

# Docker
docker-compose logs -f web
```

## Celery Workers (Optional)

For background task processing:

### Heroku
```bash
# Already configured in Procfile
heroku ps:scale worker=1 beat=1
```

### Railway
Create separate services for worker and beat with these commands:
- Worker: `celery -A hishamAiAgentOS worker --loglevel=info`
- Beat: `celery -A hishamAiAgentOS beat --loglevel=info`

### Docker
Already configured in docker-compose.yml

## Database Migrations

The Supabase database migrations are managed separately. To apply them:

1. Migrations are in `supabase/migrations/`
2. They're automatically applied via Supabase
3. Django migrations are applied via the `release` command in Procfile

## Troubleshooting

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check WhiteNoise is in MIDDLEWARE
# It should be right after SecurityMiddleware
```

### Database Connection Issues

```bash
# Test connection
python manage.py dbshell

# Check DATABASE_URL format
echo $DATABASE_URL

# Ensure SSL mode for Supabase
# Should include ?sslmode=require
```

### CORS Issues

```bash
# Update CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS=https://frontend-domain.com,https://www.frontend-domain.com

# Or temporarily allow all (not recommended for production)
CORS_ALLOW_ALL_ORIGINS=True
```

### Celery Not Processing Tasks

```bash
# Check Redis connection
python -c "import redis; r = redis.from_url('$REDIS_URL'); print(r.ping())"

# Check Celery workers
celery -A hishamAiAgentOS inspect active
```

## Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT=True`)
- [ ] Set secure cookie flags
- [ ] Configure CORS properly (no wildcards)
- [ ] Use environment variables for secrets
- [ ] Enable database SSL
- [ ] Set up regular backups
- [ ] Configure rate limiting
- [ ] Monitor error logs
- [ ] Keep dependencies updated

## API Documentation

Once deployed, access API documentation at:
- Swagger UI: `https://your-domain.com/api/schema/swagger-ui/`
- ReDoc: `https://your-domain.com/api/schema/redoc/`
- OpenAPI Schema: `https://your-domain.com/api/schema/`

## Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Test database connectivity
4. Check static files are collected
5. Verify Redis connection (if using Celery)

## Maintenance

### Update Dependencies
```bash
pip install -U -r requirements.txt
npm update
```

### Database Backup
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# Docker
docker-compose exec db pg_dump -U postgres hishamos_db > backup.sql
```

### Monitor Performance
- Set up application monitoring (e.g., Sentry)
- Monitor database queries
- Track Celery task performance
- Monitor memory and CPU usage

## URL Routing Configuration

### How URLs are Handled

The application uses Django's URL routing with priority order:

```python
urlpatterns = [
    path('admin/', admin.site.urls),                    # Priority 1
    path('api/schema/', ...),                           # Priority 2
    path('api/schema/swagger-ui/', ...),                # Priority 2
    path('api/schema/redoc/', ...),                     # Priority 2
    path('api/', include('apps.users.urls')),           # Priority 3
    path('api/agents/', include('apps.agents.urls')),   # Priority 3
    path('api/workflows/', include('apps.workflows.urls')), # Priority 3
    path('api/projects/', include('apps.projects.urls')),  # Priority 3
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')), # Catch-all
]
```

### URL Structure

#### Backend URLs (Django)
- `/admin/` - Django administration interface
- `/api/` - REST API root
- `/api/schema/` - OpenAPI schema (JSON)
- `/api/schema/swagger-ui/` - Interactive API documentation
- `/api/schema/redoc/` - Alternative API documentation

#### Frontend URLs (React SPA)
- `/` - React application (all other routes)
- Frontend uses client-side routing via React Router

### Important Notes

1. **Order Matters**: Django processes URLs in the order they appear. Admin and API routes must come before the catch-all.

2. **Static Files**: Django serves static files via WhiteNoise at `/static/`

3. **Template Configuration**: The frontend's `index.html` is found via TEMPLATES configuration:
   ```python
   TEMPLATES = [
       {
           'DIRS': [
               BASE_DIR / 'templates',
               BASE_DIR / 'frontend' / 'dist',
           ],
       }
   ]
   ```

4. **Frontend Build**: Must run `npm run build` before deploying to generate the `frontend/dist/` directory

### Testing URL Routing

```bash
# Test admin access
curl https://your-domain.com/admin/
# Should redirect to admin login

# Test API
curl https://your-domain.com/api/
# Should return JSON API root

# Test frontend
curl https://your-domain.com/
# Should return React app HTML

# Test API docs
curl https://your-domain.com/api/schema/swagger-ui/
# Should return Swagger UI HTML
```

