# ✅ HishamOS Quick Start Guide

## 🎉 Everything is Ready!

All setup is complete. You just need to start the servers!

## 🚀 Start Both Applications

### Terminal 1: Start Backend (Django)

```bash
./start-backend.sh
```

**Or manually:**
```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py runserver 8000
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Terminal 2: Start Frontend (React/Vite)

```bash
cd frontend
npm run dev
```

**Expected output:**
```
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## 🔐 Login Credentials

**Admin Panel:** http://localhost:8000/admin/

```
Username: admin
Password: Amman123
```

## 🎯 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000/api/ | REST API |
| Admin Panel | http://localhost:8000/admin/ | Django admin |
| API Docs | http://localhost:8000/api/schema/swagger-ui/ | Swagger UI |
| API Docs | http://localhost:8000/api/schema/redoc/ | ReDoc |

## ✅ What's Been Done

1. ✅ Python virtual environment created (`venv/`)
2. ✅ All Python packages installed (Django, DRF, Celery, etc.)
3. ✅ Database migrations completed (SQLite: `demo.sqlite3`)
4. ✅ Superuser created (admin/Amman123)
5. ✅ Frontend configured with backend URL
6. ✅ Smart URL detection added to frontend
7. ✅ Startup script created (`start-backend.sh`)

## 🧪 Testing the Setup

### 1. Test Backend is Running

Open browser: `http://localhost:8000/admin/`

**Expected:** Django admin login page

### 2. Test Frontend is Running

Open browser: `http://localhost:5173/`

**Expected:** HishamOS landing page

### 3. Test Admin Panel Link

From frontend homepage, click "Admin Panel"

**Expected:** Opens `http://localhost:8000/admin/` (Django admin login)

### 4. Login to Admin

Use credentials:
- Username: `admin`
- Password: `Amman123`

**Expected:** Django admin dashboard with all models

## 🛠 Configuration

### Backend (.env)
```bash
DEBUG=True
SECRET_KEY=django-insecure-...
DATABASE_URL=sqlite:///demo.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (frontend/.env)
```bash
VITE_API_URL=http://localhost:8000
```

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Browser (http://localhost:5173)               │
│                 React/Vite Frontend                     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ API Calls to VITE_API_URL
                    │ Admin links to :8000
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         Django Backend (http://localhost:8000)          │
│                                                         │
│  /admin/             → Django Admin Interface          │
│  /api/               → REST API Endpoints              │
│  /api/schema/        → API Documentation               │
│                                                         │
│  Database: SQLite (demo.sqlite3)                       │
└─────────────────────────────────────────────────────────┘
```

## 📝 Development Workflow

### Morning Startup
```bash
# Terminal 1: Backend
./start-backend.sh

# Terminal 2: Frontend
cd frontend && npm run dev
```

### During Development

**Backend changes (Python files):**
- Django auto-reloads on file changes
- No restart needed

**Frontend changes (React files):**
- Vite has hot module replacement
- Changes appear instantly

### Evening Shutdown
```bash
# Press Ctrl+C in both terminals
```

## 🔧 Common Commands

### Backend

```bash
# Activate venv
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver 8000

# Django shell
python manage.py shell

# Run tests
python manage.py test
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🐛 Troubleshooting

### Issue: Port 8000 already in use

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001

# Update frontend/.env
VITE_API_URL=http://localhost:8001
```

### Issue: Admin link goes to :5173/admin/

**Cause:** VITE_API_URL not set or frontend not restarted

**Fix:**
```bash
# 1. Verify frontend/.env
cat frontend/.env
# Should show: VITE_API_URL=http://localhost:8000

# 2. Restart frontend
cd frontend
npm run dev
```

### Issue: "Module not found" errors

**Backend:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Issue: Database errors

```bash
# Reset database (WARNING: Deletes all data)
rm demo.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🚀 Next Steps

1. ✅ Start both servers
2. ✅ Access http://localhost:5173
3. ✅ Click "Admin Panel" - should open Django admin
4. ✅ Login with admin/Amman123
5. 🎉 Start developing!

## 📚 Additional Resources

- **Project Documentation:** See `docs/` directory
- **API Documentation:** http://localhost:8000/api/schema/swagger-ui/
- **Django Admin:** http://localhost:8000/admin/

## 🎊 Summary

Everything is configured and ready to go! Just run:

**Terminal 1:**
```bash
./start-backend.sh
```

**Terminal 2:**
```bash
cd frontend && npm run dev
```

Then open http://localhost:5173 and enjoy! 🎉
