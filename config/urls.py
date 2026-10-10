# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # Endpoint API v1 untuk modul Schools
#     path('api/v1/auth/', include('apps.authentication.urls')),
#     path('api/v1/', include('apps.schools.urls')),
#     path('api/v1/', include('apps.users.urls')),
#     path('api/v1/', include('apps.students.urls')),
#     path('api/v1/', include('apps.attendance.urls')),
#     path('api/v1/', include('apps.grades.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Schema OpenAPI JSON/YAML
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Dokumentasi UI Interactive (Swagger UI & Redoc)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Local Apps API Routes
    path('admin/', admin.site.urls),
    # Endpoint API v1 untuk modul Schools
    # path('api/v1/auth/', include('apps.authentication.urls')),
    # path('api/v1/', include('apps.schools.urls')),
    # path('api/v1/', include('apps.users.urls')),
    # path('api/v1/', include('apps.students.urls')),
    # path('api/v1/', include('apps.attendance.urls')),
    # path('api/v1/', include('apps.grades.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/schools/', include('apps.schools.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/students/', include('apps.students.urls')),
    path('api/v1/attendance/', include('apps.attendance.urls')),
    path('api/v1/grades/', include('apps.grades.urls')),
    path('api/v1/academics/', include('apps.academics.urls')),
]