from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from apps.schools.models import School
from apps.users.models import TeacherProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSchoolSerializer(serializers.Serializer):
    # Field Sekolah
    school_name = serializers.CharField(max_length=255)
    school_npsn = serializers.CharField(max_length=20)
    school_address = serializers.CharField(required=False, allow_blank=True)
    school_phone = serializers.CharField(required=False, allow_blank=True)

    # Field Admin (Menggunakan Prefix admin_)
    admin_username = serializers.CharField(max_length=150)
    admin_email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    admin_first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    admin_last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    admin_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_school_npsn(self, value):
        if School.objects.filter(npsn=value).exists():
            raise serializers.ValidationError("Sekolah dengan NPSN ini sudah terdaftar.")
        return value

    def validate_admin_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username ini sudah digunakan.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            school = School.objects.create(
                name=validated_data['school_name'],
                npsn=validated_data['school_npsn'],
                address=validated_data.get('school_address', ''),
                phone_number=validated_data.get('school_phone', '')
            )

            user = User.objects.create_user(
                username=validated_data['admin_username'],
                email=validated_data['admin_email'],
                password=validated_data['password'],
                first_name=validated_data.get('admin_first_name', ''),
                last_name=validated_data.get('admin_last_name', '')
            )

            TeacherProfile.objects.create(
                user=user,
                school=school,
                role='ADMIN',
                phone_number=validated_data.get('admin_phone', '')
            )

            return {
                'school': school,
                'user': user
            }

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Custom claims ke payload JWT
#         token['username'] = user.username
#         token['email'] = user.email
#         token['full_name'] = user.get_full_name() or user.username

#         # Pengecekan aman untuk teacher_profile & school
#         profile = getattr(user, 'teacher_profile', None)
#         if profile and profile.school:
#             token['school_id'] = str(profile.school.id)
#             token['school_name'] = profile.school.name
#             token['role'] = profile.role or 'TEACHER'
#         else:
#             token['school_id'] = None
#             token['school_name'] = None
#             token['role'] = 'SUPERUSER' if user.is_superuser else 'ADMIN'

#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         # Safe Extraction
#         profile = getattr(self.user, 'teacher_profile', None)
#         school = profile.school if profile else None

#         # Tentukan role secara eksplisit
#         if profile and profile.role:
#             user_role = profile.role
#         elif self.user.is_superuser or self.user.is_staff:
#             user_role = 'ADMIN'
#         else:
#             user_role = 'ADMIN'  # Default fallback untuk registrasi akun admin sekolah baru

#         # Response payload saat login sukses
#         data['user'] = {
#             'id': self.user.id,
#             'username': self.user.username,
#             'email': self.user.email,
#             'full_name': self.user.get_full_name() or self.user.username,
#             'role': user_role,
#             'school_id': school.id if school else None,
#             'school_name': school.name if school else None,
#         }
#         return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer Login JWT:
    Menyuntikkan role dan school_id secara aman ke dalam Token Payload & Response Body
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.get_full_name() or user.username

        profile = getattr(user, 'teacher_profile', None)
        if profile and profile.school:
            token['school_id'] = str(profile.school.id)
            token['school_name'] = profile.school.name
            token['role'] = profile.role or 'TEACHER'
        else:
            token['school_id'] = None
            token['school_name'] = None
            token['role'] = 'SUPERUSER' if user.is_superuser else 'ADMIN'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        profile = getattr(self.user, 'teacher_profile', None)
        school = profile.school if profile else None

        if profile and profile.role:
            user_role = profile.role
        elif self.user.is_superuser or self.user.is_staff:
            user_role = 'ADMIN'
        else:
            user_role = 'ADMIN'

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'full_name': self.user.get_full_name() or self.user.username,
            'role': user_role,
            'school_id': school.id if school else None,
            'school_name': school.name if school else None,
        }
        return data




# from django.db import transaction
# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from apps.schools.models import School
# from apps.users.models import TeacherProfile
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class RegisterSchoolSerializer(serializers.Serializer):
#     # Data Sekolah
#     school_name = serializers.CharField(max_length=255)
#     school_npsn = serializers.CharField(max_length=50)
#     school_email = serializers.EmailField(required=False, allow_blank=True)
#     school_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
#     school_address = serializers.CharField(required=False, allow_blank=True)

#     # Data Admin Sekolah
#     admin_username = serializers.CharField(max_length=150)
#     admin_email = serializers.EmailField()
#     admin_first_name = serializers.CharField(max_length=150)
#     admin_last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
#     admin_phone = serializers.CharField(max_length=20)
#     password = serializers.CharField(write_only=True)

#     def validate_school_code(self, value):
#         npsn = value.upper()
#         if School.objects.filter(code=npsn).exists():
#             raise serializers.ValidationError("Kode sekolah/NPSN ini sudah terdaftar.")
#         return npsn

#     def validate_admin_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username ini sudah digunakan.")
#         return value

#     def validate_password(self, value):
#         validate_password(value)
#         return value

#     def create(self, validated_data):
#         with transaction.atomic():
#             # 1. Buat Sekolah
#             school = School.objects.create(
#                 name=validated_data['school_name'],
#                 npsn=validated_data['school_npsn'],
#                 email=validated_data.get('school_email', ''),
#                 phone_number=validated_data.get('school_phone', ''),
#                 address=validated_data.get('school_address', '')
#             )

#             # 2. Buat User Django
#             user = User.objects.create_user(
#                 username=validated_data['admin_username'],
#                 email=validated_data['admin_email'],
#                 first_name=validated_data['admin_first_name'],
#                 last_name=validated_data.get('admin_last_name', ''),
#                 password=validated_data['password']
#             )

#             # 3. Buat TeacherProfile Admin Sekolah
#             teacher_profile = TeacherProfile.objects.create(
#                 user=user,
#                 school=school,
#                 phone_number=validated_data['admin_phone'],
#                 role='ADMIN',
#                 is_active=True
#             )

#             return {'school': school, 'user': user, 'teacher_profile': teacher_profile}

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Tambahkan custom claims ke dalam payload JWT
#         token['username'] = user.username
#         token['email'] = user.email
#         token['full_name'] = user.get_full_name() or user.username

#         if hasattr(user, 'teacher_profile'):
#             token['school_id'] = str(user.teacher_profile.school.id)
#             token['school_name'] = user.teacher_profile.school.name
#             token['role'] = user.teacher_profile.role
#         else:
#             token['school_id'] = None
#             token['role'] = 'SUPERUSER' if user.is_superuser else 'GUEST'

#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         # Response kustom saat login sukses
#         data['user'] = {
#             'id': self.user.id,
#             'username': self.user.username,
#             'email': self.user.email,
#             'full_name': self.user.get_full_name() or self.user.username,
#             'role': getattr(self.user.teacher_profile, 'role', 'ADMIN') if hasattr(self.user, 'teacher_profile') else 'SUPERUSER',
#             'school_id': getattr(self.user.teacher_profile.school, 'id', None) if hasattr(self.user, 'teacher_profile') else None,
#             'school_name': getattr(self.user.teacher_profile.school, 'name', None) if hasattr(self.user, 'teacher_profile') else None,
#         }
#         return data