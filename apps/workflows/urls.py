from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'workflows', views.WorkflowViewSet, basename='workflow')
router.register(r'steps', views.WorkflowStepViewSet, basename='workflow-step')
router.register(r'templates', views.WorkflowTemplateViewSet, basename='workflow-template')

urlpatterns = [
    path('', include(router.urls)),
]
