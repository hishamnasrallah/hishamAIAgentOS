from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.AgentTaskViewSet, basename='agent-task')
router.register(r'prompts', views.PromptViewSet, basename='prompt')
router.register(r'providers', views.AIProviderViewSet, basename='ai-provider')
router.register(r'executions', views.AgentExecutionViewSet, basename='execution')

urlpatterns = [
    path('', include(router.urls)),
]
