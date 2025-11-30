import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.demo')
django.setup()

from apps.agents.models import AgentTask, AgentType, AIProvider, Prompt
from apps.agents.base_agent import AgentFactory
from libs.ai_providers.ollama_provider import OllamaProvider
import json


def create_test_prompts():
    """Create default prompts for all agent types."""
    prompts = {}

    agent_prompts = {
        AgentType.CODING: "You are an expert software developer. Write clean, efficient, and well-documented code.",
        AgentType.CODE_REVIEW: "You are a FAANG-level code reviewer. Provide thorough, constructive code reviews.",
        AgentType.BA: "You are an expert Business Analyst. Elicit requirements and create detailed user stories.",
        AgentType.DEVOPS: "You are a DevOps expert. Design infrastructure and automate deployments.",
        AgentType.QA: "You are a QA expert. Create comprehensive test plans and test cases.",
        AgentType.PM: "You are an experienced Project Manager. Plan projects and manage risks effectively.",
        AgentType.SCRUM_MASTER: "You are a certified Scrum Master. Facilitate agile ceremonies and remove blockers.",
        AgentType.RELEASE_MANAGER: "You are a Release Manager. Coordinate releases and manage deployments.",
        AgentType.BUG_TRIAGE: "You are a Bug Triage expert. Analyze bugs and assign appropriate priorities.",
        AgentType.SECURITY: "You are a Security expert. Identify vulnerabilities and security risks.",
        AgentType.PERFORMANCE: "You are a Performance expert. Optimize code and identify bottlenecks.",
        AgentType.DOCUMENTATION: "You are a technical writer. Create clear, comprehensive documentation.",
        AgentType.UI_UX: "You are a UI/UX designer. Create beautiful, user-friendly interfaces.",
        AgentType.DATA_ANALYST: "You are a Data Analyst. Analyze data and extract actionable insights.",
        AgentType.SUPPORT: "You are a Customer Support expert. Help users solve problems effectively.",
    }

    for agent_type, system_prompt in agent_prompts.items():
        prompt, created = Prompt.objects.get_or_create(
            name=f"Default {agent_type} Prompt",
            agent_type=agent_type,
            defaults={
                'system_prompt': system_prompt,
                'version': '1.0',
                'is_active': True
            }
        )
        prompts[agent_type] = prompt
        if created:
            print(f"✓ Created prompt for {agent_type}")

    return prompts


