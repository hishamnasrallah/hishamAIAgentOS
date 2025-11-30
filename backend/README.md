# HishamOS Backend API - Node.js/Express

## ✅ Backend is NOW RUNNING!

The Node.js backend is running on **http://localhost:8000**

## 🚀 Quick Access

| Service | URL |
|---------|-----|
| **API Root** | http://localhost:8000/api |
| **Documentation** | http://localhost:8000/api/docs |
| **Auth** | http://localhost:8000/api/auth |
| **Agents** | http://localhost:8000/api/agents |
| **Projects** | http://localhost:8000/api/projects |
| **Workflows** | http://localhost:8000/api/workflows |
| **Admin** | http://localhost:8000/api/admin |

## 📋 Features

- ✅ **Express.js** - Fast, minimalist web framework
- ✅ **Supabase** - PostgreSQL database with real-time capabilities
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **CORS Enabled** - Works with frontend on port 5173
- ✅ **RESTful API** - Standard REST endpoints
- ✅ **Auto-generated docs** - Visit /api/docs

## 🔐 Authentication

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123",
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Use Token

```bash
curl http://localhost:8000/api/agents \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📖 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (requires auth)

### Agents
- `GET /api/agents` - List all agents
- `GET /api/agents/:id` - Get agent by ID
- `POST /api/agents` - Create agent (requires auth)
- `PUT /api/agents/:id` - Update agent (requires auth)
- `DELETE /api/agents/:id` - Delete agent (requires auth)

### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects/:id` - Get project by ID
- `POST /api/projects` - Create project (requires auth)
- `PUT /api/projects/:id` - Update project (requires auth)
- `DELETE /api/projects/:id` - Delete project (requires auth)

### Workflows
- `GET /api/workflows` - List all workflows
- `GET /api/workflows/:id` - Get workflow by ID
- `POST /api/workflows` - Create workflow (requires auth)
- `PUT /api/workflows/:id` - Update workflow (requires auth)
- `DELETE /api/workflows/:id` - Delete workflow (requires auth)

### Admin (Requires admin privileges)
- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/users` - List all users
- `GET /api/admin/users/:id` - Get user by ID
- `PUT /api/admin/users/:id` - Update user permissions
- `DELETE /api/admin/users/:id` - Delete user

## 🗄️ Database

Uses **Supabase PostgreSQL** with the following tables:
- `users` - User accounts
- `agents_agenttask` - AI agent tasks
- `agents_agentexecution` - Agent execution history
- `projects_project` - Projects
- `projects_projectmembership` - Project team members
- `workflows_workflow` - Workflow definitions
- `workflows_workflowexecution` - Workflow runs

## 🛠️ Development

### Install Dependencies
```bash
npm install
```

### Start Server
```bash
npm start
```

### Start with Auto-Reload (Development)
```bash
npm run dev
```

### Environment Variables

Create `.env` file:
```env
PORT=8000
NODE_ENV=development
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
JWT_SECRET=your_jwt_secret
CORS_ORIGIN=http://localhost:5173
```

## 🔧 Configuration

The backend is configured to:
- Run on port **8000**
- Connect to **Supabase** database
- Allow CORS from **http://localhost:5173** (frontend)
- Use **JWT** for authentication
- Log all requests in development

## 📊 Testing

### Test API Root
```bash
curl http://localhost:8000/api
```

### Test Documentation
```bash
curl http://localhost:8000/api/docs
```

### Test Agents Endpoint
```bash
curl http://localhost:8000/api/agents
```

## 🚀 Deployment

The backend can be deployed to:
- **Heroku** - `git push heroku main`
- **Railway** - Connect GitHub repo
- **Render** - Deploy from GitHub
- **Vercel** - Serverless functions
- **AWS Lambda** - Serverless deployment

## 📁 Project Structure

```
backend/
├── src/
│   ├── config/
│   │   └── supabase.js      # Supabase client
│   ├── middleware/
│   │   └── auth.js          # JWT authentication
│   ├── routes/
│   │   ├── auth.js          # Auth endpoints
│   │   ├── agents.js        # Agents endpoints
│   │   ├── projects.js      # Projects endpoints
│   │   ├── workflows.js     # Workflows endpoints
│   │   └── admin.js         # Admin endpoints
│   └── server.js            # Main server file
├── .env                     # Environment variables
├── package.json             # Dependencies
└── README.md               # This file
```

## 🎯 Next Steps

1. ✅ Backend is running on port 8000
2. ✅ Frontend can connect to backend
3. 🔄 Create a user account via `/api/auth/register`
4. 🔄 Login to get JWT token
5. 🔄 Use token to create agents, projects, workflows
6. 🔄 Build frontend UI to interact with API

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
PORT=8001 npm start
```

### Supabase Connection Error
- Check `.env` has correct `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- Verify Supabase project is active
- Check database tables exist

### CORS Error
- Update `CORS_ORIGIN` in `.env`
- Restart backend after changing `.env`

## 📚 Resources

- **Express.js**: https://expressjs.com
- **Supabase**: https://supabase.com/docs
- **JWT**: https://jwt.io
- **Node.js**: https://nodejs.org

---

**Status:** ✅ RUNNING
**Port:** 8000
**Database:** Supabase PostgreSQL
**Authentication:** JWT
