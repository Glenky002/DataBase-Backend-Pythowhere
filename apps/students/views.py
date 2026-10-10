# # from rest_framework import viewsets, status,serializers
# # from rest_framework.response import Response
# # from apps.users.permissions import IsTeacherOrAdmin
# # from .models import StudentClass, Student
# # from .serializers import StudentClassSerializer, StudentSerializer


# # class StudentClassViewSet(viewsets.ModelViewSet):
# #     serializer_class = StudentClassSerializer
# #     permission_classes = [IsTeacherOrAdmin]

# #     def get_queryset(self):
# #         user = self.request.user
# #         if not hasattr(user, 'teacher_profile'):
# #             return StudentClass.objects.none()
        
# #         # Isolation: hanya tampilkan kelas milik sekolah user login
# #         return StudentClass.objects.filter(school=user.teacher_profile.school)

# #     def perform_create(self, serializer):
# #         user = self.request.user
# #         if hasattr(user, 'teacher_profile'):
# #             school = user.teacher_profile.school
# #         elif hasattr(user, 'school'):  # Jika admin langsung terhubung ke School
# #             school = user.school
# #         else:
# #             raise serializers.ValidationError({"error": "User tidak memiliki profil sekolah terikat."})
        
# #         serializer.save(school=school)


# # class StudentViewSet(viewsets.ModelViewSet):
# #     serializer_class = StudentSerializer
# #     permission_classes = [IsTeacherOrAdmin]

# #     def get_queryset(self):
# #         user = self.request.user
# #         if not hasattr(user, 'teacher_profile'):
# #             return Student.objects.none()

# #         # Isolation: hanya tampilkan siswa milik sekolah user login
# #         queryset = Student.objects.filter(school=user.teacher_profile.school)
        
# #         # Filter optional via Query Params (contoh: /api/v1/students/?class_id=1)
# #         class_id = self.request.query_params.get('class_id')
# #         status_param = self.request.query_params.get('status')

# #         if class_id:
# #             queryset = queryset.filter(student_class_id=class_id)
# #         if status_param:
# #             queryset = queryset.filter(status=status_param)

# #         return queryset

# #     def perform_create(self, serializer):
# #         # Otomatis tempelkan sekolah dari user yang sedang login
# #         school = self.request.user.teacher_profile.school
# #         serializer.save(school=school)



# # # from rest_framework import viewsets
# # # from apps.users.permissions import IsSchoolAdmin, IsTeacherOrAdmin
# # # from .models import StudentClass, Student
# # # from .serializers import StudentClassSerializer, StudentSerializer


# # # class StudentClassViewSet(viewsets.ModelViewSet):
# # #     serializer_class = StudentClassSerializer

# # #     def get_permissions(self):
# # #         # Hanya ADMIN yang boleh membuat/mengedit/menghapus kelas
# # #         if self.action in ['create', 'update', 'partial_update', 'destroy']:
# # #             return [IsSchoolAdmin()]
# # #         return [IsTeacherOrAdmin()]

# # #     def get_queryset(self):
# # #         user = self.request.user
# # #         if hasattr(user, 'teacher_profile'):
# # #             return StudentClass.objects.filter(school=user.teacher_profile.school)
# # #         return StudentClass.objects.none()


# # # class StudentViewSet(viewsets.ModelViewSet):
# # #     serializer_class = StudentSerializer

# # #     def get_permissions(self):
# # #         # Hanya ADMIN yang boleh membuat/mengedit/menghapus data siswa
# # #         if self.action in ['create', 'update', 'partial_update', 'destroy']:
# # #             return [IsSchoolAdmin()]
# # #         return [IsTeacherOrAdmin()]

# # #     def get_queryset(self):
# # #         user = self.request.user
# # #         if not hasattr(user, 'teacher_profile'):
# # #             return Student.objects.none()

# # #         queryset = Student.objects.filter(school=user.teacher_profile.school)
# # #         class_id = self.request.query_params.get('class_id')
# # #         if class_id:
# # #             queryset = queryset.filter(student_class_id=class_id)
# # #         return queryset


# # # from rest_framework import viewsets, permissions
# # # from .models import StudentClass, Student
# # # from .serializers import StudentClassSerializer, StudentSerializer


# # # class StudentClassViewSet(viewsets.ModelViewSet):
# # #     serializer_class = StudentClassSerializer
# # #     permission_classes = [permissions.IsAuthenticated]  # Ubah ke IsAuthenticated nanti saat JWT aktif

# # #     def get_queryset(self):
# # #         user = self.request.user
# # #         if user.is_authenticated and hasattr(user, 'teacher_profile'):
# # #             return StudentClass.objects.filter(school=user.teacher_profile.school)
# # #         return StudentClass.objects.all()


# # # class StudentViewSet(viewsets.ModelViewSet):
# # #     serializer_class = StudentSerializer
# # #     permission_classes = [permissions.IsAuthenticated]

# # #     def get_queryset(self):
# # #         queryset = Student.objects.all()
# # #         user = self.request.user
        
