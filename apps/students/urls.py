from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentClassViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'classes', StudentClassViewSet, basename='student-class')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]