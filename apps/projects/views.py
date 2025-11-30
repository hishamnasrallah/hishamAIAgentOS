from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, Sprint, Epic, Story, Task
from .serializers import (
    ProjectSerializer, SprintSerializer, EpicSerializer,
    StorySerializer, TaskSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active', 'owner']
    search_fields = ['key', 'name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        project = self.get_object()
        return Response({
            'project': ProjectSerializer(project).data,
            'stats': {
                'total_stories': project.stories.count(),
                'completed_stories': project.stories.filter(status='DONE').count(),
                'active_sprints': project.sprints.filter(status='ACTIVE').count(),
                'total_epics': project.epics.count(),
            }
        })


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'status']

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        sprint = self.get_object()
        sprint.status = 'ACTIVE'
        sprint.save()
        return Response({'message': 'Sprint started'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        sprint = self.get_object()
        sprint.status = 'COMPLETED'
        sprint.save()
        return Response({'message': 'Sprint completed'})


class EpicViewSet(viewsets.ModelViewSet):
    queryset = Epic.objects.all()
    serializer_class = EpicSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'status', 'priority', 'generated_by_ai']
    search_fields = ['key', 'title', 'description']


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = [
        'project', 'epic', 'sprint', 'status', 'priority',
        'assignee', 'assigned_to_ai', 'generated_by_ai'
    ]
    search_fields = ['key', 'title', 'description']
    ordering_fields = ['created_at', 'priority', 'story_points']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def generate_from_idea(self, request):
        idea = request.data.get('idea', '')
        project_id = request.data.get('project_id')

        return Response({
            'message': 'Story generation initiated',
            'idea': idea,
            'project_id': project_id,
            'status': 'processing'
        })


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['story', 'status', 'assignee', 'assigned_to_ai']
