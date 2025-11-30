# Deployment Verification Checklist

## Pre-Deployment

- [ ] Frontend built successfully (`npm run build`)
- [ ] Static files configured in Django settings
- [ ] Templates directory includes `frontend/dist`
- [ ] URL routing configured correctly
- [ ] Environment variables documented

## After Deployment

### 1. Test Admin Access

```bash
# Visit admin panel
https://your-domain.com/admin/

# Should see Django admin login screen
# NOT a 404 or frontend error
```

**Expected:**
- Django admin login page
- Can login with superuser credentials
- Admin interface loads properly

### 2. Test API Endpoints

```bash
# API Root
curl https://your-domain.com/api/

# Should return JSON like:
# {"users": "...", "agents": "...", ...}
```

**Expected:**
- JSON response
- Lists available API endpoints
- HTTP 200 status

### 3. Test API Documentation

```bash
# Swagger UI
https://your-domain.com/api/schema/swagger-ui/

# ReDoc
https://your-domain.com/api/schema/redoc/

# OpenAPI Schema
https://your-domain.com/api/schema/
```

**Expected:**
- Interactive documentation loads
- Can test API endpoints
- Schema is valid

### 4. Test Frontend

```bash
# Homepage
https://your-domain.com/

# Should show React application
# Check browser console for errors
```

**Expected:**
- React app loads
- No console errors
- Links use correct backend URL (not localhost)

### 5. Test Frontend Links

From the frontend homepage, click:
- [ ] API Root link - Opens backend API (not localhost)
- [ ] Documentation link - Opens Swagger UI (not localhost)
- [ ] ReDoc link - Opens ReDoc (not localhost)
- [ ] Admin Panel link - Opens Django admin (not localhost)

**All links should point to your deployed domain!**

### 6. Test Static Files

```bash
# Check CSS loads
curl https://your-domain.com/static/admin/css/base.css

# Check frontend assets
curl https://your-domain.com/static/index-*.css
```

**Expected:**
- Files return with HTTP 200
- No 404 errors
- CSS/JS content loads

## Common Issues & Fixes

### Admin shows 404

**Cause:** URL routing issue or templates not configured

**Fix:**
```python
# Check hishamAiAgentOS/urls.py
# Admin path must be BEFORE catch-all route
urlpatterns = [
    path('admin/', admin.site.urls),  # This first
    # ... other routes ...
    re_path(r'^.*$', ...),  # This last
]
```

### Links go to localhost

**Cause:** `VITE_API_URL` not set

**Fix:**
```bash
# Set on deployment platform
VITE_API_URL=https://your-backend-domain.com
# Then rebuild frontend
npm run build
```

### Static files 404

**Cause:** Static files not collected

**Fix:**
```bash
python manage.py collectstatic --noinput --clear
```

### Admin has no CSS

**Cause:** WhiteNoise not configured or static files not collected

**Fix:**
```python
# Check settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be here
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### CORS errors

**Cause:** Frontend domain not in CORS_ALLOWED_ORIGINS

**Fix:**
```bash
# Set on backend
CORS_ALLOWED_ORIGINS=https://frontend-domain.com
```

## Database Check

```bash
# Check migrations applied
python manage.py showmigrations

# All should have [X] marks
```

## Security Check

```bash
# Run Django security check
python manage.py check --deploy

# Should show no errors (warnings are okay)
```

## Environment Variables Check

### Required Variables

Backend:
- [ ] `SECRET_KEY` - Set and different from default
- [ ] `DATABASE_URL` - Points to production database
- [ ] `ALLOWED_HOSTS` - Includes your domain
- [ ] `DJANGO_SETTINGS_MODULE=config.settings.production`

Frontend (if separate deployment):
- [ ] `VITE_API_URL` - Points to backend

Optional:
- [ ] `OPENAI_API_KEY` - For AI features
- [ ] `ANTHROPIC_API_KEY` - For AI features
- [ ] `REDIS_URL` - For Celery/cache

## Performance Check

```bash
# Check response times
time curl https://your-domain.com/api/

# Should be < 1 second for API
# Should be < 2 seconds for frontend
```

## Final Verification

- [ ] Admin accessible at `/admin/`
- [ ] API working at `/api/`
- [ ] Docs working at `/api/schema/swagger-ui/`
- [ ] Frontend loads at `/`
- [ ] All frontend links point to correct backend
- [ ] No console errors in browser
- [ ] Static files loading (CSS, JS, images)
- [ ] Database connected and migrations applied
- [ ] Can create/login as superuser
- [ ] Environment variables set correctly

## 🎉 Deployment Complete!

If all checks pass, your application is successfully deployed!

Access your application:
- **Frontend**: https://your-domain.com/
- **Admin**: https://your-domain.com/admin/
- **API**: https://your-domain.com/api/
- **Docs**: https://your-domain.com/api/schema/swagger-ui/

## Next Steps

1. Create superuser: `python manage.py createsuperuser`
2. Configure AI API keys (optional)
3. Set up monitoring (Sentry, etc.)
4. Configure custom domain (if needed)
5. Enable SSL/HTTPS
6. Set up backups
