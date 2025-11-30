from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', include('apps.users.urls')),
    path('api/agents/', include('apps.agents.urls')),
    path('api/workflows/', include('apps.workflows.urls')),
    path('api/projects/', include('apps.projects.urls')),
]

# Serve frontend for non-admin, non-api routes
# This must be at the end but should NOT catch admin or api routes
urlpatterns += [
    re_path(r'^(?!admin|api|static).*$', TemplateView.as_view(template_name='index.html'), name='frontend'),
]
