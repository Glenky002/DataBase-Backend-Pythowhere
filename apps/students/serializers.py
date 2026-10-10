# from rest_framework import serializers
# from .models import StudentClass, Student


# class StudentClassSerializer(serializers.ModelSerializer):
#     school_name = serializers.ReadOnlyField(source='school.name')
#     homeroom_teacher_name = serializers.ReadOnlyField(source='homeroom_teacher.user.get_full_name')
#     total_students = serializers.ReadOnlyField(source='students.count')

#     class Meta:
#         model = StudentClass
#         fields = [
#             'id', 
#             'school', 
#             'school_name', 
#             'homeroom_teacher', 
#             'homeroom_teacher_name', 
#             'name', 
#             'grade_level', 
#             'academic_year', 
#             'is_active', 
#             'total_students'
#         ]
#         read_only_fields = ['school']


# class StudentSerializer(serializers.ModelSerializer):
#     school_name = serializers.ReadOnlyField(source='school.name')
#     class_name = serializers.ReadOnlyField(source='student_class.name')

#     class Meta:
#         model = Student
#         fields = [
#             'id', 
#             'school', 
#             'school_name', 
#             'student_class', 
#             'class_name', 
#             'nisn', 
#             'nis', 
#             'full_name', 
#             'gender', 
#             'birth_place', 
#             'birth_date', 
#             'address', 
#             'parent_phone_number', 
#             'status', 
#             'created_at'
#         ]
#         read_only_fields = ['school', 'created_at']

from rest_framework import serializers
from apps.users.models import TeacherProfile
from .models import StudentClass, Student


class StudentClassSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    homeroom_teacher_name = serializers.ReadOnlyField(source='homeroom_teacher.user.get_full_name')
    total_students = serializers.ReadOnlyField(source='students.count')

    # Buat academic_year opsional (required=False)
    academic_year = serializers.CharField(required=False, allow_blank=True, default='2026/2027')

    class Meta:
        model = StudentClass
        fields = [
            'id', 
            'school', 
            'school_name', 
            'homeroom_teacher', 
            'homeroom_teacher_name', 
            'name', 
            'grade_level', 
            'academic_year', 
            'is_active', 
            'total_students'
        ]
        read_only_fields = ['school']

    def validate_homeroom_teacher(self, value):
        if value:
            request = self.context.get('request')
            if request and hasattr(request.user, 'teacher_profile'):
                school = request.user.teacher_profile.school
                if value.school != school:
                    raise serializers.ValidationError("Guru ini bukan berasal dari sekolah Anda.")
        return value


class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source='school.name')
    class_name = serializers.ReadOnlyField(source='student_class.name')

    class Meta:
        model = Student
        fields = [
            'id', 
            'school', 
            'school_name', 
            'student_class', 
            'class_name', 
            'nisn', 
            'nis', 
            'full_name', 
            'gender', 
            'birth_place', 
            'birth_date', 
            'address', 
            'parent_phone_number', 
            'status', 
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['school', 'created_at', 'updated_at']