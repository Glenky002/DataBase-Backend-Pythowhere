from django.db import models
from apps.schools.models import School
from apps.students.models import Student, StudentClass
from apps.users.models import TeacherProfile


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('PRESENT', 'Hadir'),
        ('PERMIT', 'Izin'),
        ('SICK', 'Sakit'),
        ('ABSENT', 'Alpa'),
    )

    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    student_class = models.ForeignKey(
        StudentClass, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    recorded_by = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Guru yang menginput absensi"
    )
    date = models.DateField(help_text="Tanggal Absensi (YYYY-MM-DD)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='H')
    notes = models.TextField(blank=True, null=True, help_text="Catatan izin/sakit")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendances'
        ordering = ['-date', 'student__full_name']
        unique_together = ('student', 'date')  # 1 Siswa hanya punya 1 record absensi per hari

    @property
    def full_name(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return f"Guru #{self.id}"
    
    def __str__(self):
        return f"{self.student.full_name} - {self.date} ({self.get_status_display()})"