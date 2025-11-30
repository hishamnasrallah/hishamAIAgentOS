# Frontend-Backend Connection Configuration

## Quick Reference

### Environment Variable

```bash
VITE_API_URL=https://your-backend-domain.com
```

## Deployment Scenarios

### 🎯 Monolithic (Recommended for MVP)

**One deployment, one domain:**

```bash
# Example: Heroku
heroku create hishamos-app
git push heroku main
```

Access:
- Frontend: `https://hishamos-app.herokuapp.com/`
- Backend: `https://hishamos-app.herokuapp.com/api/`
- Admin: `https://hishamos-app.herokuapp.com/admin/`

**Configuration:**
- ✅ No VITE_API_URL needed (auto-detects)
- ✅ No CORS configuration needed
- ✅ Simpler deployment
- ✅ Lower cost (one dyno/service)

---

### 🔀 Separate Deployments

**Frontend and backend on different platforms:**

#### Step 1: Deploy Backend

```bash
# Heroku example
heroku create hishamos-backend
git push heroku main
# URL: https://hishamos-backend.herokuapp.com
```

#### Step 2: Deploy Frontend

**Vercel:**
```bash
vercel --prod
# Set environment variable in dashboard:
# VITE_API_URL = https://hishamos-backend.herokuapp.com
```

**Netlify:**
```bash
netlify deploy --prod
# Set environment variable in dashboard:
# VITE_API_URL = https://hishamos-backend.herokuapp.com
```

#### Step 3: Configure CORS on Backend

```bash
# Set on backend deployment
heroku config:set CORS_ALLOWED_ORIGINS=https://hishamos-frontend.vercel.app
```

---

## Environment Variables Checklist

### Frontend Variables

```bash
# Required for separate deployments
VITE_API_URL=https://backend-domain.com

# Optional (Supabase)
VITE_SUPABASE_URL=https://project.supabase.co
VITE_SUPABASE_ANON_KEY=your-key
```

### Backend Variables

```bash
# Required
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=backend-domain.com

# For separate frontend
CORS_ALLOWED_ORIGINS=https://frontend-domain.com

# Optional
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
REDIS_URL=redis://...
```

---

## Testing After Deployment

### Monolithic Deployment

```bash
# Test frontend
curl https://your-app.com/

# Test API
curl https://your-app.com/api/

# Open in browser
open https://your-app.com/
```

### Separate Deployments

```bash
# Test backend
curl https://backend-domain.com/api/

# Test frontend
curl https://frontend-domain.com/

# Test CORS
curl -H "Origin: https://frontend-domain.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS https://backend-domain.com/api/
```

---

## Common Issues

### Issue: Links go to localhost

**Cause:** `VITE_API_URL` not set

**Fix:**
```bash
# On frontend deployment platform
VITE_API_URL=https://your-backend-url.com
```

### Issue: CORS errors in browser

**Cause:** Backend doesn't allow frontend domain

**Fix:**
```bash
# On backend deployment
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
```

### Issue: 404 on API routes

**Cause:** Backend not deployed or wrong URL

**Fix:**
1. Verify backend is running: `curl https://backend-url.com/api/`
2. Check `VITE_API_URL` is correct
3. Rebuild frontend after changing env vars

---

## Platform-Specific Instructions

### Heroku

```bash
# Set frontend URL
heroku config:set VITE_API_URL=https://backend.herokuapp.com -a frontend-app

# Set backend CORS
heroku config:set CORS_ALLOWED_ORIGINS=https://frontend.herokuapp.com -a backend-app
```

### Railway

```bash
# Set in Railway dashboard:
# Variables → Add Variable
VITE_API_URL=https://backend.railway.app
```

### Vercel

```bash
# vercel.json
{
  "env": {
    "VITE_API_URL": "https://backend.herokuapp.com"
  }
}

# Or in Vercel dashboard:
# Settings → Environment Variables
```

### Netlify

```bash
# netlify.toml
[build.environment]
  VITE_API_URL = "https://backend.herokuapp.com"

# Or in Netlify dashboard:
# Site settings → Environment variables
```

---

## Best Practices

1. ✅ **Start Monolithic** - Deploy everything together initially
2. ✅ **Test Locally First** - Use `VITE_API_URL=http://localhost:8000`
3. ✅ **Deploy Backend First** - Get the URL before deploying frontend
4. ✅ **Set CORS Properly** - Only allow specific domains, not `*`
5. ✅ **Use HTTPS** - Always use secure connections in production
6. ✅ **Document URLs** - Keep track of all deployment URLs

---

## Quick Commands

```bash
# Check current API URL (in frontend)
echo $VITE_API_URL

# Test API connection
curl $VITE_API_URL/api/

# Rebuild frontend after env change
npm run build

# Check build output
cat dist/assets/index-*.js | grep -o "http[s]*://[^\"]*" | sort -u
```

---

For more details, see:
- `QUICKSTART_DEPLOYMENT.md` - Full deployment guide
- `frontend/README.md` - Frontend-specific documentation
- `BACKEND_DEPLOYMENT.md` - Backend deployment guide
