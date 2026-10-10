from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherProfileViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherProfileViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]