# Django Backend Successfully Running

## Server Status
- **Status:** Running
- **URL:** http://localhost:8000
- **Process ID:** 406
- **Database:** SQLite (demo.sqlite3)

## Admin Credentials
- **Username:** admin
- **Email:** admin@example.com
- **Password:** admin123

## Authentication
The API uses JWT authentication. To get a token:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

## Available API Endpoints

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login and get JWT tokens
- POST `/api/auth/logout/` - Logout
- POST `/api/auth/token/refresh/` - Refresh access token

### Agents
- GET/POST `/api/agents/tasks/` - Agent tasks
- GET/POST `/api/agents/prompts/` - AI prompts
- GET/POST `/api/agents/providers/` - AI providers
- GET `/api/agents/executions/` - Agent executions

### Projects
- GET `/api/projects/` - Projects root
- GET/POST `/api/projects/projects/` - Project management
- GET/POST `/api/projects/sprints/` - Sprint management
- GET/POST `/api/projects/epics/` - Epic management
- GET/POST `/api/projects/stories/` - User stories
- GET/POST `/api/projects/tasks/` - Project tasks

### Workflows
- GET/POST `/api/workflows/definitions/` - Workflow definitions
- GET/POST `/api/workflows/instances/` - Workflow instances
- POST `/api/workflows/instances/{id}/execute/` - Execute workflow

### Users
- GET/PUT `/api/users/profile/` - User profile
- GET `/api/users/permissions/` - User permissions

## Example API Call
```bash
# Get JWT token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' | \
  python3 -c "import json, sys; print(json.load(sys.stdin)['access'])")

# Use token to access API
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/agents/tasks/
```

## Server Control
- **View logs:** `tail -f backend.log`
- **Stop server:** `kill $(cat backend.pid)`
- **Restart server:** `kill $(cat backend.pid) && nohup venv/bin/python manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 & echo $! > backend.pid`

## Database
The backend is using SQLite for local development. To access the Django admin panel:
1. Visit: http://localhost:8000/admin/
2. Login with admin credentials above
