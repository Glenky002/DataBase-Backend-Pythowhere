from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import GradeAssessment, StudentGrade
from .serializers import GradeAssessmentSerializer, BulkCreateGradeSerializer


class GradeAssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = GradeAssessmentSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Helper safe getter school_id
        school_id = getattr(user, 'school_id', None)
        if not school_id and hasattr(user, 'teacher_profile') and user.teacher_profile:
            school_id = user.teacher_profile.school_id

        queryset = GradeAssessment.objects.filter(school_id=school_id)
        
        class_id = self.request.query_params.get('class_id')
        subject_id = self.request.query_params.get('subject_id')
        
        if class_id:
            queryset = queryset.filter(student_class_id=class_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
            
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create_grades(self, request):
        serializer = BulkCreateGradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        school_id = getattr(user, 'school_id', None)
        if not school_id and hasattr(user, 'teacher_profile') and user.teacher_profile:
            school_id = user.teacher_profile.school_id

        if not school_id:
            return Response(
                {'error': 'User tidak terikat dengan sekolah mana pun.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # 1. Buat / Ambil Induk Penilaian
            assessment, created = GradeAssessment.objects.update_or_create(
                school_id=school_id,
                student_class_id=data['class_id'],
                subject_id=data['subject_id'],
                title=data['title'],
                defaults={
                    'category': data['category'],
                    'date': data['date'],
                    'teacher': getattr(user, 'teacher_profile', None)
                }
            )

            # 2. Input / Update Nilai Siswa
            for item in data['grades']:
                StudentGrade.objects.update_or_create(
                    assessment=assessment,
                    student_id=item['student_id'],
                    defaults={
                        'score': item['score'],
                        'notes': item.get('notes', '')
                    }
                )

        return Response({
            'message': 'Nilai berhasil disimpan!',
            'assessment_id': assessment.id
        }, status=status.HTTP_201_CREATED)