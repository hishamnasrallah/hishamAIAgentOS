# HishamOS - Quick Start Guide

Get HishamOS up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- PostgreSQL (or use Supabase)
- Redis

## Installation (macOS/Linux)

```bash
# 1. Navigate to project directory
cd /path/to/hishamAiAgentOS

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Configure environment
# Edit .env with your credentials (database, Redis, AI keys)
nano .env

# 5. Create superuser
python manage.py createsuperuser

# 6. Start Redis (in new terminal)
redis-server

# 7. Start Django server
python manage.py runserver

# 8. Start Celery (in another terminal)
source venv/bin/activate
celery -A hishamAiAgentOS worker -l info
```

## Installation (Windows)

```powershell
# 1. Navigate to project directory
cd C:\path\to\hishamAiAgentOS

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure .env file
copy .env.example .env
# Edit .env with your settings

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start Redis (in new terminal)
redis-server

# 8. Start Django
python manage.py runserver

# 9. Start Celery (in another terminal)
venv\Scripts\activate
celery -A hishamAiAgentOS worker -l info
```

## Access Points

Once running:

- **API Base**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/

## First Steps

### 1. Login to Admin
Go to http://localhost:8000/admin/ and login with your superuser credentials.

### 2. Configure AI Provider

**Option A: Via API**
```bash
curl -X POST http://localhost:8000/api/agents/providers/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenAI GPT-4",
    "provider_type": "OPENAI",
    "api_key": "sk-...",
    "model_name": "gpt-4",
    "is_active": true,
    "max_tokens": 4096,
    "temperature": 0.7
  }'
```

**Option B: Via Admin Panel**
1. Go to Admin → AI Providers → Add AI Provider
2. Fill in the details
3. Save

### 3. Create Your First Project

```bash
# Get JWT token first
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'

# Create project
curl -X POST http://localhost:8000/api/projects/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "DEMO",
    "name": "Demo Project",
    "description": "My first HishamOS project"
  }'
```

### 4. Create an Agent Task

```bash
curl -X POST http://localhost:8000/api/agents/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "CODING",
    "title": "Create Hello World Function",
    "description": "Create a simple hello world function in Python",
    "priority": 5,
    "input_data": {
      "task_type": "NEW_BUILD",
      "language": "Python",
      "requirements": "Create a function that prints Hello World"
    }
  }'
```

### 5. Generate User Stories from Idea

```bash
curl -X POST http://localhost:8000/api/projects/stories/generate_from_idea/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "Build a task management app with drag and drop",
    "project_id": 1
  }'
```

## Environment Configuration

### Required Settings (.env)

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key

# Database (PostgreSQL)
DB_NAME=hishamos_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Providers (at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# CORS (for frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Optional Settings

```env
# Supabase (if using)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=your_key
```

## Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/api/docs/
2. Click "Authorize" and enter your JWT token
3. Try different endpoints interactively

### Using curl

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "role": "DEVELOPER"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Get current user (use access token from login)
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# List agent types
curl -X GET http://localhost:8000/api/agents/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "email": "test@example.com",
    "password": "SecurePass123!"
})
token = response.json()["access"]

# Headers for authenticated requests
headers = {"Authorization": f"Bearer {token}"}

# Create project
project = requests.post(f"{BASE_URL}/projects/projects/",
    headers=headers,
    json={
        "key": "TEST",
        "name": "Test Project",
        "description": "Testing the API"
    }
)
print(project.json())

# Create agent task
task = requests.post(f"{BASE_URL}/agents/tasks/",
    headers=headers,
    json={
        "agent_type": "CODING",
        "title": "Generate Python function",
        "description": "Create a sorting function",
        "priority": 3,
        "input_data": {
            "task_type": "NEW_BUILD",
            "language": "Python",
            "requirements": "Create a function to sort a list of numbers"
        }
    }
)
print(task.json())
```

## Common Issues

### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
python manage.py runserver 8001
```

### Redis not running
```bash
# Check if Redis is running
redis-cli ping

# Should return: PONG

# If not, start Redis
redis-server
```

### Database connection error
```bash
# Test PostgreSQL connection
psql -h localhost -U postgres -d hishamos_db

# Create database if it doesn't exist
createdb hishamos_db
```

### Import errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## What's Next?

1. **Explore the Admin**: http://localhost:8000/admin/
   - Manage users
   - Configure AI providers
   - View agent tasks
   - Monitor workflows

2. **Read the Documentation**:
   - `README.md` - Complete overview
   - `DEVELOPMENT.md` - Developer guide
   - `BUILD_SUMMARY.md` - What's been built
   - `docs/` - Detailed design docs

3. **Try the Agents**:
   - Create coding tasks
   - Request code reviews
   - Generate user stories
   - Build workflows

4. **Build the Frontend**:
   - React + TypeScript
   - Tailwind + shadcn/ui
   - Connect to this API

5. **Customize**:
   - Add new agent types
   - Create workflow templates
   - Extend the models
   - Add custom tools

## Support

- Check `DEVELOPMENT.md` for troubleshooting
- Review API docs at http://localhost:8000/api/docs/
- Examine the code - it's well-documented!

---

**Happy coding with HishamOS! 🚀**
