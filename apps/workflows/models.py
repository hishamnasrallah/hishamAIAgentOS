from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import HishamOSUser
from apps.agents.models import AgentTask


class WorkflowStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    RUNNING = 'RUNNING', _('Running')
    PAUSED = 'PAUSED', _('Paused')
    COMPLETED = 'COMPLETED', _('Completed')
    FAILED = 'FAILED', _('Failed')
    CANCELLED = 'CANCELLED', _('Cancelled')


class StepStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    RUNNING = 'RUNNING', _('Running')
    COMPLETED = 'COMPLETED', _('Completed')
    FAILED = 'FAILED', _('Failed')
    SKIPPED = 'SKIPPED', _('Skipped')


class Workflow(models.Model):
    """
    Represents a multi-step workflow that orchestrates multiple agents/tasks.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    workflow_type = models.CharField(
        max_length=50,
        choices=[
            ('BUG_LIFECYCLE', 'Bug Lifecycle'),
            ('FEATURE_DEVELOPMENT', 'Feature Development'),
            ('CHANGE_REQUEST', 'Change Request'),
            ('RELEASE', 'Release Process'),
            ('CODE_REVIEW', 'Code Review'),
            ('CUSTOM', 'Custom')
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.PENDING
    )
    config = models.JSONField(
        default=dict,
        help_text=_('Workflow configuration and parameters')
    )
    input_data = models.JSONField(
        default=dict,
        help_text=_('Input data for the workflow')
    )
    output_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Final output from the workflow')
    )
    created_by = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_workflows'
    )
    current_step = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    priority = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'workflows'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['workflow_type', 'status']),
            models.Index(fields=['created_by', 'status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.status}"

    @property
    def progress_percentage(self):
        if self.total_steps == 0:
            return 0
        return (self.current_step / self.total_steps) * 100


class WorkflowStep(models.Model):
    """
    Represents a single step in a workflow.
    """
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    step_order = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    step_type = models.CharField(
        max_length=50,
        choices=[
            ('AGENT_TASK', 'Agent Task'),
            ('HUMAN_APPROVAL', 'Human Approval'),
            ('CONDITION', 'Conditional Check'),
            ('PARALLEL', 'Parallel Execution'),
            ('WEBHOOK', 'Webhook Call'),
            ('DELAY', 'Delay/Wait')
        ],
        default='AGENT_TASK'
    )
    status = models.CharField(
        max_length=20,
        choices=StepStatus.choices,
        default=StepStatus.PENDING
    )
    config = models.JSONField(
        default=dict,
        help_text=_('Step configuration')
    )
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict, blank=True)
    agent_task = models.ForeignKey(
        AgentTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workflow_steps'
    )
    depends_on = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='dependent_steps'
    )
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'workflow_steps'
        ordering = ['workflow', 'step_order']
        unique_together = ['workflow', 'step_order']

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}: {self.name}"

    def can_execute(self):
        """Check if all dependencies are completed."""
        dependencies = self.depends_on.all()
        return all(dep.status == StepStatus.COMPLETED for dep in dependencies)


class WorkflowTemplate(models.Model):
    """
    Reusable workflow templates.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    workflow_type = models.CharField(max_length=50)
    template_config = models.JSONField(
        help_text=_('Template configuration including steps')
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_templates'
    )
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workflow_templates'
        ordering = ['name']

    def __str__(self):
        return self.name

    def instantiate(self, created_by, input_data):
        """Create a workflow instance from this template."""
        workflow = Workflow.objects.create(
            name=f"{self.name} - {created_by.username}",
            description=self.description,
            workflow_type=self.workflow_type,
            config=self.template_config,
            input_data=input_data,
            created_by=created_by
        )

        steps_config = self.template_config.get('steps', [])
        workflow.total_steps = len(steps_config)
        workflow.save()

        for i, step_config in enumerate(steps_config):
            WorkflowStep.objects.create(
                workflow=workflow,
                step_order=i,
                name=step_config['name'],
                description=step_config.get('description', ''),
                step_type=step_config['step_type'],
                config=step_config.get('config', {}),
                max_retries=step_config.get('max_retries', 3)
            )

        self.usage_count += 1
        self.save()

        return workflow
