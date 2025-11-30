from django.contrib import admin
from .models import AgentTask, Prompt, AIProvider, AgentExecution


@admin.register(AgentTask)
class AgentTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'agent_type', 'status', 'priority', 'created_by', 'created_at']
    list_filter = ['agent_type', 'status', 'priority', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['created_by', 'assigned_to', 'parent_task']
    readonly_fields = ['tokens_used', 'execution_time_seconds', 'created_at', 'updated_at']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['id', 'agent_type', 'name', 'version', 'is_active', 'created_at']
    list_filter = ['agent_type', 'is_active', 'created_at']
    search_fields = ['name', 'agent_type']


@admin.register(AIProvider)
class AIProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'provider_type', 'model_name', 'is_active', 'created_at']
    list_filter = ['provider_type', 'is_active', 'created_at']
    search_fields = ['name', 'model_name']


@admin.register(AgentExecution)
class AgentExecutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'agent_type', 'task', 'provider', 'success', 'total_tokens', 'created_at']
    list_filter = ['agent_type', 'success', 'provider', 'created_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return []
