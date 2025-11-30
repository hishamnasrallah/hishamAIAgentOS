import logging
from typing import Dict, Any, List, Optional
from django.utils import timezone
from django.db import transaction
from apps.agents.models import AgentTask, AgentType
from .models import Workflow, WorkflowStep, StepStatus, WorkflowStatus
import asyncio

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Orchestrates workflow execution with dependency resolution and error handling.
    """

    def __init__(self):
        self.logger = logger

    async def execute_workflow(self, workflow_id: int, input_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute a workflow from start to finish.

        Args:
            workflow_id: The workflow to execute
            input_data: Optional input data to override workflow's input_data

        Returns:
            Dict containing execution results
        """
        try:
            workflow = await self._get_workflow(workflow_id)

            if workflow.status == WorkflowStatus.RUNNING:
                raise ValueError(f"Workflow {workflow_id} is already running")

            if input_data:
                workflow.input_data = input_data

            workflow.status = WorkflowStatus.RUNNING
            workflow.started_at = timezone.now()
            await self._save_workflow(workflow)

            self.logger.info(f"Starting workflow execution: {workflow.name} (ID: {workflow_id})")

            steps = await self._get_workflow_steps(workflow)
            workflow.total_steps = len(steps)
            await self._save_workflow(workflow)

            results = {}

            for step in steps:
                if not await self._can_execute_step(step):
                    self.logger.info(f"Waiting for dependencies for step: {step.name}")
                    continue

                try:
                    step_result = await self._execute_step(workflow, step)
                    results[step.name] = step_result
                    workflow.current_step += 1
                    await self._save_workflow(workflow)

                except Exception as e:
                    self.logger.error(f"Step {step.name} failed: {str(e)}")

                    if step.retry_count < step.max_retries:
                        step.retry_count += 1
                        await self._save_step(step)
                        self.logger.info(f"Retrying step {step.name} (attempt {step.retry_count})")
                        step_result = await self._execute_step(workflow, step)
                        results[step.name] = step_result
                    else:
                        step.status = StepStatus.FAILED
                        step.error_message = str(e)
                        await self._save_step(step)

                        workflow.status = WorkflowStatus.FAILED
                        await self._save_workflow(workflow)
                        raise

            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = timezone.now()
            workflow.output_data = results
            await self._save_workflow(workflow)

            self.logger.info(f"Workflow {workflow.name} completed successfully")

            return {
                'workflow_id': workflow.id,
                'status': workflow.status,
                'results': results,
                'execution_time': (workflow.completed_at - workflow.started_at).total_seconds()
            }

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            raise

    async def _execute_step(self, workflow: Workflow, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single workflow step."""

        step.status = StepStatus.RUNNING
        step.started_at = timezone.now()
        await self._save_step(step)

        self.logger.info(f"Executing step: {step.name} (type: {step.step_type})")

        result = {}

        if step.step_type == 'AGENT_TASK':
            result = await self._execute_agent_task_step(workflow, step)
        elif step.step_type == 'HUMAN_APPROVAL':
            result = await self._handle_human_approval(step)
        elif step.step_type == 'CONDITION':
            result = await self._evaluate_condition(step)
        elif step.step_type == 'WEBHOOK':
            result = await self._call_webhook(step)
        elif step.step_type == 'DELAY':
            result = await self._handle_delay(step)
        else:
            raise ValueError(f"Unknown step type: {step.step_type}")

        step.status = StepStatus.COMPLETED
        step.completed_at = timezone.now()
        step.output_data = result
        await self._save_step(step)

        return result

    async def _execute_agent_task_step(self, workflow: Workflow, step: WorkflowStep) -> Dict[str, Any]:
        """Execute an agent task as part of a workflow step."""

        from apps.agents.tasks import execute_agent_task_async

        if step.agent_task:
            task = step.agent_task
        else:
            agent_type = step.config.get('agent_type')
            task_data = step.config.get('task_data', {})

            task = await self._create_agent_task(
                agent_type=agent_type,
                title=step.name,
                description=step.description or step.name,
                input_data={**workflow.input_data, **step.input_data, **task_data},
                created_by=workflow.created_by
            )

            step.agent_task = task
            await self._save_step(step)

        result = await execute_agent_task_async(task.id)

        return result

    async def _handle_human_approval(self, step: WorkflowStep) -> Dict[str, Any]:
        """Handle human approval step - marks as pending approval."""

        step.status = StepStatus.PENDING
        await self._save_step(step)

        self.logger.info(f"Step {step.name} awaiting human approval")

        return {
            'status': 'pending_approval',
            'message': 'Awaiting human approval'
        }

    async def _evaluate_condition(self, step: WorkflowStep) -> Dict[str, Any]:
        """Evaluate a conditional step."""

        condition = step.config.get('condition')
        context = step.input_data

        result = eval(condition, {"__builtins__": {}}, context)

        return {
            'condition': condition,
            'result': result,
            'action': 'continue' if result else 'skip'
        }

    async def _call_webhook(self, step: WorkflowStep) -> Dict[str, Any]:
        """Call an external webhook."""

        import aiohttp

        url = step.config.get('url')
        method = step.config.get('method', 'POST')
        headers = step.config.get('headers', {})
        payload = step.input_data

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=payload, headers=headers) as response:
                result = await response.json()

                return {
                    'status_code': response.status,
                    'response': result
                }

    async def _handle_delay(self, step: WorkflowStep) -> Dict[str, Any]:
        """Handle a delay/wait step."""

        delay_seconds = step.config.get('delay_seconds', 60)

        await asyncio.sleep(delay_seconds)

        return {
            'delayed': delay_seconds,
            'message': f'Waited for {delay_seconds} seconds'
        }

    async def _can_execute_step(self, step: WorkflowStep) -> bool:
        """Check if a step's dependencies are met."""
        return step.can_execute()

    async def _get_workflow(self, workflow_id: int) -> Workflow:
        """Get workflow instance (async wrapper)."""
        from asgiref.sync import sync_to_async
        return await sync_to_async(Workflow.objects.get)(id=workflow_id)

    async def _get_workflow_steps(self, workflow: Workflow) -> List[WorkflowStep]:
        """Get all steps for a workflow."""
        from asgiref.sync import sync_to_async
        return await sync_to_async(list)(workflow.steps.all().order_by('step_order'))

    async def _save_workflow(self, workflow: Workflow):
        """Save workflow (async wrapper)."""
        from asgiref.sync import sync_to_async
        await sync_to_async(workflow.save)()

    async def _save_step(self, step: WorkflowStep):
        """Save step (async wrapper)."""
        from asgiref.sync import sync_to_async
        await sync_to_async(step.save)()

    async def _create_agent_task(self, **kwargs) -> AgentTask:
        """Create agent task (async wrapper)."""
        from asgiref.sync import sync_to_async
        return await sync_to_async(AgentTask.objects.create)(**kwargs)

    def pause_workflow(self, workflow_id: int):
        """Pause a running workflow."""
        workflow = Workflow.objects.get(id=workflow_id)
        workflow.status = WorkflowStatus.PAUSED
        workflow.save()

        self.logger.info(f"Workflow {workflow_id} paused")

    def resume_workflow(self, workflow_id: int):
        """Resume a paused workflow."""
        workflow = Workflow.objects.get(id=workflow_id)

        if workflow.status != WorkflowStatus.PAUSED:
            raise ValueError(f"Workflow {workflow_id} is not paused")

        workflow.status = WorkflowStatus.RUNNING
        workflow.save()

        self.logger.info(f"Workflow {workflow_id} resumed")

    def cancel_workflow(self, workflow_id: int):
        """Cancel a workflow."""
        workflow = Workflow.objects.get(id=workflow_id)
        workflow.status = WorkflowStatus.CANCELLED
        workflow.save()

        self.logger.info(f"Workflow {workflow_id} cancelled")


class WorkflowTemplateInstantiator:
    """Creates workflow instances from templates."""

    @staticmethod
    def create_from_template(template_id: int, created_by, input_data: Dict) -> Workflow:
        """
        Create a workflow instance from a template.

        Args:
            template_id: The template to use
            created_by: User creating the workflow
            input_data: Input data for the workflow

        Returns:
            Created Workflow instance
        """
        from .models import WorkflowTemplate

        template = WorkflowTemplate.objects.get(id=template_id)

        return template.instantiate(created_by, input_data)
