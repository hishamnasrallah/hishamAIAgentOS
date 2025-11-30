from rest_framework import serializers
from .models import Project, ProjectMembership, Sprint, Epic, Story, Task, Comment


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'user_name', 'user_email', 'role', 'joined_at']


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    memberships = ProjectMembershipSerializer(
        source='projectmembership_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            'id', 'key', 'name', 'description', 'owner', 'owner_name',
            'is_active', 'settings', 'created_at', 'updated_at', 'memberships'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SprintSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Sprint
        fields = [
            'id', 'project', 'project_name', 'name', 'goal', 'start_date',
            'end_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EpicSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Epic
        fields = [
            'id', 'project', 'project_name', 'key', 'title', 'description',
            'owner', 'owner_name', 'status', 'priority', 'generated_by_ai',
            'ai_confidence', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'key', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source='assignee.get_full_name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'story', 'title', 'description', 'assignee', 'assignee_name',
            'assigned_to_ai', 'status', 'estimated_hours', 'actual_hours',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'story', 'author', 'author_name', 'content',
            'is_ai_generated', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class StorySerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    epic_title = serializers.CharField(source='epic.title', read_only=True)
    sprint_name = serializers.CharField(source='sprint.name', read_only=True)
    assignee_name = serializers.CharField(source='assignee.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id', 'project', 'project_name', 'epic', 'epic_title',
            'sprint', 'sprint_name', 'key', 'title', 'description',
            'acceptance_criteria', 'story_points', 'assignee', 'assignee_name',
            'assigned_to_ai', 'status', 'priority', 'generated_by_ai',
            'ai_confidence', 'technical_notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'tasks', 'comments'
        ]
        read_only_fields = ['id', 'key', 'created_by', 'created_at', 'updated_at']
