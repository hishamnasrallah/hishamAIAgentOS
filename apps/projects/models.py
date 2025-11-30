from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import HishamOSUser


class Project(models.Model):
    """Main project model - like a Jira project."""

    key = models.CharField(max_length=10, unique=True, help_text=_('Project key (e.g., PROJ)'))
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_projects'
    )
    members = models.ManyToManyField(
        HishamOSUser,
        through='ProjectMembership',
        related_name='projects'
    )
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.key} - {self.name}"


class ProjectMembership(models.Model):
    """Project team membership with roles."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(HishamOSUser, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=[
            ('OWNER', 'Owner'),
            ('ADMIN', 'Admin'),
            ('DEVELOPER', 'Developer'),
            ('VIEWER', 'Viewer')
        ],
        default='DEVELOPER'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_memberships'
        unique_together = ['project', 'user']

    def __str__(self):
        return f"{self.user.email} - {self.project.key} ({self.role})"


class Sprint(models.Model):
    """Sprint model for agile projects."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=255)
    goal = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PLANNING', 'Planning'),
            ('ACTIVE', 'Active'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled')
        ],
        default='PLANNING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sprints'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class Epic(models.Model):
    """Epic model - large body of work."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='epics')
    key = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_epics'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done')
        ],
        default='TODO'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('CRITICAL', 'Critical')
        ],
        default='MEDIUM'
    )
    generated_by_ai = models.BooleanField(default=False)
    ai_confidence = models.FloatField(null=True, blank=True, help_text=_('AI confidence score 0-1'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'epics'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.key} - {self.title}"


class Story(models.Model):
    """User story model."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stories')
    epic = models.ForeignKey(
        Epic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stories'
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stories'
    )
    key = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    acceptance_criteria = models.JSONField(
        default=list,
        help_text=_('List of acceptance criteria')
    )
    story_points = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Story points estimate')
    )
    assignee = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_stories'
    )
    assigned_to_ai = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('BACKLOG', 'Backlog'),
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('IN_REVIEW', 'In Review'),
            ('TESTING', 'Testing'),
            ('DONE', 'Done')
        ],
        default='BACKLOG'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('CRITICAL', 'Critical')
        ],
        default='MEDIUM'
    )
    generated_by_ai = models.BooleanField(default=False)
    ai_confidence = models.FloatField(null=True, blank=True)
    technical_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_stories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stories'
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return f"{self.key} - {self.title}"


class Task(models.Model):
    """Task model - smaller unit of work within a story."""

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks_pm'
    )
    assigned_to_ai = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done')
        ],
        default='TODO'
    )
    estimated_hours = models.FloatField(null=True, blank=True)
    actual_hours = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['story', 'created_at']

    def __str__(self):
        return f"{self.story.key} - {self.title}"


class Comment(models.Model):
    """Comments on stories."""

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(HishamOSUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    is_ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.story.key} by {self.author}"
