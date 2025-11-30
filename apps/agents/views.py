from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AgentTask, Prompt, AIProvider, AgentExecution
from .serializers import (
    AgentTaskSerializer, PromptSerializer,
    AIProviderSerializer, AgentExecutionSerializer
)


class AgentTaskViewSet(viewsets.ModelViewSet):
    queryset = AgentTask.objects.all()
    serializer_class = AgentTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['agent_type', 'status', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'status']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        task = self.get_object()
        return Response({
            'message': 'Task execution initiated',
            'task_id': task.id,
            'status': task.status
        })


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['agent_type', 'is_active']
    search_fields = ['name', 'agent_type']


class AIProviderViewSet(viewsets.ModelViewSet):
    queryset = AIProvider.objects.all()
    serializer_class = AIProviderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['provider_type', 'is_active']

    @action(detail=True, methods=['post'])
    def health_check(self, request, pk=None):
        provider = self.get_object()
        return Response({
            'provider': provider.name,
            'healthy': provider.is_active,
            'message': 'Health check completed'
        })


class AgentExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AgentExecution.objects.all()
    serializer_class = AgentExecutionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['agent_type', 'success', 'provider']
    ordering_fields = ['created_at', 'execution_time_seconds']
