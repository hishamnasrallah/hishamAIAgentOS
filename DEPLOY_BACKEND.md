# 🚀 Deploy Backend to Railway (5 Minutes)

## Why Railway?

Railway supports Python/Django out of the box and is the fastest way to get your backend live.

## 📋 Prerequisites

1. GitHub account
2. Railway account (sign up at https://railway.app with GitHub)

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit - HishamOS Backend"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hishamos-backend.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `hishamos-backend` repository
5. Railway will auto-detect Django and deploy!

### Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=(Railway will auto-generate PostgreSQL)
```

### Step 4: Access Your Backend

Railway will give you a URL like:
`https://hishamos-backend-production.up.railway.app`

Access:
- Admin: `https://your-app.railway.app/admin/`
- API: `https://your-app.railway.app/api/`
- Docs: `https://your-app.railway.app/api/schema/swagger-ui/`

## ⚡ Alternative: Render.com

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn hishamAiAgentOS.wsgi:application`
6. Add environment variables
7. Deploy!

## 🎯 After Deployment

Create superuser:
```bash
# In Railway dashboard, go to your service
# Click "Variables" → "Service" → "Terminal"
python manage.py createsuperuser
```

## 📝 Already Configured

✅ `Procfile` - For Heroku/Railway
✅ `railway.json` - Railway configuration
✅ `runtime.txt` - Python version
✅ `requirements.txt` - All dependencies
✅ Production settings - `config/settings/production.py`
✅ Gunicorn - Production server
✅ WhiteNoise - Static files

Everything is ready for deployment!

## 🔗 Update Frontend

Once backend is deployed, update `frontend/.env`:

```bash
VITE_API_URL=https://your-app.railway.app
```

Then rebuild frontend:
```bash
cd frontend
npm run build
```

Deploy frontend to Vercel/Netlify!
