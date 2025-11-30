from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import HishamOSUser


class AgentType(models.TextChoices):
    CODING = 'CODING', _('Coding Agent')
    CODE_REVIEW = 'CODE_REVIEW', _('Code Reviewer')
    DEVOPS = 'DEVOPS', _('DevOps Agent')
    QA = 'QA', _('QA Agent')
    BA = 'BA', _('Business Analyst')
    PM = 'PM', _('Project Manager')
    SCRUM_MASTER = 'SCRUM_MASTER', _('Scrum Master')
    RELEASE_MANAGER = 'RELEASE_MANAGER', _('Release Manager')
    BUG_TRIAGE = 'BUG_TRIAGE', _('Bug Triage Agent')
    SECURITY = 'SECURITY', _('Security Agent')
    PERFORMANCE = 'PERFORMANCE', _('Performance Agent')
    DOCUMENTATION = 'DOCUMENTATION', _('Documentation Agent')
    UI_UX = 'UI_UX', _('UI/UX Agent')
    DATA_ANALYST = 'DATA_ANALYST', _('Data Analyst')
    SUPPORT = 'SUPPORT', _('Support Agent')


class TaskStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    COMPLETED = 'COMPLETED', _('Completed')
    FAILED = 'FAILED', _('Failed')
    CANCELLED = 'CANCELLED', _('Cancelled')


class AgentTask(models.Model):
    agent_type = models.CharField(
        max_length=50,
        choices=AgentType.choices,
        help_text=_('Type of agent to handle this task')
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    input_data = models.JSONField(
        default=dict,
        help_text=_('Input parameters for the task')
    )
    output_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Output result from the agent')
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    priority = models.IntegerField(default=5, help_text=_('1-10, where 1 is highest priority'))
    created_by = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text=_('Human user assigned to review/approve')
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks'
    )
    tokens_used = models.IntegerField(default=0)
    execution_time_seconds = models.FloatField(default=0.0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'agent_tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['agent_type', 'status']),
            models.Index(fields=['created_by', 'status']),
            models.Index(fields=['priority', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.agent_type}] {self.title} - {self.status}"


class Prompt(models.Model):
    agent_type = models.CharField(
        max_length=50,
        choices=AgentType.choices,
        help_text=_('Agent type this prompt belongs to')
    )
    name = models.CharField(max_length=100, help_text=_('Prompt identifier'))
    system_prompt = models.TextField(help_text=_('System prompt for the agent'))
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prompts'
        unique_together = ['agent_type', 'name', 'version']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agent_type} - {self.name} v{self.version}"


class AIProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    provider_type = models.CharField(
        max_length=20,
        choices=[
            ('OPENAI', 'OpenAI'),
            ('ANTHROPIC', 'Anthropic'),
            ('GOOGLE', 'Google'),
            ('OLLAMA', 'Ollama'),
            ('CUSTOM', 'Custom')
        ]
    )
    api_key = models.CharField(max_length=500, blank=True)
    api_url = models.URLField(blank=True)
    model_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    max_tokens = models.IntegerField(default=4096)
    temperature = models.FloatField(default=0.7)
    config = models.JSONField(default=dict, help_text=_('Additional configuration'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_providers'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.provider_type})"


class AgentExecution(models.Model):
    task = models.ForeignKey(AgentTask, on_delete=models.CASCADE, related_name='executions')
    agent_type = models.CharField(max_length=50, choices=AgentType.choices)
    provider = models.ForeignKey(AIProvider, on_delete=models.SET_NULL, null=True)
    prompt_used = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    execution_time_seconds = models.FloatField(default=0.0)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    raw_request = models.JSONField(default=dict)
    raw_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agent_executions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agent_type} - {self.task.title} - {'Success' if self.success else 'Failed'}"
