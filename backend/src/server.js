import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.js';
import agentsRoutes from './routes/agents.js';
import projectsRoutes from './routes/projects.js';
import workflowsRoutes from './routes/workflows.js';
import adminRoutes from './routes/admin.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.json({
    message: 'HishamOS Backend API',
    version: '1.0.0',
    endpoints: {
      auth: '/api/auth',
      agents: '/api/agents',
      projects: '/api/projects',
      workflows: '/api/workflows',
      admin: '/api/admin'
    },
    documentation: '/api/docs'
  });
});

app.get('/api', (req, res) => {
  res.json({
    message: 'HishamOS API - Node.js/Express + Supabase',
    version: '1.0.0',
    endpoints: {
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login',
        me: 'GET /api/auth/me'
      },
      agents: {
        list: 'GET /api/agents',
        get: 'GET /api/agents/:id',
        create: 'POST /api/agents',
        update: 'PUT /api/agents/:id',
        delete: 'DELETE /api/agents/:id'
      },
      projects: {
        list: 'GET /api/projects',
        get: 'GET /api/projects/:id',
        create: 'POST /api/projects',
        update: 'PUT /api/projects/:id',
        delete: 'DELETE /api/projects/:id'
      },
      workflows: {
        list: 'GET /api/workflows',
        get: 'GET /api/workflows/:id',
        create: 'POST /api/workflows',
        update: 'PUT /api/workflows/:id',
        delete: 'DELETE /api/workflows/:id'
      },
      admin: {
        stats: 'GET /api/admin/stats',
        users: 'GET /api/admin/users',
        getUser: 'GET /api/admin/users/:id',
        updateUser: 'PUT /api/admin/users/:id',
        deleteUser: 'DELETE /api/admin/users/:id'
      }
    },
    database: 'Supabase PostgreSQL',
    authentication: 'JWT'
  });
});

app.use('/api/auth', authRoutes);
app.use('/api/agents', agentsRoutes);
app.use('/api/projects', projectsRoutes);
app.use('/api/workflows', workflowsRoutes);
app.use('/api/admin', adminRoutes);

app.get('/api/docs', (req, res) => {
  res.json({
    title: 'HishamOS API Documentation',
    description: 'AI-Powered Operating System for Software Development',
    version: '1.0.0',
    baseUrl: `http://localhost:${PORT}/api`,
    authentication: {
      type: 'Bearer Token (JWT)',
      header: 'Authorization: Bearer <token>',
      howToGetToken: 'POST /api/auth/login or /api/auth/register'
    },
    endpoints: {
      authentication: [
        {
          method: 'POST',
          path: '/api/auth/register',
          description: 'Register a new user',
          body: {
            username: 'string (required)',
            email: 'string (required)',
            password: 'string (required)'
          },
          response: {
            token: 'JWT token',
            user: 'User object'
          }
        },
        {
          method: 'POST',
          path: '/api/auth/login',
          description: 'Login user',
          body: {
            email: 'string (required)',
            password: 'string (required)'
          },
          response: {
            token: 'JWT token',
            user: 'User object'
          }
        },
        {
          method: 'GET',
          path: '/api/auth/me',
          description: 'Get current user',
          headers: {
            Authorization: 'Bearer <token>'
          },
          response: {
            user: 'User object'
          }
        }
      ],
      agents: [
        {
          method: 'GET',
          path: '/api/agents',
          description: 'List all agents'
        },
        {
          method: 'GET',
          path: '/api/agents/:id',
          description: 'Get agent by ID'
        },
        {
          method: 'POST',
          path: '/api/agents',
          description: 'Create new agent (requires auth)',
          body: {
            title: 'string (required)',
            description: 'string',
            agent_type: 'string (required)',
            priority: 'low | medium | high'
          }
        },
        {
          method: 'PUT',
          path: '/api/agents/:id',
          description: 'Update agent (requires auth)'
        },
        {
          method: 'DELETE',
          path: '/api/agents/:id',
          description: 'Delete agent (requires auth)'
        }
      ],
      projects: [
        {
          method: 'GET',
          path: '/api/projects',
          description: 'List all projects'
        },
        {
          method: 'POST',
          path: '/api/projects',
          description: 'Create new project (requires auth)'
        }
      ],
      workflows: [
        {
          method: 'GET',
          path: '/api/workflows',
          description: 'List all workflows'
        },
        {
          method: 'POST',
          path: '/api/workflows',
          description: 'Create new workflow (requires auth)'
        }
      ],
      admin: [
        {
          method: 'GET',
          path: '/api/admin/stats',
          description: 'Get system statistics (requires admin)'
        },
        {
          method: 'GET',
          path: '/api/admin/users',
          description: 'List all users (requires admin)'
        },
        {
          method: 'PUT',
          path: '/api/admin/users/:id',
          description: 'Update user permissions (requires admin)'
        }
      ]
    }
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log('╔════════════════════════════════════════════════════════════════╗');
  console.log('║          🚀 HishamOS Backend Server Started!                  ║');
  console.log('╚════════════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`✅ Server running on: http://localhost:${PORT}`);
  console.log('');
  console.log('📋 API Endpoints:');
  console.log(`   • API Root:       http://localhost:${PORT}/api`);
  console.log(`   • Documentation:  http://localhost:${PORT}/api/docs`);
  console.log(`   • Auth:           http://localhost:${PORT}/api/auth`);
  console.log(`   • Agents:         http://localhost:${PORT}/api/agents`);
  console.log(`   • Projects:       http://localhost:${PORT}/api/projects`);
  console.log(`   • Workflows:      http://localhost:${PORT}/api/workflows`);
  console.log(`   • Admin:          http://localhost:${PORT}/api/admin`);
  console.log('');
  console.log('🗄️  Database: Supabase PostgreSQL');
  console.log('🔐 Auth: JWT Tokens');
  console.log('');
  console.log('Press Ctrl+C to stop the server');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
});

export default app;
