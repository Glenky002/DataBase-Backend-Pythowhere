from django.db import models
from apps.schools.models import School
from apps.users.models import TeacherProfile


class StudentClass(models.Model):
    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='classes'
    )

    homeroom_teacher = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_classes',
        help_text="Wali Kelas"
    )

    name = models.CharField(max_length=100, help_text="Contoh: X IPA 1, XI IPS 2")
    grade_level = models.IntegerField(default=10, help_text="Tingkat Kelas (misal: 10, 11, 12)")
    academic_year = models.CharField(max_length=20, help_text="Contoh: 2026/2027")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_classes'
        ordering = ['name']
        unique_together = ('school', 'name', 'academic_year')

    def __str__(self):
        return f"{self.name} ({self.academic_year}) - {self.school.name}"


class Student(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Aktif'),
        ('GRADUATED', 'Lulus'),
        ('TRANSFERRED', 'Pindah'),
        ('DROPPED_OUT', 'Keluar'),
    )

    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='students'
    )
    student_class = models.ForeignKey(
        StudentClass, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )
    nisn = models.CharField(max_length=20, help_text="Nomor Induk Siswa Nasional")
    nis = models.CharField(max_length=20, blank=True, null=True, help_text="Nomor Induk Sekolah Internal")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    parent_phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        help_text="Nomor WhatsApp Orang Tua untuk Notifikasi Absensi"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['full_name']
        unique_together = ('school', 'nisn')

    def __str__(self):
        return f"{self.full_name} ({self.nisn}) - {self.school.name}"