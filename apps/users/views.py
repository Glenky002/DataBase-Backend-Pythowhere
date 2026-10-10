# # # # # # from rest_framework import viewsets, status
# # # # # # from rest_framework.response import Response
# # # # # # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # # # # # from .models import TeacherProfile
# # # # # # from .serializers import TeacherProfileSerializer, CreateTeacherSerializer


# # # # # # class TeacherProfileViewSet(viewsets.ModelViewSet):
# # # # # #     """
# # # # # #     ViewSet untuk Manajemen Guru & Staf Sekolah.
# # # # # #     - Multi-Tenant Isolation: Mengisolasi data guru per sekolah.
# # # # # #     - RBAC: Hanya Admin Sekolah yang boleh membuat/menghapus guru.
# # # # # #     """
# # # # # #     permission_classes = [IsTeacherOrAdmin]

# # # # # #     def get_serializer_class(self):
# # # # # #         # Saat POST (buat guru baru), gunakan CreateTeacherSerializer
# # # # # #         if self.action == 'create':
# # # # # #             return CreateTeacherSerializer
# # # # # #         # Saat GET/PUT/PATCH, gunakan TeacherProfileSerializer biasa
# # # # # #         return TeacherProfileSerializer

# # # # # #     def get_permissions(self):
# # # # # #         # Hanya ADMIN Sekolah yang boleh mendaftarkan (POST) atau menghapus (DELETE) akun guru
# # # # # #         if self.action in ['create', 'destroy']:
# # # # # #             return [IsSchoolAdmin()]
# # # # # #         # Untuk GET/LIST/RETRIEVE/UPDATE boleh ADMIN, TEACHER, atau STAFF
# # # # # #         return [IsTeacherOrAdmin()]

# # # # # #     def get_queryset(self):
# # # # # #         user = self.request.user
        
# # # # # #         # Superuser Django Admin bisa melihat seluruh guru di semua sekolah
# # # # # #         if user.is_superuser:
# # # # # #             return TeacherProfile.objects.all()

# # # # # #         # Multi-Tenant Isolation untuk Admin/Guru Sekolah
# # # # # #         if hasattr(user, 'teacher_profile'):
# # # # # #             return TeacherProfile.objects.filter(
# # # # # #                 school=user.teacher_profile.school
# # # # # #             )

# # # # # #         return TeacherProfile.objects.none()

# # # # # #     def create(self, request, *args, **kwargs):
# # # # # #         serializer = CreateTeacherSerializer(data=request.data, context={'request': request})
# # # # # #         serializer.is_valid(raise_exception=True)
# # # # # #         profile = serializer.save()
# # # # # #         output_serializer = TeacherProfileSerializer(profile)
# # # # # #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)




# # # # # from rest_framework import viewsets, status
# # # # # from rest_framework.response import Response
# # # # # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # # # # from .models import TeacherProfile
# # # # # from .serializers import TeacherProfileSerializer, CreateTeacherSerializer


# # # # # class TeacherProfileViewSet(viewsets.ModelViewSet):
# # # # #     """
# # # # #     ViewSet untuk Manajemen Guru & Staf Sekolah.
# # # # #     - Multi-Tenant Isolation: Mengisolasi data guru per sekolah.
# # # # #     - RBAC: Hanya Admin Sekolah yang boleh membuat/menghapus guru.
# # # # #     - Staff / Teacher / Admin memiliki akses baca/update sesuai haknya.
# # # # #     """

# # # # #     def get_serializer_class(self):
# # # # #         # Saat POST (buat guru baru), gunakan CreateTeacherSerializer
# # # # #         if self.action == 'create':
# # # # #             return CreateTeacherSerializer
# # # # #         # Saat GET/PUT/PATCH, gunakan TeacherProfileSerializer biasa
# # # # #         return TeacherProfileSerializer

# # # # #     def get_permissions(self):
# # # # #         # Hanya ADMIN Sekolah yang boleh mendaftarkan (POST) atau menghapus (DELETE) akun guru
# # # # #         if self.action in ['create', 'destroy']:
# # # # #             return [IsSchoolAdmin()]
# # # # #         # Untuk GET/LIST/RETRIEVE/UPDATE boleh ADMIN, TEACHER, atau STAFF
# # # # #         return [IsTeacherOrAdmin()]

# # # # #     def get_queryset(self):
# # # # #         user = self.request.user
        
