from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.schools.serializers import SchoolSerializer
from .serializers import RegisterSchoolSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class RegisterSchoolView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSchoolSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                {
                    "message": "Pendaftaran sekolah dan akun admin berhasil!",
                    "school": SchoolSerializer(result['school']).data,
                    "admin_username": result['user'].username
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer