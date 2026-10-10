from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.full_name')
    class_name = serializers.ReadOnlyField(source='student_class.name')

    class Meta:
        model = Attendance
        fields = [
            'id', 
            'school', 
            'student_class', 
            'class_name', 
            'student', 
            'student_name', 
            'recorded_by', 
            'date', 
            'status', 
            'notes', 
            'created_at'
        ]


class BulkAttendanceItemSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Attendance.STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class BulkAttendanceSerializer(serializers.Serializer):
    # school_id = serializers.UUIDField()
    class_id = serializers.IntegerField()
    date = serializers.DateField()
    attendances = BulkAttendanceItemSerializer(many=True)


class AttendanceSummaryItemSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    nisn = serializers.CharField()
    total_days = serializers.IntegerField(help_text="Total hari sekolah tercatat")
    hadir = serializers.IntegerField()
    sakit = serializers.IntegerField()
    izin = serializers.IntegerField()
    alpa = serializers.IntegerField()
    attendance_percentage = serializers.FloatField(help_text="Persentase Kehadiran (%)")
    parent_phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True) # ✅ Tambahkan ini

class ClassAttendanceSummarySerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    class_name = serializers.CharField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    students_summary = AttendanceSummaryItemSerializer(many=True)