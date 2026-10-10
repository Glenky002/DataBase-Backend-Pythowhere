from django.db import models
from django.contrib.auth.models import User
from apps.schools.models import School


class TeacherProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin Sekolah'),
        ('TEACHER', 'Guru Pengajar'),
        ('STAFF', 'Staf Tata Usaha'),
    )

    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher_profile'
    )
    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='teachers',
        help_text="Sekolah tempat guru/staf bertugas"
    )
    nip = models.CharField(max_length=50, blank=True, null=True, help_text="NIP / Nomor Induk Pegawai")
    phone_number = models.CharField(max_length=20, help_text="Nomor WhatsApp Aktif Guru")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TEACHER')
    

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    main_subject = models.CharField(max_length=100, blank=True, null=True, help_text="Mata Pelajaran Utama yang Diampu")
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True, help_text="Status keaktifan akun guru")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_profiles'
        ordering = ['-created_at']

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f"{full_name} ({self.role}) - {self.school.name}"
