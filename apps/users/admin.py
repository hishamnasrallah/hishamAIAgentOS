from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import HishamOSUser, UserPermission


@admin.register(HishamOSUser)
class HishamOSUserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Role & Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('AI Token Management'), {'fields': ('ai_token_limit', 'ai_tokens_used', 'last_token_reset')}),
        (_('Preferences'), {'fields': ('preferences',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission_name', 'resource_type', 'resource_id', 'granted_at', 'granted_by']
    list_filter = ['permission_name', 'resource_type', 'granted_at']
    search_fields = ['user__email', 'user__username', 'permission_name', 'resource_type']
    raw_id_fields = ['user', 'granted_by']