# # # # #         if user.is_superuser:
# # # # #             return TeacherProfile.objects.all()

# # # # #         # Admin, Teacher, dan Staff bisa melihat daftar guru di sekolahnya
# # # # #         if hasattr(user, 'teacher_profile'):
# # # # #             return TeacherProfile.objects.filter(
# # # # #                 school=user.teacher_profile.school
# # # # #             )

# # # # #         return TeacherProfile.objects.none()

# # # # #     def create(self, request, *args, **kwargs):
# # # # #         # Gunakan self.get_serializer agar context={'request': request} otomatis terbawa
# # # # #         serializer = self.get_serializer(data=request.data)
# # # # #         serializer.is_valid(raise_exception=True)
# # # # #         profile = serializer.save()
        
# # # # #         output_serializer = TeacherProfileSerializer(profile, context={'request': request})
# # # # #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)


# # # # from rest_framework import viewsets, status
# # # # from rest_framework.response import Response
# # # # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # # # from .models import TeacherProfile
# # # # from .serializers import TeacherProfileSerializer, CreateTeacherSerializer


# # # # class TeacherProfileViewSet(viewsets.ModelViewSet):
# # # #     """
# # # #     ViewSet untuk Manajemen Guru & Staf Sekolah.
# # # #     - Multi-Tenant Isolation: Mengisolasi data guru per sekolah.
# # # #     - RBAC: Hanya Admin Sekolah yang boleh membuat/menghapus guru.
# # # #     """

# # # #     def get_serializer_class(self):
# # # #         if self.action == 'create':
# # # #             return CreateTeacherSerializer
# # # #         return TeacherProfileSerializer

# # # #     def get_permissions(self):
# # # #         # Hanya ADMIN Sekolah yang boleh mendaftarkan (POST) atau menghapus (DELETE)
# # # #         if self.action in ['create', 'destroy']:
# # # #             return [IsSchoolAdmin()]
# # # #         # Untuk GET/LIST/RETRIEVE/UPDATE diizinkan ADMIN, TEACHER, atau STAFF
# # # #         return [IsTeacherOrAdmin()]

# # # #     def get_queryset(self):
# # # #         user = self.request.user
        
# # # #         # Superuser Django Admin melihat seluruh sekolah
# # # #         if user.is_superuser:
# # # #             return TeacherProfile.objects.all()

# # # #         # Multi-Tenant Isolation per Sekolah
# # # #         if hasattr(user, 'teacher_profile'):
# # # #             return TeacherProfile.objects.filter(
# # # #                 school=user.teacher_profile.school
# # # #             )

# # # #         return TeacherProfile.objects.none()

# # # #     def create(self, request, *args, **kwargs):
# # # #         serializer = self.get_serializer(data=request.data)
# # # #         serializer.is_valid(raise_exception=True)
# # # #         profile = serializer.save()
        
# # # #         output_serializer = TeacherProfileSerializer(profile, context={'request': request})
# # # #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)



# # # from rest_framework import viewsets, status
# # # from rest_framework.response import Response
# # # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # # from .models import TeacherProfile
# # # from .serializers import TeacherProfileSerializer, CreateTeacherSerializer

# # # class TeacherProfileViewSet(viewsets.ModelViewSet):
# # #     def get_serializer_class(self):
# # #         if self.action == 'create':
# # #             return CreateTeacherSerializer
# # #         return TeacherProfileSerializer

# # #     def get_permissions(self):
# # #         if self.action in ['create', 'destroy']:
# # #             return [IsSchoolAdmin()]
# # #         return [IsTeacherOrAdmin()]

# # #     def get_queryset(self):
# # #         user = self.request.user
# # #         if user.is_superuser or user.is_staff:
# # #             return TeacherProfile.objects.all()

# # #         if hasattr(user, 'teacher_profile'):
# # #             return TeacherProfile.objects.filter(
# # #                 school=user.teacher_profile.school
# # #             )

# # #         return TeacherProfile.objects.none()

# # #     def create(self, request, *args, **kwargs):
# # #         serializer = self.get_serializer(data=request.data)
# # #         serializer.is_valid(raise_exception=True)
# # #         profile = serializer.save()
        
# # #         output_serializer = TeacherProfileSerializer(profile, context={'request': request})
# # #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)






# # from rest_framework import viewsets, status
# # from rest_framework.response import Response
# # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # from .models import TeacherProfile
# # from .serializers import TeacherProfileSerializer, CreateTeacherSerializer


