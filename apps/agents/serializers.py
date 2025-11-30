from rest_framework import serializers
from .models import AgentTask, Prompt, AIProvider, AgentExecution


class AgentTaskSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)

    class Meta:
        model = AgentTask
        fields = [
            'id', 'agent_type', 'title', 'description', 'input_data',
            'output_data', 'status', 'priority', 'created_by', 'created_by_name',
            'assigned_to', 'assigned_to_name', 'parent_task', 'tokens_used',
            'execution_time_seconds', 'error_message', 'created_at', 'updated_at',
            'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'output_data', 'tokens_used',
            'execution_time_seconds', 'error_message', 'created_at',
            'updated_at', 'started_at', 'completed_at'
        ]


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = [
            'id', 'agent_type', 'name', 'system_prompt', 'version',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIProviderSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = AIProvider
        fields = [
            'id', 'name', 'provider_type', 'api_key', 'api_url',
            'model_name', 'is_active', 'max_tokens', 'temperature',
            'config', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AgentExecutionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = AgentExecution
        fields = [
            'id', 'task', 'task_title', 'agent_type', 'provider', 'provider_name',
            'prompt_used', 'input_tokens', 'output_tokens', 'total_tokens',
            'execution_time_seconds', 'success', 'error_message',
            'raw_request', 'raw_response', 'created_at'
        ]
        read_only_fields = '__all__'
