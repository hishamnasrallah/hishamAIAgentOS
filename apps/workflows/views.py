from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Workflow, WorkflowStep, WorkflowTemplate
from .serializers import WorkflowSerializer, WorkflowStepSerializer, WorkflowTemplateSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['workflow_type', 'status', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'priority']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        workflow = self.get_object()
        workflow.status = 'RUNNING'
        workflow.save()
        return Response({
            'message': 'Workflow started',
            'workflow_id': workflow.id,
            'status': workflow.status
        })

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        workflow = self.get_object()
        workflow.status = 'PAUSED'
        workflow.save()
        return Response({
            'message': 'Workflow paused',
            'workflow_id': workflow.id
        })

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        workflow = self.get_object()
        workflow.status = 'RUNNING'
        workflow.save()
        return Response({
            'message': 'Workflow resumed',
            'workflow_id': workflow.id
        })


class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['workflow', 'step_type', 'status']


class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['workflow_type', 'is_active']

    @action(detail=True, methods=['post'])
    def instantiate(self, request, pk=None):
        template = self.get_object()
        input_data = request.data.get('input_data', {})
        workflow = template.instantiate(request.user, input_data)
        return Response({
            'message': 'Workflow created from template',
            'workflow_id': workflow.id,
            'workflow': WorkflowSerializer(workflow).data
        })
