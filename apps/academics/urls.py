from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, SubjectPassingGradeViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'passing-grades', SubjectPassingGradeViewSet, basename='passing-grade')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]