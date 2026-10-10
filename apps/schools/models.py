import uuid
from django.db import models
from django.utils import timezone


class ActiveSchoolManager(models.Manager):
    """Manager khusus agar kueri bawaan hanya mengambil sekolah yang belum dihapus (Soft Delete)"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class School(models.Model):
    SUBSCRIPTION_STATUS = (
        ('TRIAL', 'Masa Uji Coba'),
        ('ACTIVE', 'Berlangganan Aktif'),
        ('EXPIRED', 'Kedaluwarsa'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Nama Sekolah / Yayasan")
    npsn = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text="Nomor Pokok Sekolah Nasional")
    email = models.EmailField(blank=True, null=True, help_text="Email Resmi Sekolah / Administrasi")  # <-- Field Email
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Kontak Resmi Sekolah")

    subscription_status = models.CharField(max_length=10, choices=SUBSCRIPTION_STATUS, default='TRIAL')
    max_student_quota = models.IntegerField(default=500, help_text="Batas maksimal jumlah siswa")
    # Timestamp Log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft Delete Field (Sesuai Kebutuhan Hapus Akun)
    deleted_at = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="Tanggal akun dinonaktifkan/dihapus. Jika NULL berarti akun masih aktif."
    )

    # Manager
    objects = ActiveSchoolManager()       # School.objects.all() -> Hanya ambil yang aktif
    all_objects = models.Manager()        # School.all_objects.all() -> Ambil semua termasuk yang dihapus

    class Meta:
        db_table = 'schools'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.npsn})"

    def soft_delete(self):
        """Method untuk menghapus akun secara aman tanpa membuang data dari database"""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Method untuk memulihkan akun yang pernah dihapus"""
        self.deleted_at = None
        self.save()