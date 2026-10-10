from django.contrib import admin
from .models import StudentClass, Student

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'school', 'is_active')
    list_filter = ('school', 'academic_year', 'is_active')
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nisn', 'student_class', 'school', 'gender', 'is_active')
    list_filter = ('school', 'student_class', 'gender', 'is_active')
    search_fields = ('full_name', 'nisn', 'parent_phone_number')