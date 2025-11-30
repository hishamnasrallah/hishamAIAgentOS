# HishamOS Development Guide

This guide provides detailed instructions for developers working on HishamOS.

## Quick Start

```bash
# 1. Run the setup script
chmod +x setup.sh
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

## Development Workflow

### 1. Setting Up Your Environment

#### Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql redis-server
```

**macOS:**
```bash
brew install python@3.11 postgresql redis
```

**Windows:**
- Install Python 3.11+ from python.org
- Install PostgreSQL from postgresql.org
- Install Redis from github.com/microsoftarchive/redis

#### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Database Setup

#### Using PostgreSQL Locally

```bash
# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database
createdb hishamos_db

# Update .env
DB_NAME=hishamos_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

#### Using Supabase

1. Go to supabase.com and create a project
2. Get your connection details from Project Settings > Database
3. Update .env with Supabase credentials

### 3. Running Services

#### Start Redis
```bash
redis-server
```

#### Start Django Development Server
```bash
python manage.py runserver
```

#### Start Celery Worker
```bash
celery -A hishamAiAgentOS worker -l info
```

#### Start Celery Beat (for scheduled tasks)
```bash
celery -A hishamAiAgentOS beat -l info
```

### 4. Working with Migrations

```bash
# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Revert migrations
python manage.py migrate app_name migration_name
```

### 5. Django Admin

Access Django admin at http://localhost:8000/admin/

Create a superuser:
```bash
python manage.py createsuperuser
```

## Project Structure Explained

```
hishamAiAgentOS/
├── apps/                           # Django apps
│   ├── users/                      # User management
│   │   ├── models.py              # HishamOSUser, UserPermission
│   │   ├── serializers.py         # API serializers
│   │   ├── views.py               # API views
│   │   ├── permissions.py         # RBAC permissions
│   │   └── urls.py                # API routes
│   │
│   ├── agents/                     # AI Agents
│   │   ├── models.py              # AgentTask, Prompt, AIProvider
│   │   ├── base_agent.py          # BaseAgent class
│   │   ├── specialized/           # Specialized agent classes
│   │   │   ├── coding_agent.py
│   │   │   ├── code_review_agent.py
│   │   │   └── ba_agent.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── workflows/                  # Workflow orchestration
│   │   ├── models.py              # Workflow, WorkflowStep, Template
│   │   ├── engine.py              # Workflow execution engine
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── projects/                   # Project management
│       ├── models.py              # Project, Epic, Story, Task
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── libs/                           # Reusable libraries
│   ├── ai_providers/              # AI provider integrations
│   │   ├── base.py               # AIProviderBase
│   │   ├── openai_provider.py
│   │   ├── anthropic_provider.py
│   │   └── ollama_provider.py
│   │
│   └── tools/                     # Agent tools
│       └── ...
│
├── config/                         # Configuration
│   └── settings/
│       ├── base.py               # Base settings
│       └── local.py              # Local development
│
├── hishamAiAgentOS/               # Main Django project
│   ├── settings.py               # Settings import
│   ├── urls.py                   # Main URL config
│   ├── celery.py                 # Celery config
│   └── wsgi.py
│
├── docs/                          # Documentation
├── logs/                          # Log files
├── manage.py                      # Django management
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── README.md                      # Main documentation
```

## Adding New Features

### Creating a New Agent

1. Create agent class in `apps/agents/specialized/`:

```python
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType

class MyNewAgent(BaseAgent):
    agent_type = AgentType.MY_AGENT
    agent_name = "My New Agent"
    agent_description = "Description"
    capabilities = ['CAPABILITY_1', 'CAPABILITY_2']

    def execute_task(self, task: AgentTask):
        # Implementation
        pass
```

2. Register in agent factory
3. Create prompt in database
4. Test the agent

### Creating a New Workflow

1. Define workflow type in `apps/workflows/models.py`
2. Create workflow template
3. Implement workflow steps
4. Test workflow execution

### Adding New API Endpoint

1. Add method to ViewSet in `views.py`
2. Use `@action` decorator for custom actions
3. Update serializers if needed
4. Document in API docs

Example:
```python
@action(detail=True, methods=['post'])
def my_custom_action(self, request, pk=None):
    obj = self.get_object()
    # Implementation
    return Response({'status': 'success'})
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific app tests
pytest apps/users/tests/

