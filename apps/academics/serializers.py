# from rest_framework import serializers
# from .models import Schedule, Subject

# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = ['id', 'name', 'code']


# class ScheduleSerializer(serializers.ModelSerializer):
#     subject_name = serializers.ReadOnlyField(source='subject.name')
#     teacher_name = serializers.SerializerMethodField()
#     time_slot = serializers.SerializerMethodField()

#     class Meta:
#         model = Schedule
#         fields = [
#             'id', 
#             'student_class', 
#             'subject', 
#             'subject_name', 
#             'teacher', 
#             'teacher_name', 
#             'day', 
#             'start_time', 
#             'end_time', 
#             'time_slot'
#         ]

#     def get_teacher_name(self, obj):
#         if obj.teacher:
#             if hasattr(obj.teacher, 'full_name') and obj.teacher.full_name:
#                 return obj.teacher.full_name
#             if hasattr(obj.teacher, 'user'):
#                 return f"{obj.teacher.user.first_name} {obj.teacher.user.last_name}".strip()
#         return "Belum diatur"

#     def get_time_slot(self, obj):
#         return f"{obj.start_time.strftime('%H.%M')} - {obj.end_time.strftime('%H.%M')}"







from rest_framework import serializers
from .models import Subject, SubjectPassingGrade, Schedule
from apps.users.models import TeacherProfile

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']

class SubjectPassingGradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='student_class.name', read_only=True)

    class Meta:
        model = SubjectPassingGrade
        fields = ['id', 'subject', 'subject_name', 'student_class', 'class_name', 'kkm']

class ScheduleSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='student_class.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'student_class', 'class_name', 
            'subject', 'subject_name', 'teacher', 
            'teacher_name', 'day', 'start_time', 'end_time'
        ]

    def get_teacher_name(self, obj):
        if obj.teacher and obj.teacher.user:
            full_name = obj.teacher.user.get_full_name()
            return full_name if full_name.strip() else obj.teacher.user.username
        return '-'