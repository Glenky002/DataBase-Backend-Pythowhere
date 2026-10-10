from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeAssessmentViewSet

router = DefaultRouter()
router.register(r'assessments', GradeAssessmentViewSet, basename='grade-assessment')

urlpatterns = [
    path('', include(router.urls)),
]