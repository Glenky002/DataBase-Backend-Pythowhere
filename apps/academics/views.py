# from rest_framework import viewsets, permissions
# from .models import Schedule,Subject
# from .serializers import ScheduleSerializer,SubjectSerializer

# class ScheduleViewSet(viewsets.ModelViewSet):
#     serializer_class = ScheduleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         school = getattr(user, 'school', None)
#         if not school and hasattr(user, 'teacher_profile'):
#             school = user.teacher_profile.school

#         queryset = Schedule.objects.filter(school=school)
        
#         class_id = self.request.query_params.get('class_id')
#         if class_id:
#             queryset = queryset.filter(student_class_id=class_id)

#         return queryset

#     def perform_create(self, serializer):
#         user = self.request.user
#         school = getattr(user, 'school', None) or getattr(user.teacher_profile, 'school', None)
#         serializer.save(school=school)

# class SubjectViewSet(viewsets.ModelViewSet):
#     serializer_class = SubjectSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         school = getattr(user, 'school', None) or getattr(user.teacher_profile, 'school', None)
#         return Subject.objects.filter(school=school)

#     def perform_create(self, serializer):
#         user = self.request.user
#         school = getattr(user, 'school', None) or getattr(user.teacher_profile, 'school', None)
#         serializer.save(school=school)


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Subject, SubjectPassingGrade, Schedule
from .serializers import SubjectSerializer, SubjectPassingGradeSerializer, ScheduleSerializer


def get_user_school_id(user):
    """Helper function terpusat untuk mengambil school_id dengan aman."""
    school_id = getattr(user, 'school_id', None)
    if not school_id and hasattr(user, 'teacher_profile') and user.teacher_profile:
        school_id = getattr(user.teacher_profile, 'school_id', None)
    return school_id


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = get_user_school_id(self.request.user)
        return Subject.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = get_user_school_id(self.request.user)
        serializer.save(school_id=school_id)


class SubjectPassingGradeViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectPassingGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = get_user_school_id(self.request.user)
        queryset = SubjectPassingGrade.objects.filter(school_id=school_id)
        
        student_class = self.request.query_params.get('student_class')
        subject = self.request.query_params.get('subject')

        if student_class:
            queryset = queryset.filter(student_class_id=student_class)
        if subject:
            queryset = queryset.filter(subject_id=subject)

        return queryset

    def create(self, request, *args, **kwargs):
        school_id = get_user_school_id(request.user)
        student_class_id = request.data.get('student_class')
        subject_id = request.data.get('subject')
        kkm_value = request.data.get('kkm', 75)

        obj, created = SubjectPassingGrade.objects.update_or_create(
            school_id=school_id,
            student_class_id=student_class_id,
            subject_id=subject_id,
            defaults={'kkm': kkm_value}
        )
        serializer = self.get_serializer(obj)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = get_user_school_id(self.request.user)
        queryset = Schedule.objects.filter(school_id=school_id)
        
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(student_class_id=class_id)

        return queryset

    def perform_create(self, serializer):
        school_id = get_user_school_id(self.request.user)
        serializer.save(school_id=school_id)