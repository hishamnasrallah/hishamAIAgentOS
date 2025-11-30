from celery import shared_task
from django.utils import timezone
from typing import Dict, Any
import logging
import time

from .models import AgentTask, AgentExecution, AIProvider, Prompt, AgentType
from .base_agent import AgentFactory
from libs.ai_providers import OpenAIProvider, AnthropicProvider, OllamaProvider

logger = logging.getLogger(__name__)


def get_ai_provider_instance(provider: AIProvider):
    """Get AI provider instance from model."""

    if provider.provider_type == 'OPENAI':
        return OpenAIProvider(
            api_key=provider.api_key,
            model=provider.model_name,
            temperature=float(provider.temperature),
            max_tokens=provider.max_tokens
        )
    elif provider.provider_type == 'ANTHROPIC':
        return AnthropicProvider(
            api_key=provider.api_key,
            model=provider.model_name,
            temperature=float(provider.temperature),
            max_tokens=provider.max_tokens
        )
    elif provider.provider_type == 'OLLAMA':
        return OllamaProvider(
            model=provider.model_name,
            temperature=float(provider.temperature),
            max_tokens=provider.max_tokens,
            api_url=provider.api_url or 'http://localhost:11434'
        )
    else:
        raise ValueError(f"Unsupported provider type: {provider.provider_type}")


@shared_task(bind=True, max_retries=3)
def execute_agent_task(self, task_id: int) -> Dict[str, Any]:
    """
    Execute an agent task asynchronously.

    Args:
        task_id: The AgentTask ID to execute

    Returns:
        Dict containing execution results
    """
    try:
        task = AgentTask.objects.get(id=task_id)

        task.status = 'IN_PROGRESS'
        task.started_at = timezone.now()
        task.save()

        logger.info(f"Starting execution of task {task_id}: {task.title}")

        provider = AIProvider.objects.filter(
            is_active=True,
            provider_type='OPENAI'
        ).first()

        if not provider:
            provider = AIProvider.objects.filter(is_active=True).first()

        if not provider:
            raise ValueError("No active AI provider found")

        prompt = Prompt.objects.filter(
            agent_type=task.agent_type,
            is_active=True
        ).first()

        if not prompt:
            prompt = _create_default_prompt(task.agent_type)

        provider_instance = get_ai_provider_instance(provider)

        agent = AgentFactory.create_agent(
            agent_type=task.agent_type,
            provider=provider_instance,
            prompt=prompt
        )

        execution = AgentExecution.objects.create(
            task=task,
            agent_type=task.agent_type,
            provider=provider,
            prompt_used=prompt
        )

        start_time = time.time()

        result = agent.run_with_tracking(task, provider)

        execution_time = time.time() - start_time

        execution.execution_time_seconds = execution_time
        execution.success = True
        execution.save()

        task.status = 'COMPLETED'
        task.completed_at = timezone.now()
        task.execution_time_seconds = execution_time
        task.save()

        if task.created_by:
            task.created_by.increment_token_usage(execution.total_tokens)

        logger.info(f"Task {task_id} completed successfully in {execution_time:.2f}s")

        return {
            'task_id': task_id,
            'status': 'completed',
            'output': task.output_data,
            'execution_time': execution_time
        }

    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")

        if task:
            task.status = 'FAILED'
            task.error_message = str(e)
            task.save()

        raise self.retry(exc=e, countdown=60)


async def execute_agent_task_async(task_id: int) -> Dict[str, Any]:
    """
    Execute agent task asynchronously (for use in async contexts).

    Args:
        task_id: The AgentTask ID to execute

    Returns:
        Dict containing execution results
    """
    from asgiref.sync import sync_to_async

    result = await sync_to_async(execute_agent_task.apply_async)((task_id,))

    return await sync_to_async(result.get)(timeout=300)


