from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import TeacherProfile


# 1. Tampilkan TeacherProfile menyatu di dalam halaman User Django
class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Profil Guru / Admin Sekolah'
    fk_name = 'user'


# 2. Custom Tampilan User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (TeacherProfileInline,)
    list_display = ('username', 'email', 'first_name', 'get_school', 'get_role', 'is_staff')

    def get_school(self, obj):
        if hasattr(obj, 'teacher_profile'):
            return obj.teacher_profile.school.name
        return "-"
    get_school.short_description = 'Sekolah'

    def get_role(self, obj):
        if hasattr(obj, 'teacher_profile'):
            return obj.teacher_profile.role
        return "-"
    get_role.short_description = 'Role'


# 3. Re-register User Admin bawaan Django
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 4. Tetap daftarkan TeacherProfile secara independen
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'role', 'phone_number', 'is_active')
    list_filter = ('school', 'role', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__email', 'phone_number')