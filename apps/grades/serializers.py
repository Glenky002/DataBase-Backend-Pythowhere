# from rest_framework import serializers


# class GradeSerializer(serializers.ModelSerializer):
#     student_name = serializers.ReadOnlyField(source='student.full_name')
#     class_name = serializers.ReadOnlyField(source='student_class.name')

#     class Meta:
#         model = Grade
#         fields = [
#             'id', 
#             'school', 
#             'student_class', 
#             'class_name', 
#             'student', 
#             'student_name', 
#             'teacher', 
#             'subject_name', 
#             'category', 
#             'title', 
#             'score', 
#             'notes', 
#             'created_at'
#         ]


# class BulkGradeItemSerializer(serializers.Serializer):
#     student_id = serializers.IntegerField()
#     category = serializers.CharField()
#     score = serializers.FloatField()
#     notes = serializers.CharField(required=False, allow_blank=True, default='')

# class BulkGradeSerializer(serializers.Serializer):
#     class_id = serializers.IntegerField()
#     subject_name = serializers.CharField()
#     date = serializers.DateField(required=False)
#     category = serializers.CharField(required=False, default='RAPOR')
#     title = serializers.CharField(required=False, default='Penilaian Rapor')
#     grades = BulkGradeItemSerializer(many=True)

# class SubjectGradeSummarySerializer(serializers.Serializer):
#     subject_name = serializers.CharField()
#     assignment_avg = serializers.FloatField(help_text="Rata-rata Nilai Tugas")
#     uts_score = serializers.FloatField(help_text="Nilai UTS")
#     uas_score = serializers.FloatField(help_text="Nilai UAS")
#     final_score = serializers.FloatField(help_text="Nilai Akhir (Tugas 20% + UTS 30% + UAS 50%)")
#     grade_letter = serializers.CharField(help_text="Predikat: A, B, C, D, F")
#     status = serializers.CharField(help_text="Lulus / Tidak Lulus")


# class StudentReportCardSerializer(serializers.Serializer):
#     student_id = serializers.IntegerField()
#     student_name = serializers.CharField()
#     nisn = serializers.CharField()
#     class_name = serializers.CharField()
#     academic_year = serializers.CharField()
#     subjects = SubjectGradeSummarySerializer(many=True)
#     overall_gpa = serializers.FloatField(help_text="Rata-rata Nilai Akhir Seluruh Mapel")


from rest_framework import serializers
from .models import GradeAssessment, StudentGrade
from apps.students.models import Student


class StudentGradeSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id')
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    nisn = serializers.CharField(source='student.nisn', read_only=True)

    class Meta:
        model = StudentGrade
        fields = ['id', 'student_id', 'student_name', 'nisn', 'score', 'notes']


class GradeAssessmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='student_class.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True, default='-')
    grades = StudentGradeSerializer(source='student_grades', many=True, read_only=True)

    class Meta:
        model = GradeAssessment
        fields = [
            'id', 'school', 'student_class', 'class_name', 
            'subject', 'subject_name', 'teacher', 'teacher_name',
            'title', 'category', 'date', 'grades', 'created_at'
        ]


class BulkCreateGradeSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    category = serializers.CharField(max_length=20)
    date = serializers.DateField()
    grades = serializers.ListField(
        child=serializers.DictField()
    )