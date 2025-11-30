from django.contrib import admin
from .models import Project, ProjectMembership, Sprint, Epic, Story, Task, Comment


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'name', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['key', 'name', 'description']
    raw_id_fields = ['owner']
    inlines = [ProjectMembershipInline]


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'project', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'start_date', 'project']
    search_fields = ['name', 'goal']
    raw_id_fields = ['project']


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'title', 'project', 'status', 'priority', 'generated_by_ai']
    list_filter = ['status', 'priority', 'generated_by_ai', 'created_at']
    search_fields = ['key', 'title', 'description']
    raw_id_fields = ['project', 'owner']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'key', 'title', 'project', 'status', 'priority',
        'story_points', 'assigned_to_ai', 'generated_by_ai'
    ]
    list_filter = [
        'status', 'priority', 'assigned_to_ai', 'generated_by_ai', 'created_at'
    ]
    search_fields = ['key', 'title', 'description']
    raw_id_fields = ['project', 'epic', 'sprint', 'assignee', 'created_by']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'story', 'status', 'assignee', 'assigned_to_ai']
    list_filter = ['status', 'assigned_to_ai', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['story', 'assignee']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'author', 'is_ai_generated', 'created_at']
    list_filter = ['is_ai_generated', 'created_at']
    search_fields = ['content']
    raw_id_fields = ['story', 'author']
