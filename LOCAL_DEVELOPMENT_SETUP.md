# Local Development Setup Guide

## The Problem You're Experiencing

When you click "Admin Panel" from the frontend, you're staying on the same page. This is because:

1. ✅ **Frontend is running** (Vite dev server on port 5173)
2. ❌ **Backend is NOT running** (Django server should be on port 8000)
3. ❌ **Frontend doesn't know where backend is** (missing VITE_API_URL)

## Quick Fix - Start Both Servers

You need **TWO separate terminals** running simultaneously:

### Terminal 1: Start Django Backend

```bash
# Navigate to project root
cd /path/to/project

# Activate virtual environment (if you have one)
# source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate     # On Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Run migrations (first time only)
python manage.py migrate

# Create superuser (first time only)
python manage.py createsuperuser
# Username: admin
# Password: Amman123 (or your choice)

# Start Django server
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Terminal 2: Start Frontend

```bash
# Navigate to frontend directory
cd /path/to/project/frontend

# Install dependencies (first time only)
npm install

# Start Vite dev server
npm run dev
```

**Expected output:**
```
VITE v7.2.4  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## Configure Frontend to Connect to Backend

### Step 1: Create `.env` file in frontend directory

```bash
cd frontend
cat > .env << 'EOL'
VITE_API_URL=http://localhost:8000
EOL
```

### Step 2: Restart Frontend Dev Server

After creating `.env`, restart the frontend:
```bash
# Press Ctrl+C to stop
# Then restart:
npm run dev
```

## Verify Setup

### 1. Check Backend is Running

Open browser to: `http://localhost:8000/admin/`

**Expected:** Django admin login page

### 2. Check Frontend is Running

Open browser to: `http://localhost:5173/`

**Expected:** React application homepage

### 3. Test Frontend Links

From the frontend homepage, click "Admin Panel"

**Expected:** Opens `http://localhost:8000/admin/` (Django admin)

## Troubleshooting

### Issue: "Connection Refused" or "Cannot connect"

**Cause:** Backend server not running

**Fix:**
```bash
# In Terminal 1
python manage.py runserver
```

### Issue: Admin link goes to `localhost:5173/admin/`

**Cause:** `VITE_API_URL` not set or frontend not restarted

**Fix:**
```bash
# 1. Create/check frontend/.env
cat frontend/.env
# Should show: VITE_API_URL=http://localhost:8000

# 2. Restart frontend
cd frontend
npm run dev
```

### Issue: "No module named 'django'"

**Cause:** Python dependencies not installed

**Fix:**
```bash
pip install -r requirements.txt
```

### Issue: "Database doesn't exist"

**Cause:** Migrations not run

**Fix:**
```bash
python manage.py migrate
```

### Issue: Port 8000 already in use

**Cause:** Another process using port 8000

**Fix:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001

# Then update frontend/.env
VITE_API_URL=http://localhost:8001
```

## Complete Setup Checklist

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:5173`
- [ ] `frontend/.env` exists with `VITE_API_URL=http://localhost:8000`
- [ ] Can access `http://localhost:8000/admin/` directly
- [ ] Can access `http://localhost:5173/` directly
- [ ] Clicking "Admin Panel" from frontend opens Django admin

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Your Browser                      │
│  http://localhost:5173  (Frontend - React/Vite)    │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Clicks "Admin Panel"
                 │ Link has: ${API_URL}/admin/
                 │ Where API_URL comes from VITE_API_URL
                 │
                 ↓
┌─────────────────────────────────────────────────────┐
│            http://localhost:8000                     │
│           (Backend - Django Server)                  │
│                                                      │
│  /admin/        → Django Admin Interface            │
│  /api/          → REST API                          │
│  /api/schema/   → API Documentation                 │
└─────────────────────────────────────────────────────┘
```

## Environment Variables Explained

### Frontend `.env` (frontend/.env)

```bash
# Where the backend Django server is running
VITE_API_URL=http://localhost:8000

# Optional: Supabase configuration
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### Backend `.env` (root .env)

```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=config.settings.local

# Database
DATABASE_URL=sqlite:///demo.sqlite3

# CORS - Allow frontend to access backend
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Starting Development - Quick Commands

### Option 1: Manual (Recommended for learning)

```bash
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Option 2: Using screen/tmux (Linux/Mac)

```bash
# Start both in background
screen -dmS django bash -c 'python manage.py runserver'
screen -dmS frontend bash -c 'cd frontend && npm run dev'

# View sessions
screen -ls

# Attach to a session
screen -r django
screen -r frontend
```

### Option 3: Create start script

```bash
# Create start.sh
cat > start.sh << 'EOL'
#!/bin/bash
trap 'kill $(jobs -p)' EXIT

python manage.py runserver &
cd frontend && npm run dev &

wait
EOL

chmod +x start.sh
./start.sh
```

## Production vs Development

### Development (What you're doing now)
- Frontend: Vite dev server (`npm run dev`) on port 5173
- Backend: Django dev server (`runserver`) on port 8000
- Two separate servers, frontend proxies to backend

### Production (After deployment)
- Frontend: Built static files served by Django/WhiteNoise
- Backend: Django on production server (Heroku, etc.)
- Single server, Django serves both frontend and API

## Next Steps

1. ✅ Start both servers (backend + frontend)
2. ✅ Create frontend/.env with VITE_API_URL
3. ✅ Test admin access from frontend
4. Create superuser if not done: `python manage.py createsuperuser`
5. Start developing features!

## Quick Test Commands

```bash
# Test backend is running
curl http://localhost:8000/api/
# Should return JSON

# Test admin is accessible
curl http://localhost:8000/admin/
# Should return HTML with "Django administration"

# Test frontend is running
curl http://localhost:5173/
# Should return HTML with React app

# Check environment variable is set
cd frontend && cat .env
# Should show: VITE_API_URL=http://localhost:8000
```

## Common Development Workflow

```bash
# 1. Morning - Start servers
python manage.py runserver          # Terminal 1
cd frontend && npm run dev           # Terminal 2

# 2. Develop features
# Edit Python files for backend
# Edit React files in frontend/src for frontend

# 3. Test changes
# Backend changes auto-reload
# Frontend changes auto-reload with hot module replacement

# 4. Evening - Stop servers
# Ctrl+C in both terminals
```

## Summary

**The issue:** Frontend is running but backend is not. Frontend needs to know where backend is.

**The fix:** 
1. Start Django backend: `python manage.py runserver`
2. Create frontend/.env: `VITE_API_URL=http://localhost:8000`
3. Restart frontend: `npm run dev`

**Now it works:**
- Frontend on `localhost:5173`
- Backend on `localhost:8000`
- Admin accessible at `localhost:8000/admin/`
