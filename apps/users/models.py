from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    DEVELOPER = 'DEVELOPER', _('Developer')
    MANAGER = 'MANAGER', _('Manager')
    VIEWER = 'VIEWER', _('Viewer')


class HishamOSUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEVELOPER,
        help_text=_('User role for RBAC')
    )
    avatar = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text=_('User avatar URL')
    )
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('User preferences and settings')
    )
    ai_token_limit = models.IntegerField(
        default=100000,
        help_text=_('Monthly AI token usage limit')
    )
    ai_tokens_used = models.IntegerField(
        default=0,
        help_text=_('AI tokens used this month')
    )
    last_token_reset = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Last time token counter was reset')
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def has_ai_tokens_available(self):
        return self.ai_tokens_used < self.ai_token_limit

    def increment_token_usage(self, tokens):
        self.ai_tokens_used += tokens
        self.save(update_fields=['ai_tokens_used'])

    def reset_token_usage(self):
        self.ai_tokens_used = 0
        self.last_token_reset = models.functions.Now()
        self.save(update_fields=['ai_tokens_used', 'last_token_reset'])


class UserPermission(models.Model):
    user = models.ForeignKey(
        HishamOSUser,
        on_delete=models.CASCADE,
        related_name='custom_permissions'
    )
    permission_name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        HishamOSUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='permissions_granted'
    )

    class Meta:
        db_table = 'user_permissions'
        unique_together = ['user', 'permission_name', 'resource_type', 'resource_id']
        verbose_name = _('User Permission')
        verbose_name_plural = _('User Permissions')

    def __str__(self):
        return f"{self.user.email} - {self.permission_name} on {self.resource_type}"