# Run with coverage
pytest --cov=apps --cov-report=html
```

### Writing Tests

Create test files in each app:

```python
# apps/users/tests/test_models.py
from django.test import TestCase
from apps.users.models import HishamOSUser

class UserModelTest(TestCase):
    def test_create_user(self):
        user = HishamOSUser.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@test.com')
```

## Code Quality

### Formatting

```bash
# Format code with Black
black .

# Check formatting
black --check .
```

### Linting

```bash
# Lint with flake8
flake8 .

# Fix common issues
autopep8 --in-place --recursive .
```

### Type Checking

```bash
# Type check with mypy
mypy apps/
```

## Debugging

### Django Debug Toolbar

Add to `INSTALLED_APPS` in local.py:
```python
INSTALLED_APPS += ['debug_toolbar']
```

### Logging

View logs in `logs/hishamos.log`

Add logging to your code:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
```

### Django Shell

```bash
python manage.py shell
```

```python
from apps.users.models import HishamOSUser
users = HishamOSUser.objects.all()
```

## API Development

### Testing API Endpoints

Using curl:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'

# Use token
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Using httpie:
```bash
# Login
http POST localhost:8000/api/auth/login/ email=user@example.com password=pass123

# Use token
http GET localhost:8000/api/users/me/ "Authorization: Bearer TOKEN"
```

### API Documentation

Access Swagger UI at: http://localhost:8000/api/docs/

The API is fully documented with:
- Request/response schemas
- Authentication requirements
- Example requests
- Error responses

## Common Tasks

### Create New App

```bash
python manage.py startapp app_name apps/app_name
```

### Create Management Command

Create `apps/app_name/management/commands/my_command.py`:

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description'

    def handle(self, *args, **options):
        # Implementation
        self.stdout.write(self.style.SUCCESS('Done!'))
```

Run: `python manage.py my_command`

### Database Backup

```bash
# Backup
python manage.py dumpdata --indent 2 > backup.json

# Restore
python manage.py loaddata backup.json
```

### Clear Cache

```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Environment Variables

Key environment variables:

- `DEBUG`: Enable debug mode (True/False)
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database config
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `ALLOWED_HOSTS`: Comma-separated allowed hosts
- `CORS_ALLOWED_ORIGINS`: Comma-separated CORS origins

## Troubleshooting

### Common Issues

**1. Module not found**
```bash
pip install -r requirements.txt
```

**2. Database connection error**
- Check PostgreSQL is running
- Verify .env database credentials
- Test connection: `psql -h localhost -U postgres hishamos_db`

**3. Redis connection error**
- Check Redis is running: `redis-cli ping`
- Verify REDIS_URL in .env

**4. Migration conflicts**
```bash
python manage.py migrate --fake app_name migration_name
python manage.py migrate
```

**5. Permission denied**
```bash
chmod +x setup.sh
```

## Performance

### Database Query Optimization

Use `select_related()` and `prefetch_related()`:

```python
# Bad - N+1 queries
stories = Story.objects.all()
for story in stories:
    print(story.project.name)  # Hits DB each time

# Good - 1 query
stories = Story.objects.select_related('project').all()
for story in stories:
    print(story.project.name)  # Uses cached data
```

### Caching

```python
from django.core.cache import cache

# Set cache
cache.set('key', 'value', timeout=300)

# Get cache
value = cache.get('key')

# Delete cache
cache.delete('key')
```

### Celery Tasks

For long-running operations, use Celery:

```python
from celery import shared_task

@shared_task
def process_large_dataset(data_id):
    # Long-running task
    pass
```

## Deployment

See `docs/project_planning/MASTER_DEVELOPMENT_PLAN.md` for complete deployment guide.

Quick checklist:
- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use production database
- [ ] Set up SSL/HTTPS
- [ ] Configure static files
- [ ] Set up Celery with supervisor
- [ ] Configure logging
- [ ] Set up monitoring

## Resources

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Celery Documentation: https://docs.celeryproject.org/
- Project Documentation: See `docs/` directory

## Getting Help

1. Check the documentation in `docs/`
2. Review the code and comments
3. Check Django/DRF documentation
4. Contact the development team
