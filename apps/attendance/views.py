from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
# from django.db.models import Count, Q
from django.db import transaction
from apps.users.permissions import IsTeacherOrAdmin
from apps.students.models import StudentClass, Student
from .models import Attendance
from .serializers import AttendanceSerializer, ClassAttendanceSummarySerializer,BulkAttendanceSerializer
from django.utils import timezone
from django.db.models import Count
import calendar
from datetime import datetime

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'teacher_profile'):
            return Attendance.objects.none()

        queryset = Attendance.objects.filter(school=user.teacher_profile.school)
        date = self.request.query_params.get('date')
        class_id = self.request.query_params.get('class_id')

        if date:
            queryset = queryset.filter(date=date)
        if class_id:
            queryset = queryset.filter(student_class_id=class_id)

        return queryset

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user

            # Cek keamanan jika user tidak punya teacher_profile
            if not hasattr(user, 'teacher_profile'):
                return Response(
                    {"error": "User tidak terdaftar sebagai staf/guru sekolah."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # 🔒 Validasi Penguncian Tanggal (Max 3 hari lalu kecuali Superuser)
            target_date = data['date']
            if (timezone.now().date() - target_date).days > 3 and not user.is_superuser:
                return Response(
                    {"error": "Absensi pada tanggal ini sudah dikunci (lebih dari 3 hari yang lalu). Hubungi Administrator."},
                    status=status.HTTP_403_FORBIDDEN
                )

            school = user.teacher_profile.school

            created_records = []
            with transaction.atomic():
                for item in data['attendances']:
                    attendance, _ = Attendance.objects.update_or_create(
                        school=school,
                        student_id=item['student_id'],
                        date=data['date'],
                        defaults={
                            'student_class_id': data['class_id'],
                            'recorded_by': user.teacher_profile,
                            'status': item['status'],
                            'notes': item.get('notes', '')
                        }
                    )
                    created_records.append(attendance)

            return Response(
                {"message": f"Berhasil mencatat absensi untuk {len(created_records)} siswa."},
                status=status.HTTP_201_CREATED
            )

        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        class_id = request.query_params.get('class_id')
        month = request.query_params.get('month')
        year = request.query_params.get('year', 2026)

        if not class_id or not month:
            return Response(
                {"error": "Query parameter 'class_id' dan 'month' wajib diisi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        school = request.user.teacher_profile.school

        try:
            student_class = StudentClass.objects.get(id=class_id, school=school)
        except StudentClass.DoesNotExist:
            return Response(
                {"error": "Kelas tidak ditemukan atau bukan milik sekolah Anda."},
                status=status.HTTP_404_NOT_FOUND
            )

        students = Student.objects.filter(student_class=student_class, school=school)

        students_summary = []
        for student in students:
            records = Attendance.objects.filter(
                student=student,
                school=school,
                date__month=month,
                date__year=year
            )

            total_days = records.count()
            
            # KONSISTENSI STATUS DENGAN MODEL & FRONTEND:
            hadir = records.filter(status='PRESENT').count()
            sakit = records.filter(status='SICK').count()
            izin = records.filter(status='PERMIT').count()
            alpa = records.filter(status='ABSENT').count()

            percentage = round((hadir / total_days) * 100, 2) if total_days > 0 else 0.0

            students_summary.append({
                "student_id": student.id,
                "student_name": student.full_name or f"{student.first_name} {student.last_name}",
                "nisn": student.nisn,
                "total_days": total_days,
                "hadir": hadir,
                "sakit": sakit,
                "izin": izin,
                "alpa": alpa,
                "attendance_percentage": percentage,
                "parent_phone_number": student.parent_phone_number,
            })

        data = {
            "class_id": student_class.id,
            "class_name": student_class.name,
            "month": int(month),
            "year": int(year),
            "students_summary": students_summary
        }

        serializer = ClassAttendanceSummarySerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['get'], url_path=r'students/(?P<student_id>\d+)/summary')
    # def student_summary(self, request, student_id=None):
    #     user = request.user
    #     school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else getattr(user, 'school', None)

    #     if not school:
    #         return Response({"error": "Profil sekolah tidak ditemukan."}, status=status.HTTP_400_BAD_REQUEST)

    #     # Ambil log absensi 1 siswa
    #     logs = Attendance.objects.filter(
    #         student_id=student_id,
    #         school=school
    #     ).order_by('-date')

    #     # Hitung berdasarkan STATUS MODEL KAMU ('PRESENT', 'SICK', 'PERMIT', 'ABSENT')
    #     hadir = logs.filter(status='PRESENT').count()
    #     sakit = logs.filter(status='SICK').count()
    #     izin = logs.filter(status='PERMIT').count()
    #     alpa = logs.filter(status='ABSENT').count()

    #     STATUS_MAP = {
    #         'PRESENT': 'HADIR',
    #         'PERMIT': 'IZIN',
    #         'SICK': 'SAKIT',
    #         'ABSENT': 'ALPA'
    #     }

    #     recent_logs = [
    #         {
    #             'date': log.date.strftime('%d %b %Y'),
    #             'status': STATUS_MAP.get(log.status, log.status),  # Mengembalikan 'HADIR', 'SAKIT', dll.
    #             'notes': getattr(log, 'notes', '') or ''
    #         }
    #         for log in logs[:10]
    #     ]

    #     return Response({
    #         'summary': STATUS_MAP,
    #         'recent_logs': recent_logs
    #     }, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], url_path='summary')
    def student_summary(self, request, pk=None):
        user = request.user
        school = user.teacher_profile.school if hasattr(user, 'teacher_profile') else getattr(user, 'school', None)

        if not school:
            return Response({"error": "Profil sekolah tidak ditemukan."}, status=status.HTTP_400_BAD_REQUEST)

        # 'pk' di sini otomatis diisi ID siswa dari URL (/attendances/{pk}/summary/)
        logs = Attendance.objects.filter(
            student_id=pk,
            school=school
        ).order_by('-date')

        hadir = logs.filter(status='PRESENT').count()
        izin  = logs.filter(status='PERMIT').count()
        sakit = logs.filter(status='SICK').count()
        alpa  = logs.filter(status='ABSENT').count()

        summary_dict = {
            'HADIR': hadir,
            'IZIN': izin,
            'SAKIT': sakit,
            'ALPA': alpa,
            'total': logs.count()
        }

        STATUS_MAP = {
            'PRESENT': 'HADIR',
            'PERMIT': 'IZIN',
            'SICK': 'SAKIT',
            'ABSENT': 'ALPA'
        }

        recent_logs = [
            {
                'date': log.date.strftime('%d %b %Y'),
                'status': STATUS_MAP.get(log.status, log.status),
                'notes': getattr(log, 'notes', '') or ''
            }
            for log in logs[:10]
        ]

        return Response({
            'summary': summary_dict,
            'recent_logs': recent_logs
        }, status=status.HTTP_200_OK)\


    @action(detail=False, methods=['get'], url_path='monitoring')
    def monitoring(self, request):
        user = request.user
        school = getattr(user, 'school', None) or getattr(user.teacher_profile, 'school', None)
        date = request.query_params.get('date')

        if not date:
            return Response({'error': 'Tanggal wajib diisi.'}, status=status.HTTP_400_BAD_REQUEST)

        classes = StudentClass.objects.filter(school=school)
        monitoring_result = []

        for cls in classes:
            total_students = cls.students.count()
            records = Attendance.objects.filter(school=school, student_class=cls, date=date)
            recorded_count = records.count()

            if recorded_count == 0:
                status_str = 'NOT_STARTED'
            elif recorded_count >= total_students and total_students > 0:
                status_str = 'COMPLETED'
            else:
                status_str = 'PARTIAL'

            # Penanganan Nama Guru dari model User
            teacher_name = None
            if cls.homeroom_teacher:
                teacher = cls.homeroom_teacher
                teacher_name = (
                    teacher.user.get_full_name() or 
                    teacher.user.username
                ) if teacher.user else f"Guru #{teacher.id}"

            monitoring_result.append({
                'class_id': cls.id,
                'class_name': cls.name,
                'homeroom_teacher': teacher_name,
                'total_students': total_students,
                'recorded_students': recorded_count,
                'status': status_str,
                'present_count': records.filter(status='PRESENT').count(),
                'permit_count': records.filter(status='PERMIT').count(),
                'sick_count': records.filter(status='SICK').count(),
                'absent_count': records.filter(status='ABSENT').count(),
            })

        return Response({'classes_monitoring': monitoring_result}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='matrix')
    def monthly_matrix(self, request):
        user = request.user
        school = getattr(user, 'school', None) or getattr(user.teacher_profile, 'school', None)
        
        class_id = request.query_params.get('class_id')
        month = int(request.query_params.get('month', datetime.now().month))
        year = int(request.query_params.get('year', datetime.now().year))

        if not class_id:
            return Response({'error': 'class_id wajib diisi.'}, status=status.HTTP_400_BAD_REQUEST)

        # Dapatkan jumlah hari dalam bulan tersebut (misal: 28, 30, atau 31 hari)
        _, num_days = calendar.monthrange(year, month)

        # Ambil seluruh siswa di kelas tersebut
        students = Student.objects.filter(school=school, student_class_id=class_id).order_by('full_name')

        # Ambil seluruh absensi bulan ini
        records = Attendance.objects.filter(
            school=school,
            student_class_id=class_id,
            date__year=year,
            date__month=month
        )

        matrix_result = []
        for student in students:
            daily_status = {}
            student_records = records.filter(student=student)
            
            hadir_count = 0
            sakit_count = 0
            izin_count = 0
            alpa_count = 0

            for day in range(1, num_days + 1):
                day_record = student_records.filter(date__day=day).first()
                if day_record:
                    status_code = day_record.status  # 'PRESENT', 'SICK', 'PERMIT', 'ABSENT'
                    
                    if status_code in ['PRESENT', 'H']:
                        daily_status[str(day)] = 'H'
                        hadir_count += 1
                    elif status_code in ['SICK', 'S']:
                        daily_status[str(day)] = 'S'
                        sakit_count += 1
                    elif status_code in ['PERMIT', 'I']:
                        daily_status[str(day)] = 'I'
                        izin_count += 1
                    elif status_code in ['ABSENT', 'A']:
                        daily_status[str(day)] = 'A'
                        alpa_count += 1
                else:
                    daily_status[str(day)] = '-'

            matrix_result.append({
                'student_id': student.id,
                'nisn': student.nisn,
                'full_name': student.full_name,
                'gender': student.gender,
                'daily': daily_status,
                'total_hadir': hadir_count,
                'total_sakit': sakit_count,
                'total_izin': izin_count,
                'total_alpa': alpa_count,
            })

        # --- SEKARANG DI LUAR LOOP FOR STUDENT ---
        student_class = StudentClass.objects.filter(school=school, id=class_id).first()
        teacher_name = "Belum Diatur"
        
        if student_class and student_class.homeroom_teacher:
            teacher = student_class.homeroom_teacher
            if hasattr(teacher, 'user') and teacher.user:
                teacher_name = teacher.user.get_full_name() or teacher.user.username
            else:
                teacher_name = getattr(teacher, 'full_name', f"Guru #{teacher.id}")

        return Response({
            'days_in_month': num_days,
            'homeroom_teacher': teacher_name,
            'matrix': matrix_result
        }, status=status.HTTP_200_OK)