def _create_default_prompt(agent_type: str) -> Prompt:
    """Create a default prompt if none exists."""

    default_prompts = {
        AgentType.CODING: """You are an expert software developer.
Your task is to write high-quality, production-ready code.
Follow best practices, include error handling, and write clean, maintainable code.""",

        AgentType.CODE_REVIEW: """You are a senior code reviewer.
Provide thorough, constructive feedback on code quality, security, performance, and best practices.
Rate the code on a scale of 1-10 and provide specific recommendations.""",

        AgentType.BA: """You are a business analyst expert.
Your task is to analyze requirements, create user stories, and define acceptance criteria.
Be thorough and consider edge cases.""",

        AgentType.DEVOPS: """You are a DevOps engineer expert.
Help with infrastructure, deployment, CI/CD, and operations tasks.
Focus on automation, reliability, and best practices.""",

        AgentType.QA: """You are a QA engineer expert.
Create comprehensive test plans, test cases, and identify potential bugs.
Think about edge cases and user scenarios.""",

        AgentType.PM: """You are a project manager expert.
Help plan projects, create timelines, identify risks, and coordinate tasks.
Focus on delivery and stakeholder management.""",

        AgentType.SCRUM_MASTER: """You are a Scrum Master expert.
Facilitate agile ceremonies, remove blockers, and ensure team productivity.
Focus on continuous improvement.""",

        AgentType.RELEASE_MANAGER: """You are a release manager expert.
Coordinate releases, manage deployment schedules, and ensure smooth rollouts.
Focus on risk mitigation and communication.""",

        AgentType.BUG_TRIAGE: """You are a bug triage specialist.
Analyze bugs, categorize severity, assign priority, and recommend fixes.
Be systematic and thorough.""",

        AgentType.SECURITY: """You are a security expert.
Identify security vulnerabilities, recommend fixes, and ensure best practices.
Focus on OWASP Top 10 and secure coding practices.""",

        AgentType.PERFORMANCE: """You are a performance optimization expert.
Analyze performance issues, recommend optimizations, and improve efficiency.
Focus on bottlenecks and scalability.""",

        AgentType.DOCUMENTATION: """You are a documentation specialist.
Create clear, comprehensive documentation for code, APIs, and systems.
Focus on clarity and completeness.""",

        AgentType.UI_UX: """You are a UI/UX designer expert.
Design intuitive user interfaces and optimize user experience.
Focus on usability, accessibility, and aesthetics.""",

        AgentType.DATA_ANALYST: """You are a data analyst expert.
Analyze data, create insights, and make data-driven recommendations.
Focus on accuracy and actionable insights.""",

        AgentType.SUPPORT: """You are a customer support specialist.
Help users solve problems, answer questions, and provide excellent service.
Be patient, clear, and helpful.""",
    }

    system_prompt = default_prompts.get(
        agent_type,
        "You are a helpful AI assistant. Complete the task to the best of your ability."
    )

    prompt = Prompt.objects.create(
        agent_type=agent_type,
        name=f"Default {agent_type} Prompt",
        system_prompt=system_prompt,
        version="1.0",
        is_active=True
    )

    logger.info(f"Created default prompt for {agent_type}")

    return prompt


@shared_task
def cleanup_old_tasks():
    """Cleanup old completed/failed tasks (older than 90 days)."""
    from datetime import timedelta

    threshold_date = timezone.now() - timedelta(days=90)

    old_tasks = AgentTask.objects.filter(
        status__in=['COMPLETED', 'FAILED', 'CANCELLED'],
        completed_at__lt=threshold_date
    )

    count = old_tasks.count()
    old_tasks.delete()

    logger.info(f"Cleaned up {count} old tasks")

    return {'deleted_count': count}


@shared_task
def reset_stuck_tasks():
    """Reset tasks that have been stuck in IN_PROGRESS for >1 hour."""
    from datetime import timedelta

    threshold_time = timezone.now() - timedelta(hours=1)

    stuck_tasks = AgentTask.objects.filter(
        status='IN_PROGRESS',
        started_at__lt=threshold_time
    )

    count = 0
    for task in stuck_tasks:
        task.status = 'PENDING'
        task.error_message = 'Task was stuck and has been reset'
        task.save()
        count += 1

    logger.warning(f"Reset {count} stuck tasks")

    return {'reset_count': count}
