from django.contrib import admin
from .models import Workflow, WorkflowStep, WorkflowTemplate


class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 0
    readonly_fields = ['status', 'started_at', 'completed_at']


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'workflow_type', 'status', 'progress_percentage', 'created_by', 'created_at']
    list_filter = ['workflow_type', 'status', 'priority', 'created_at']
    search_fields = ['name', 'description']
    raw_id_fields = ['created_by']
    readonly_fields = ['current_step', 'total_steps', 'created_at', 'updated_at']
    inlines = [WorkflowStepInline]


@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'workflow', 'step_order', 'name', 'step_type', 'status']
    list_filter = ['step_type', 'status', 'created_at']
    search_fields = ['name', 'description']
    raw_id_fields = ['workflow', 'agent_task']


@admin.register(WorkflowTemplate)
class WorkflowTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'workflow_type', 'is_active', 'usage_count', 'created_at']
    list_filter = ['workflow_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    raw_id_fields = ['created_by']