def test_agent(agent_type, task_data):
    """Test a specific agent."""
    print(f"\n{'='*60}")
    print(f"Testing {agent_type} Agent")
    print('='*60)

    try:
        task = AgentTask.objects.create(
            agent_type=agent_type,
            title=task_data['title'],
            description=task_data.get('description', ''),
            input_data=task_data['input_data'],
            status='PENDING'
        )

        print(f"✓ Task created: {task.title}")
        print(f"  Input: {json.dumps(task.input_data, indent=2)}")

        prompt = Prompt.objects.filter(agent_type=agent_type, is_active=True).first()
        if not prompt:
            print(f"✗ No prompt found for {agent_type}")
            return False

        try:
            provider_instance = OllamaProvider(
                model="qwen2.5-coder:0.5b",
                api_url="http://localhost:11434",
                temperature=0.7
            )

            agent = AgentFactory.create_agent(
                agent_type=agent_type,
                provider=provider_instance,
                prompt=prompt
            )

            print(f"✓ Agent created: {agent.agent_name}")
            print(f"  Capabilities: {', '.join(agent.capabilities)}")

            print("\n  Executing task (dry run - no actual AI call)...")
            print(f"  Would call AI with prompt: {prompt.system_prompt[:100]}...")

            task.status = 'SIMULATED'
            task.save()

            print(f"\n✓ {agent_type} agent test PASSED (simulation)")
            return True

        except Exception as e:
            print(f"\n✗ Error during agent execution: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"\n✗ Error creating task: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run tests for all agents."""
    print("\n" + "="*60)
    print("HISHAMOS - AGENT TEST SUITE")
    print("="*60)

    print("\nCreating prompts...")
    prompts = create_test_prompts()

    test_cases = {
        AgentType.CODING: {
            'title': 'Create REST API endpoint',
            'input_data': {
                'task_type': 'NEW_BUILD',
                'language': 'Python',
                'requirements': 'Create a REST API endpoint for user registration using Django REST Framework'
            }
        },
        AgentType.CODE_REVIEW: {
            'title': 'Review authentication code',
            'input_data': {
                'code': 'def login(username, password):\n    return User.objects.get(username=username)',
                'language': 'Python',
            }
        },
        AgentType.BA: {
            'title': 'Generate user stories for e-commerce',
            'input_data': {
                'task_type': 'GENERATE_STORIES',
                'idea': 'E-commerce platform with shopping cart and checkout'
            }
        },
        AgentType.DEVOPS: {
            'title': 'Create CI/CD pipeline',
            'input_data': {
                'task_type': 'CI_CD',
                'technology': 'GitHub Actions',
                'requirements': 'Set up CI/CD for Django application'
            }
        },
        AgentType.QA: {
            'title': 'Create test cases for login',
            'input_data': {
                'task_type': 'TEST_CASES',
                'feature': 'User login functionality',
                'requirements': 'Test user authentication with username and password'
            }
        },
        AgentType.PM: {
            'title': 'Create project plan',
            'input_data': {
                'task_type': 'PLAN',
                'project': 'Mobile app development',
                'requirements': 'iOS and Android app for task management'
            }
        },
        AgentType.SCRUM_MASTER: {
            'title': 'Plan sprint',
            'input_data': {
                'task_type': 'SPRINT_PLAN',
                'team_context': '5 developers, 2-week sprint',
                'requirements': 'Sprint 10 - Focus on user authentication features'
            }
        },
        AgentType.RELEASE_MANAGER: {
            'title': 'Create release plan',
            'input_data': {
                'task_type': 'PLAN',
                'release': 'v2.0.0',
                'requirements': 'Major release with new features and breaking changes'
            }
        },
        AgentType.BUG_TRIAGE: {
            'title': 'Triage login bug',
            'input_data': {
                'task_type': 'TRIAGE',
                'bug_report': 'Users cannot login after password reset'
            }
        },
        AgentType.SECURITY: {
            'title': 'Security audit',
            'input_data': {
                'task_type': 'AUDIT',
                'system': 'Web application with user authentication and payment processing'
            }
        },
        AgentType.PERFORMANCE: {
            'title': 'Optimize database query',
            'input_data': {
                'task_type': 'OPTIMIZE',
                'code': 'for user in User.objects.all():\n    print(user.profile.avatar)',
                'system': 'Django ORM queries'
            }
        },
        AgentType.DOCUMENTATION: {
            'title': 'Document API',
            'input_data': {
                'task_type': 'API_DOCS',
                'system': 'RESTful API with authentication and CRUD operations'
            }
        },
        AgentType.UI_UX: {
            'title': 'Design login screen',
            'input_data': {
                'task_type': 'DESIGN',
                'feature': 'User login screen',
                'requirements': 'Mobile-first design with email and password fields'
            }
        },
        AgentType.DATA_ANALYST: {
            'title': 'Analyze user metrics',
            'input_data': {
                'task_type': 'ANALYZE',
                'data': 'User signups: 1000/month, Retention: 45%, Churn: 15%',
                'question': 'How can we improve user retention?'
            }
        },
        AgentType.SUPPORT: {
            'title': 'Help user with login issue',
            'input_data': {
                'task_type': 'TROUBLESHOOT',
                'issue': 'User cannot login, gets "Invalid credentials" error',
                'user_context': {'browser': 'Chrome', 'device': 'Desktop'}
            }
        }
    }

    results = {}
    for agent_type, task_data in test_cases.items():
        success = test_agent(agent_type, task_data)
        results[agent_type] = success

    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    passed = sum(1 for success in results.values() if success)
    total = len(results)

    for agent_type, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {agent_type}")

    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} agents passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print('='*60)

    print("\n" + "="*60)
    print("AGENT CAPABILITIES SUMMARY")
    print("="*60)

    for agent_type in AgentType.choices:
        agent_type_value = agent_type[0]
        try:
            prompt = Prompt.objects.filter(agent_type=agent_type_value, is_active=True).first()
            if prompt:
                provider_instance = OllamaProvider(model="qwen2.5-coder:0.5b", api_url="http://localhost:11434")
                agent = AgentFactory.create_agent(agent_type_value, provider_instance, prompt)
                print(f"\n{agent.agent_name}")
                print(f"  Type: {agent.agent_type}")
                print(f"  Capabilities: {len(agent.capabilities)}")
                for cap in agent.capabilities:
                    print(f"    - {cap}")
        except Exception as e:
            print(f"\n{agent_type_value}: Error - {str(e)}")

    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