# # #         # Isolasi berdasarkan sekolah
# # #         if user.is_authenticated and hasattr(user, 'teacher_profile'):
# # #             queryset = queryset.filter(school=user.teacher_profile.school)

# # #         # Filter opsional berdasarkan kelas
# # #         class_id = self.request.query_params.get('class_id')
# # #         if class_id:
# # #             queryset = queryset.filter(student_class_id=class_id)

# # #         return queryset

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from apps.users.permissions import IsTeacherOrAdmin
from .models import StudentClass, Student
from .serializers import StudentClassSerializer, StudentSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q 
from rest_framework.decorators import action
from django.db import transaction


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StudentClassViewSet(viewsets.ModelViewSet):
    serializer_class = StudentClassSerializer
    pagination_class = StandardResultsSetPagination  # Aktifkan Pagination Backend
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher_profile'):
            return StudentClass.objects.filter(school=user.teacher_profile.school)
        elif hasattr(user, 'school'):
            return StudentClass.objects.filter(school=user.school)
        return StudentClass.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'teacher_profile'):
            school = user.teacher_profile.school
        elif hasattr(user, 'school'):
            school = user.school
        else:
            raise serializers.ValidationError({"error": "User tidak memiliki profil sekolah terikat."})
        
        serializer.save(school=school)


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination  # Aktifkan Pagination agar terstruktur (count & results)
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher_profile'):
            school = user.teacher_profile.school
        elif hasattr(user, 'school'):
            school = user.school
        else:
            return Student.objects.none()

        queryset = Student.objects.filter(school=school).order_by('-id')

        class_id = self.request.query_params.get('class_id') or self.request.query_params.get('student_class')
        status_param = self.request.query_params.get('status')
        search_query = self.request.query_params.get('search')

        # Filter Kelas
        if class_id:
            queryset = queryset.filter(student_class_id=class_id)
            
        # Filter Status
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        # Filter Search Nama / NISN / NIS
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) | 
                Q(nisn__icontains=search_query) |
                Q(nis__icontains=search_query)
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school
        if not school:
            raise serializers.ValidationError({"error": "User tidak memiliki profil sekolah terikat."})

        serializer.save(school=school)

    # 1. BULK CREATE (IMPORT EXCEL)
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create_students(self, request):
        students_data = request.data.get('students', [])
        if not students_data or not isinstance(students_data, list):
            return Response(
                {"error": "Format data siswa tidak valid. Kirimkan array siswa."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school

        created_count = 0
        errors = []

        with transaction.atomic():
            for idx, item in enumerate(students_data, 1):
                serializer = self.get_serializer(data=item)
                if serializer.is_valid():
                    serializer.save(school=school)
                    created_count += 1
                else:
                    errors.append({"row": idx, "errors": serializer.errors})

        if errors and created_count == 0:
            return Response(
                {"error": "Gagal mengimpor seluruh data.", "details": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": f"Berhasil mengimpor {created_count} siswa.",
                "failed_count": len(errors),
                "errors": errors
            },
            status=status.HTTP_201_CREATED
        )

    # 2. BULK DELETE
    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids or not isinstance(ids, list):
            return Response(
                {"error": "Daftar ID siswa wajib dikirim dalam bentuk array/list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school
        
        # Isolasi Tenant: Hanya hapus siswa yang terikat ke sekolah pengguna login
        deleted_count, _ = Student.objects.filter(id__in=ids, school=school).delete()

        return Response(
            {"message": f"Berhasil menghapus {deleted_count} data siswa."},
            status=status.HTTP_200_OK
        )

    # 3. BULK UPDATE CLASS (ATUR KELAS MASSAL)
    @action(detail=False, methods=['post'], url_path='bulk-update-class')
    def bulk_update_class(self, request):
        student_ids = request.data.get('student_ids', [])
        class_id = request.data.get('class_id')

        if not student_ids or not isinstance(student_ids, list) or not class_id:
            return Response(
                {"error": "student_ids (array) dan class_id wajib diisi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school

        # Validasi bahwa kelas tujuan memang milik sekolah yang sama
        if not StudentClass.objects.filter(id=class_id, school=school).exists():
            return Response(
                {"error": "Kelas tujuan tidak ditemukan atau tidak sesuai dengan sekolah Anda."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update massal terisolasi tenant
        updated_count = Student.objects.filter(
            id__in=student_ids,
            school=school
        ).update(student_class_id=class_id)

        return Response(
            {"message": f"Berhasil memperbarui kelas untuk {updated_count} siswa."},
            status=status.HTTP_200_OK
        )










# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class StudentClassViewSet(viewsets.ModelViewSet):
#     serializer_class = StudentClassSerializer
#     pagination_class = StandardResultsSetPagination  # <-- Aktifkan Pagination Backend
#     permission_classes = [IsTeacherOrAdmin]

#     def get_queryset(self):
#         user = self.request.user
#         # Isolasi Data: Hanya kembalikan kelas milik sekolah user login
#         if hasattr(user, 'teacher_profile'):
#             return StudentClass.objects.filter(school=user.teacher_profile.school)
#         elif hasattr(user, 'school'):
#             return StudentClass.objects.filter(school=user.school)
#         return StudentClass.objects.none()

#     def perform_create(self, serializer):
#         user = self.request.user
#         if hasattr(user, 'teacher_profile'):
#             school = user.teacher_profile.school
#         elif hasattr(user, 'school'):
#             school = user.school
#         else:
#             raise serializers.ValidationError({"error": "User tidak memiliki profil sekolah terikat."})
        
#         serializer.save(school=school)


# class StudentViewSet(viewsets.ModelViewSet):
#     serializer_class = StudentSerializer
#     permission_classes = [IsTeacherOrAdmin]

#     def get_queryset(self):
#         user = self.request.user
#         if hasattr(user, 'teacher_profile'):
#             school = user.teacher_profile.school
#         elif hasattr(user, 'school'):
#             school = user.school
#         else:
#             return Student.objects.none()

#         queryset = Student.objects.filter(school=school).order_by('-id')

#         class_id = self.request.query_params.get('class_id') or self.request.query_params.get('student_class')
#         status_param = self.request.query_params.get('status')
#         search_query = self.request.query_params.get('search')

#         # Filter Kelas
#         if class_id:
#             queryset = queryset.filter(student_class_id=class_id)
            
#         # Filter Status
#         if status_param:
#             queryset = queryset.filter(status=status_param)
            
#         # Filter Search Nama / NISN (Menggunakan Q Object)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(full_name__icontains=search_query) | Q(nisn__icontains=search_query)
#             )

#         return queryset

#     def perform_create(self, serializer):
#         user = self.request.user
#         if hasattr(user, 'teacher_profile'):
#             school = user.teacher_profile.school
#         elif hasattr(user, 'school'):
#             school = user.school
#         else:
#             raise serializers.ValidationError({"error": "User tidak memiliki profil sekolah terikat."})

#         serializer.save(school=school)

#     @action(detail=False, methods=['post'], url_path='bulk-create')
#     def bulk_create_students(self, request):
#         students_data = request.data.get('students', [])
#         if not students_data or not isinstance(students_data, list):
#             return Response(
#                 {"error": "Format data siswa tidak valid. Kirimkan array siswa."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = request.user
#         school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school

#         created_count = 0
#         errors = []

#         for idx, item in enumerate(students_data, 1):
#             serializer = self.get_serializer(data=item)
#             if serializer.is_valid():
#                 serializer.save(school=school)
#                 created_count += 1
#             else:
#                 errors.append({"row": idx, "errors": serializer.errors})

#         if errors and created_count == 0:
#             return Response(
#                 {"error": "Gagal mengimpor seluruh data.", "details": errors},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return Response(
#             {
#                 "message": f"Berhasil mengimpor {created_count} siswa.",
#                 "failed_count": len(errors),
#                 "errors": errors
#             },
#             status=status.HTTP_201_CREATED
#         )
    
#     # ACTION BARU: BULK DELETE
#     @action(detail=False, methods=['post'], url_path='bulk-delete')
#     def bulk_delete(self, request):
#         ids = request.data.get('ids', [])
#         if not ids or not isinstance(ids, list):
#             return Response(
#                 {"error": "Daftar ID siswa wajib dikirim dalam bentuk array/list."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = request.user
#         school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else user.school
        
#         # Hapus siswa yang sesuai ID dan terikat ke sekolah user login
#         deleted_count, _ = Student.objects.filter(id__in=ids, school=school).delete()

#         return Response(
#             {"message": f"Berhasil menghapus {deleted_count} data siswa."},
#             status=status.HTTP_200_OK
#         )

# from rest_framework import viewsets, status, serializers
# from rest_framework.pagination import PageNumberPagination
# from django.db.models import Q  # <-- Import Q untuk pencarian fleksibel
# from apps.users.permissions import IsTeacherOrAdmin
# from .models import Student
# from .serializers import StudentSerializer

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class StudentViewSet(viewsets.ModelViewSet):
#     serializer_class = StudentSerializer
#     permission_classes = [IsTeacherOrAdmin]
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         user = self.request.user
#         if hasattr(user, 'teacher_profile'):
#             school = user.teacher_profile.school
#         elif hasattr(user, 'school'):
#             school = user.school
#         else:
#             return Student.objects.none()

#         queryset = Student.objects.filter(school=school).order_by('-id')

#         class_id = self.request.query_params.get('class_id') or self.request.query_params.get('student_class')
#         status_param = self.request.query_params.get('status')
#         search_query = self.request.query_params.get('search')

#         # Filter Kelas
#         if class_id:
#             queryset = queryset.filter(student_class_id=class_id)
            
#         # Filter Status
#         if status_param:
#             queryset = queryset.filter(status=status_param)
            
#         # Filter Search Nama / NISN (Menggunakan Q Object)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(full_name__icontains=search_query) | Q(nisn__icontains=search_query)
#             )

#         return queryset