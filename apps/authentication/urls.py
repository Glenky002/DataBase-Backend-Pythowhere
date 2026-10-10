from django.urls import path
from .views import RegisterSchoolView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterSchoolView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterSchoolView.as_view(), name='register-school'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]