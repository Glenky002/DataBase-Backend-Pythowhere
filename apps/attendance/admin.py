from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_class', 'date', 'status', 'school')
    list_filter = ('school', 'date', 'status', 'student_class')
    search_fields = ('student__full_name', 'student__nisn')