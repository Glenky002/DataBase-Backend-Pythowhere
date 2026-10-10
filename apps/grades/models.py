from django.db import models
from apps.schools.models import School
from apps.students.models import Student, StudentClass
from apps.users.models import TeacherProfile
from apps.academics.models import Subject  # Relasi langsung ke master mapel
from django.utils import timezone


class GradeAssessment(models.Model):
    """
    Model Induk: Menampung 1 pelaksanaan Ujian / Tugas per Kelas & Mapel
    (Contoh: "Tugas 1 Aljabar", "UTS Semester Ganjil")
    """
    CATEGORY_CHOICES = (
        ('ASSIGNMENT', 'Tugas / PR / Kuis'),
        ('DAILY_EXAM', 'Ulangan Harian'),
        ('UTS', 'Ujian Tengah Semester'),
        ('UAS', 'Ujian Akhir Semester'),
        ('PRACTICE', 'Praktikum / Proyek'),
    )

    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='assessments'
    )
    student_class = models.ForeignKey(
        StudentClass, 
        on_delete=models.CASCADE, 
        related_name='assessments'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='assessments'
    )
    teacher = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Guru pengampu / penilai"
    )
    
    title = models.CharField(max_length=150, help_text="Contoh: Tugas 1 Aljabar, UH Trigonometri")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ASSIGNMENT')
    date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'grade_assessments'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.student_class.name})"


class StudentGrade(models.Model):
    """
    Model Rincian: Menampung Nilai Murni per Siswa untuk Ujian Terkait
    """
    assessment = models.ForeignKey(
        GradeAssessment, 
        on_delete=models.CASCADE, 
        related_name='student_grades'
    )
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='student_grades'
    )
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Nilai (0 - 100)"
    )
    notes = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text="Catatan evaluasi guru per siswa"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_grades'
        unique_together = ('assessment', 'student')

    def __str__(self):
        return f"{self.student.full_name} - {self.assessment.title}: {self.score}"