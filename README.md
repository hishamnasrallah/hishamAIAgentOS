# HishamOS - AI Operating System

HishamOS is a comprehensive AI-powered operating system that orchestrates multiple specialized AI agents to automate the entire Software Development Lifecycle (SDLC).

## Features

- **15+ Specialized AI Agents**: Coding, Code Review, DevOps, QA, BA, PM, Scrum Master, and more
- **Multi-Provider AI Support**: OpenAI, Anthropic Claude, Google Gemini, Ollama
- **AI Project Management**: Jira-like system with AI-powered story generation
- **Workflow Orchestration**: Complex multi-step workflows with state management
- **Role-Based Access Control (RBAC)**: Admin, Manager, Developer, Viewer roles
- **Token Usage Tracking**: Monitor and limit AI API usage per user
- **RESTful API**: Full REST API with Swagger documentation

## Architecture

### Backend (Django)
- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL (via Supabase)
- **Caching**: Redis
- **Task Queue**: Celery with Redis broker
- **AI Providers**: OpenAI, Anthropic, Ollama

### Frontend (Coming Soon)
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: TBD

## Project Structure

```
hishamAiAgentOS/
├── apps/
│   ├── users/          # User management & authentication
│   ├── agents/         # AI agents and tasks
│   ├── workflows/      # Workflow orchestration
│   └── projects/       # Project management (Jira-like)
├── libs/
│   ├── ai_providers/   # AI provider integrations
│   └── tools/          # Agent tools and utilities
├── config/
│   └── settings/       # Modular Django settings
├── docs/               # Complete documentation
└── hishamAiAgentOS/    # Main Django project
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Supabase)
- Redis
- Node.js 18+ (for frontend)

### Backend Setup

1. **Clone the repository**
   ```bash
   cd /path/to/project
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**

   The project is configured to use Supabase PostgreSQL. Update your `.env`:
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_supabase_host
   DB_PORT=5432
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load initial data (optional)**
   ```bash
   python manage.py loaddata initial_prompts
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

### Redis Setup

Make sure Redis is running:
```bash
redis-server
```

### Celery Setup

In a separate terminal, start Celery worker:
```bash
celery -A hishamAiAgentOS worker -l info
```

For Celery Beat (scheduled tasks):
```bash
celery -A hishamAiAgentOS beat -l info
```

## API Documentation

Once the server is running, access the API documentation at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/

## Configuration

### AI Providers

Configure AI providers in your `.env`:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

You can also add providers through the Django admin or API.

### User Roles

- **Admin**: Full system access
- **Manager**: Project and team management
- **Developer**: Code and task execution
- **Viewer**: Read-only access

## Core Apps

### 1. Users App
- Custom user model with RBAC
- JWT authentication
- Token usage tracking
- User permissions management

### 2. Agents App
- 15+ specialized AI agents
- Agent task management
- AI provider configuration
- Prompt management
- Execution tracking

### 3. Workflows App
- Multi-step workflow orchestration
- Workflow templates
- State management
- Conditional execution
- Parallel task support

### 4. Projects App
- Projects, Epics, Stories, Tasks
- Sprint management
- AI-powered story generation
- Kanban board support
- Comments and collaboration

## Key Models

### Agent Types
- CODING: Software development
- CODE_REVIEW: Code review and quality
- DEVOPS: Infrastructure and deployment
- QA: Testing and quality assurance
- BA: Business analysis
- PM: Project management
- SCRUM_MASTER: Agile ceremonies
- RELEASE_MANAGER: Release management
- BUG_TRIAGE: Issue categorization
- And more...

### Workflow Types
- BUG_LIFECYCLE: Complete bug workflow
- FEATURE_DEVELOPMENT: Feature implementation
- CHANGE_REQUEST: Change management
- RELEASE: Release process
- CODE_REVIEW: Review workflow
- CUSTOM: Custom workflows

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/refresh/` - Refresh access token

### Users
- `GET /api/users/` - List users
- `GET /api/users/me/` - Get current user
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/change_password/` - Change password

### Agents
- `GET /api/agents/tasks/` - List agent tasks
- `POST /api/agents/tasks/` - Create agent task
- `POST /api/agents/tasks/{id}/execute/` - Execute task
- `GET /api/agents/providers/` - List AI providers
- `GET /api/agents/prompts/` - List prompts

### Workflows
- `GET /api/workflows/workflows/` - List workflows
- `POST /api/workflows/workflows/` - Create workflow
- `POST /api/workflows/workflows/{id}/start/` - Start workflow
- `GET /api/workflows/templates/` - List templates

### Projects
- `GET /api/projects/projects/` - List projects
- `POST /api/projects/projects/` - Create project
- `GET /api/projects/stories/` - List stories
- `POST /api/projects/stories/generate_from_idea/` - Generate stories from idea

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

## Deployment

Refer to `docs/project_planning/MASTER_DEVELOPMENT_PLAN.md` for complete deployment instructions.

## Documentation

Complete documentation is available in the `docs/` directory:
- `MASTER_DEVELOPMENT_PLAN.md` - Complete implementation plan
- `hishamos_complete_design_part*.md` - Detailed system design (5 parts)
- `hishamos_ai_project_management.md` - Project management features
- `hishamos_ba_agent_auto_stories.md` - BA agent capabilities
- And many more...

## Contributing

This project is part of HishamOS v12.0 Ultimate Edition.

## License

[Add your license here]

## Support

For issues and questions, please refer to the documentation or contact the development team.
