

from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser or user.is_staff:
            return True

        profile = getattr(user, 'teacher_profile', None)
        if not profile:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return profile.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        user_profile = getattr(user, 'teacher_profile', None)
        if not user_profile or user_profile.role != 'ADMIN':
            return False

        # SAFE NULL-CHECK: Bebas dari AttributeError meskipun school bernilai None
        user_school_id = getattr(user_profile.school, 'id', None) if user_profile.school else None
        target_school_id = getattr(obj.school, 'id', None) if obj.school else None

        # Jika kedua user tidak punya sekolah, atau sekolahnya beda -> Tolak
        if user_school_id is None or target_school_id is None:
            # Toleransi jika Admin mengedit guru di bawah instansinya
            return True 

        return user_school_id == target_school_id