# # class TeacherProfileViewSet(viewsets.ModelViewSet):
# #     """
# #     ViewSet untuk Manajemen Guru & Staf Sekolah.
# #     - Multi-Tenant Isolation: Mengisolasi data guru per sekolah.
# #     - RBAC: Hanya Admin Sekolah yang boleh CREATE, UPDATE, DELETE.
# #     - Staff / Teacher: Hanya boleh READ (List & Detail).
# #     """

# #     def get_serializer_class(self):
# #         if self.action == 'create':
# #             return CreateTeacherSerializer
# #         return TeacherProfileSerializer

# #     def get_permissions(self):
# #         # Hanya ADMIN yang diizinkan untuk membuat, mengedit, atau menghapus
# #         if self.action in ['create', 'update', 'partial_update', 'destroy']:
# #             return [IsSchoolAdmin()]
# #         # READ (list & retrieve) diizinkan untuk semua peran sekolah yang terautentikasi
# #         return [IsTeacherOrAdmin()]

# #     def get_queryset(self):
# #         user = self.request.user
        
# #         # Superuser atau Django Staff selalu bisa melihat & mengelola semua data
# #         if user.is_superuser or user.is_staff:
# #             return TeacherProfile.objects.all()

# #         # Admin Sekolah (Berdasarkan Profil Sekolah)
# #         if hasattr(user, 'teacher_profile') and user.teacher_profile.school:
# #             return TeacherProfile.objects.filter(school=user.teacher_profile.school)

# #         # Jika user biasa belum punya profil
# #         return TeacherProfile.objects.none()

# #     def create(self, request, *args, **kwargs):
# #         serializer = self.get_serializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         profile = serializer.save()
        
# #         output_serializer = TeacherProfileSerializer(profile, context={'request': request})
# #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)












# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import TeacherProfile
# from .serializers import TeacherProfileSerializer
# from .permissions import IsTeacherOrAdmin

# class TeacherProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = TeacherProfileSerializer
#     permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser or user.is_staff:
#             return TeacherProfile.objects.all()
        
#         profile = getattr(user, 'teacher_profile', None)
#         if profile and profile.school:
#             return TeacherProfile.objects.filter(school=profile.school)
#         return TeacherProfile.objects.none()

#     def partial_update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         data = request.data.copy()

#         # FIX PROBLEM 2: Jika target akun adalah ADMIN, larang perubahan role!
#         if instance.role == 'ADMIN' and 'role' in data and data['role'] != 'ADMIN':
#             return Response(
#                 {"detail": "Role ADMIN terkunci dan tidak dapat diubah menjadi TEACHER/STAFF."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)








from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TeacherProfile
from .serializers import (
    TeacherProfileSerializer, 
    CreateTeacherSerializer
)
from .permissions import IsTeacherOrAdmin


class TeacherProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTeacherSerializer
        return TeacherProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return TeacherProfile.objects.all()

        profile = getattr(user, 'teacher_profile', None)
        if profile and profile.school:
            return TeacherProfile.objects.filter(school=profile.school)
        return TeacherProfile.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile_instance = serializer.save()
        
        # Kembalikan format data lengkap dari TeacherProfileSerializer
        read_serializer = TeacherProfileSerializer(profile_instance, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Proteksi: Hapus field role dari payload jika nilainya kosong/null agar tidak memicu error validasi
        if 'role' in data and not data['role']:
            data.pop('role')

        # Proteksi Kunci Role Admin: Cegah akun ADMIN diubah ke TEACHER/STAFF
        if instance.role == 'ADMIN' and data.get('role') and data.get('role') != 'ADMIN':
            return Response(
                {"detail": "Role ADMIN terikat dan tidak dapat diubah."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        target_user = instance.user

        # 1. CEGAH ADMIN MENGHAPUS AKUN SENDIRI (Self-Deletion Protection)
        if target_user and target_user.id == request.user.id:
            return Response(
                {"detail": "Anda tidak dapat menghapus akun Anda sendiri!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. HAPUS TOTAL AKUN USER (Bukan cuma detach TeacherProfile)
        if target_user:
            # Menghapus User Django secara otomatis menghapus TeacherProfile via CASCADE
            target_user.delete()
        else:
            instance.delete()

        return Response(
            {"detail": "Akun berhasil dihapus secara total dari sistem."}, 
            status=status.HTTP_204_NO_CONTENT
        )