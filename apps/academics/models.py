# from django.db import models

# class Subject(models.Model):
#     """Model Mata Pelajaran (misal: Matematika Wajib, Fisika)"""
#     school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='subjects')
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=20, blank=True, null=True)

#     def __str__(self):
#         return self.name


# class Schedule(models.Model):
#     """Model Jadwal Pelajaran per Kelas"""
#     DAY_CHOICES = [
#         ('SENIN', 'Senin'),
#         ('SELASA', 'Selasa'),
#         ('RABU', 'Rabu'),
#         ('KAMIS', 'Kamis'),
#         ('JUMAT', 'Jumat'),
#         ('SABTU', 'Sabtu'),
#     ]

#     school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='schedules')
#     student_class = models.ForeignKey('students.StudentClass', on_delete=models.CASCADE, related_name='schedules')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
#     teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    
#     day = models.CharField(max_length=10, choices=DAY_CHOICES)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     class Meta:
#         ordering = ['day', 'start_time']

#     def __str__(self):
#         return f"{self.student_class.name} - {self.subject.name} ({self.day})"


from django.db import models


class Subject(models.Model):
    """Model Mata Pelajaran (misal: Matematika Wajib, Fisika)"""
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class SubjectPassingGrade(models.Model):
    """Model KKM (Kriteria Ketuntasan Minimal) per Mapel dan Kelas"""
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='passing_grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='passing_grades')
    student_class = models.ForeignKey('students.StudentClass', on_delete=models.CASCADE, related_name='passing_grades')
    kkm = models.IntegerField(default=75)

    class Meta:
        unique_together = ('school', 'subject', 'student_class')

    def __str__(self):
        return f"{self.subject.name} - {self.student_class.name} (KKM: {self.kkm})"


class Schedule(models.Model):
    """Model Jadwal Pelajaran per Kelas"""
    DAY_CHOICES = [
        ('SENIN', 'Senin'),
        ('SELASA', 'Selasa'),
        ('RABU', 'Rabu'),
        ('KAMIS', 'Kamis'),
        ('JUMAT', 'Jumat'),
        ('SABTU', 'Sabtu'),
    ]

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='schedules')
    student_class = models.ForeignKey('students.StudentClass', on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.student_class.name} - {self.subject.name} ({self.day})"