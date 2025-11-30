from rest_framework import serializers
from .models import Workflow, WorkflowStep, WorkflowTemplate


class WorkflowStepSerializer(serializers.ModelSerializer):
    can_execute = serializers.BooleanField(read_only=True)

    class Meta:
        model = WorkflowStep
        fields = [
            'id', 'workflow', 'step_order', 'name', 'description', 'step_type',
            'status', 'config', 'input_data', 'output_data', 'agent_task',
            'depends_on', 'retry_count', 'max_retries', 'error_message',
            'created_at', 'updated_at', 'started_at', 'completed_at', 'can_execute'
        ]
        read_only_fields = [
            'id', 'output_data', 'retry_count', 'error_message',
            'created_at', 'updated_at', 'started_at', 'completed_at'
        ]


class WorkflowSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'workflow_type', 'status', 'config',
            'input_data', 'output_data', 'created_by', 'created_by_name',
            'current_step', 'total_steps', 'priority', 'created_at', 'updated_at',
            'started_at', 'completed_at', 'progress_percentage', 'steps'
        ]
        read_only_fields = [
            'id', 'created_by', 'output_data', 'current_step', 'total_steps',
            'created_at', 'updated_at', 'started_at', 'completed_at'
        ]


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = WorkflowTemplate
        fields = [
            'id', 'name', 'description', 'workflow_type', 'template_config',
            'is_active', 'created_by', 'created_by_name', 'usage_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'usage_count', 'created_at', 'updated_at'
        ]
