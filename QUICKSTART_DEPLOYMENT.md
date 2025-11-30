# Quick Deployment Checklist

## ✅ Pre-Deployment Verification

- [x] Frontend build working (`npm run build`)
- [x] Backend configuration complete
- [x] Database migrations created
- [x] Environment variables documented
- [x] Security settings configured

## 🚀 Deploy in 3 Steps

### Option 1: Heroku (Recommended for Quick Deploy)

```bash
# 1. Create app and add services
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini

# 2. Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set SECRET_KEY=$(openssl rand -base64 32)
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set VITE_SUPABASE_URL=your-supabase-url
heroku config:set VITE_SUPABASE_ANON_KEY=your-key

# 3. Deploy
git push heroku main
heroku run python manage.py createsuperuser
```

### Option 2: Railway (Easiest)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select repository
4. Add PostgreSQL and Redis services
5. Set environment variables (Railway auto-sets DATABASE_URL)
6. Deploy automatically triggers

### Option 3: Render

1. Go to https://render.com
2. Create "Web Service" from GitHub
3. Build: `./setup.sh`
4. Start: `gunicorn hishamAiAgentOS.wsgi --bind 0.0.0.0:$PORT`
5. Add PostgreSQL and Redis services
6. Set environment variables
7. Deploy

## 📋 Required Environment Variables

**Minimal setup:**
```bash
SECRET_KEY=generate-random-string-here
DATABASE_URL=postgresql://...
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=your-domain.com
```

**With Supabase:**
```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

**With AI features:**
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## 🔍 Verify Deployment

```bash
# Check API is running
curl https://your-domain.com/api/

# Check admin panel
open https://your-domain.com/admin/

# Check API docs
open https://your-domain.com/api/schema/swagger-ui/
```

## 🐛 Common Issues

**Build fails on `tsc` command:**
- ✅ FIXED: TypeScript is now in dependencies

**Static files not loading:**
```bash
python manage.py collectstatic --noinput --clear
```

**Database connection fails:**
- Check DATABASE_URL includes `?sslmode=require`
- Verify Supabase allows connections

**CORS errors:**
- Set CORS_ALLOWED_ORIGINS to your frontend URL
- Temporarily set CORS_ALLOW_ALL_ORIGINS=True for testing

## 📚 Full Documentation

- `BACKEND_DEPLOYMENT.md` - Detailed backend guide
- `DEPLOYMENT.md` - General deployment guide
- `.env.example` - All environment variables

## 🎉 You're Ready!

The application is fully configured for deployment. Choose your platform and follow the steps above.

**Frontend:** React + Vite (builds to `frontend/dist/`)
**Backend:** Django REST API (runs on Gunicorn)
**Database:** Supabase PostgreSQL
**Storage:** WhiteNoise for static files

Good luck with your deployment! 🚀

## 🔗 Frontend-Backend Connection

### Important: API URL Configuration

The frontend needs to know where your backend is deployed. This is configured via the `VITE_API_URL` environment variable.

**For separate deployments (Frontend on Vercel/Netlify, Backend on Heroku/Railway):**

1. **Deploy Backend First** and note its URL (e.g., `https://your-app.herokuapp.com`)

2. **Configure Frontend Environment Variable**:
   ```bash
   # On Vercel/Netlify
   VITE_API_URL=https://your-backend-url.herokuapp.com
   ```

3. **Update CORS on Backend**:
   ```bash
   # Set this on your backend deployment
   CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

**For monolithic deployment (Both on same domain):**

If deploying both frontend and backend together (e.g., Heroku/Railway serving static files):
- The frontend will automatically use `window.location.origin`
- No additional configuration needed
- Django serves the React build via WhiteNoise

### Deployment Scenarios

#### Scenario 1: Monolithic (Recommended for MVP)
Deploy everything together on one platform:
- Platform: Heroku/Railway/Render
- Frontend: Built and served by Django/WhiteNoise
- Backend: Django on same domain
- Configuration: No VITE_API_URL needed (auto-detects)

#### Scenario 2: Separate Deployments
Deploy frontend and backend separately:
- Frontend: Vercel/Netlify/Cloudflare Pages
- Backend: Heroku/Railway/Render
- Configuration Required:
  - Frontend: Set `VITE_API_URL=https://backend-url`
  - Backend: Set `CORS_ALLOWED_ORIGINS=https://frontend-url`

### Quick Test After Deployment

```bash
# Check frontend loads
curl https://your-domain.com/

# Check API is accessible
curl https://your-domain.com/api/

# Check CORS (from frontend domain)
curl -H "Origin: https://your-frontend-domain.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS https://your-backend-domain.com/api/
```

