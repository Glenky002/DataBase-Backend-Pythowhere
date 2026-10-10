# # # # # # from rest_framework import serializers
# # # # # # from django.contrib.auth.models import User
# # # # # # from .models import TeacherProfile


# # # # # # class UserSerializer(serializers.ModelSerializer):
# # # # # #     class Meta:
# # # # # #         model = User
# # # # # #         fields = ['id', 'username', 'email', 'first_name', 'last_name']

# # # # # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # # # # #     user = UserSerializer()
# # # # # #     school_name = serializers.ReadOnlyField(source='school.name')

# # # # # #     class Meta:
# # # # # #         model = TeacherProfile
# # # # # #         fields = [
# # # # # #             'id', 
# # # # # #             'user', 
# # # # # #             'school', 
# # # # # #             'school_name', 
# # # # # #             'nip', 
# # # # # #             'phone_number', 
# # # # # #             'role', 
# # # # # #             'is_active', 
# # # # # #             'created_at'
# # # # # #         ]

# # # # # #     def create(self, validated_data):
# # # # # #         """Mendaftarkan User Django dan TeacherProfile sekaligus dalam 1 Request"""
# # # # # #         user_data = validated_data.pop('user')
        
# # # # # #         # 1. Buat User Django
# # # # # #         user = User.objects.create_user(
# # # # # #             username=user_data['username'],
# # # # # #             email=user_data.get('email', ''),
# # # # # #             first_name=user_data.get('first_name', ''),
# # # # # #             last_name=user_data.get('last_name', ''),
# # # # # #             password=self.context['request'].data.get('password', 'Password123!') # Password bawaan
# # # # # #         )
        
# # # # # #         # 2. Buat Profil Guru yang terikat ke Sekolah
# # # # # #         teacher_profile = TeacherProfile.objects.create(user=user, **validated_data)
# # # # # #         return teacher_profile

# # # # # from rest_framework import serializers
# # # # # from django.contrib.auth.models import User
# # # # # from django.db import transaction
# # # # # from .models import TeacherProfile


# # # # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # # # #     username = serializers.ReadOnlyField(source='user.username')
# # # # #     email = serializers.ReadOnlyField(source='user.email')
# # # # #     full_name = serializers.ReadOnlyField(source='user.get_full_name')

# # # # #     class Meta:
# # # # #         model = TeacherProfile
# # # # #         fields = [
# # # # #             'id', 
# # # # #             'username', 
# # # # #             'email', 
# # # # #             'full_name', 
# # # # #             'nip', 
# # # # #             'role', 
# # # # #             'gender', 
# # # # #             'main_subject', 
# # # # #             'phone_number', 
# # # # #             'address'
# # # # #         ]


# # # # # class CreateTeacherSerializer(serializers.Serializer):
# # # # #     username = serializers.CharField(max_length=150)
# # # # #     email = serializers.EmailField()
# # # # #     password = serializers.CharField(write_only=True, min_length=8)
# # # # #     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
# # # # #     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
# # # # #     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
# # # # #     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
# # # # #     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
# # # # #     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
# # # # #     address = serializers.CharField(required=False, allow_blank=True)

# # # # #     def validate_username(self, value):
# # # # #         if User.objects.filter(username=value).exists():
# # # # #             raise serializers.ValidationError("Username ini sudah digunakan.")
# # # # #         return value

# # # # #     def create(self, validated_data):
# # # # #         # Otomatis ambil sekolah dari user login (Admin)
# # # # #         request = self.context.get('request')
# # # # #         school = request.user.teacher_profile.school

# # # # #         with transaction.atomic():
# # # # #             full_name = validated_data.get('full_name', '')
# # # # #             first_name = full_name.split()[0] if full_name else ''
# # # # #             last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''

# # # # #             user = User.objects.create_user(
# # # # #                 username=validated_data['username'],
# # # # #                 email=validated_data['email'],
# # # # #                 password=validated_data['password'],
# # # # #                 first_name=first_name,
# # # # #                 last_name=last_name
# # # # #             )

# # # # #             profile = TeacherProfile.objects.create(
# # # # #                 user=user,
# # # # #                 school=school,  # <-- Otomatis terikat ke sekolah Admin
# # # # #                 nip=validated_data.get('nip', ''),
# # # # #                 role=validated_data.get('role', 'TEACHER'),
# # # # #                 gender=validated_data.get('gender'),
# # # # #                 main_subject=validated_data.get('main_subject', ''),
# # # # #                 phone_number=validated_data.get('phone_number', ''),
# # # # #                 address=validated_data.get('address', '')
# # # # #             )
# # # # #             return profile


# # # # # serializers.py
# # # # from rest_framework import serializers
# # # # from django.contrib.auth.models import User
# # # # from django.db import transaction
# # # # from .models import TeacherProfile


# # # # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # # # #     username = serializers.ReadOnlyField(source='user.username')
# # # # #     email = serializers.SerializerMethodField()
# # # # #     full_name = serializers.SerializerMethodField()

# # # # #     class Meta:
# # # # #         model = TeacherProfile
# # # # #         fields = [
# # # # #             'id', 
# # # # #             'username', 
# # # # #             'email', 
# # # # #             'full_name', 
# # # # #             'nip', 
# # # # #             'role', 
# # # # #             'gender', 
# # # # #             'main_subject', 
# # # # #             'phone_number', 
# # # # #             'address'
# # # # #         ]

# # # # #     def get_email(self, obj):
# # # # #         return obj.user.email if obj.user else ''

# # # # #     def get_full_name(self, obj):
# # # # #         if obj.user:
# # # # #             name = obj.user.get_full_name()
# # # # #             return name if name.strip() else obj.user.username
# # # # #         return '-'

# # # # #     def update(self, instance, validated_data):
# # # # #         # Update User Email & Full Name jika disertakan dalam request update
# # # # #         request = self.context.get('request')
# # # # #         if request and request.data:
# # # # #             full_name = request.data.get('full_name', '').strip()
# # # # #             email = request.data.get('email', '').strip()
            
# # # # #             user = instance.user
# # # # #             if user:
# # # # #                 if email:
# # # # #                     user.email = email
# # # # #                 if full_name:
# # # # #                     name_parts = full_name.split()
# # # # #                     user.first_name = name_parts[0]
# # # # #                     user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# # # # #                 user.save()

# # # # #         return super().update(instance, validated_data)\

# # # # from rest_framework import serializers
# # # # from .models import TeacherProfile

# # # # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # # # #     username = serializers.ReadOnlyField(source='user.username')
# # # # #     email = serializers.SerializerMethodField()
# # # # #     full_name = serializers.SerializerMethodField()

# # # # #     class Meta:
# # # # #         model = TeacherProfile
# # # # #         fields = [
# # # # #             'id', 'username', 'email', 'full_name', 'nip', 
# # # # #             'role', 'gender', 'main_subject', 'phone_number', 'address'
# # # # #         ]

# # # # #     def get_email(self, obj):
# # # # #         return obj.user.email if obj.user else ''

# # # # #     def get_full_name(self, obj):
# # # # #         if obj.user:
# # # # #             name = obj.user.get_full_name()
# # # # #             return name if name.strip() else obj.user.username
# # # # #         return '-'

# # # # #     def update(self, instance, validated_data):
# # # # #         request = self.context.get('request')
# # # # #         user = request.user if request else None

# # # # #         # PENTING: Jika BUKAN ADMIN / Superuser, kunci field 'role' agar tidak bisa diubah
# # # # #         # if user and not user.is_superuser:
# # # # #         #     if hasattr(user, 'teacher_profile') and user.teacher_profile.role != 'ADMIN':
# # # # #         #         validated_data.pop('role', None)

# # # # #         if 'role' in validated_data and validated_data['role'] != instance.role:
# # # # #             if user and not user.is_superuser:
# # # # #                 if hasattr(user, 'teacher_profile') and user.teacher_profile.role != 'ADMIN':
# # # # #                     raise serializers.ValidationError({
# # # # #                         "role": "Anda tidak memiliki izin Admin untuk mengubah role pengguna."
# # # # #                     })

# # # # #         # Update User Email & Full Name
# # # # #         if request and request.data:
# # # # #             full_name = request.data.get('full_name', '').strip()
# # # # #             email = request.data.get('email', '').strip()
            
# # # # #             target_user = instance.user
# # # # #             if target_user:
# # # # #                 if email:
# # # # #                     target_user.email = email
# # # # #                 if full_name:
# # # # #                     name_parts = full_name.split()
# # # # #                     target_user.first_name = name_parts[0]
# # # # #                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# # # # #                 target_user.save()

# # # # #         return super().update(instance, validated_data)

# # # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # # #     username = serializers.ReadOnlyField(source='user.username')
# # # #     email = serializers.SerializerMethodField()
# # # #     full_name = serializers.SerializerMethodField()

# # # #     class Meta:
# # # #         model = TeacherProfile
# # # #         fields = [
# # # #             'id', 'username', 'email', 'full_name', 'nip', 
# # # #             'role', 'gender', 'main_subject', 'phone_number', 'address'
# # # #         ]

# # # #     def get_email(self, obj):
# # # #         return obj.user.email if obj.user else ''

# # # #     def get_full_name(self, obj):
# # # #         if obj.user:
# # # #             name = obj.user.get_full_name()
# # # #             return name if name.strip() else obj.user.username
# # # #         return '-'

# # # #     def update(self, instance, validated_data):
# # # #         request = self.context.get('request')
# # # #         user = request.user if request else None

# # # #         # PROTEKSI ROLE: Jika bukan Admin/Superuser dan mencoba mengubah role -> Tolak dengan 400 Bad Request
# # # #         if 'role' in validated_data and validated_data['role'] != instance.role:
# # # #             is_admin = False
# # # #             if user and user.is_superuser:
# # # #                 is_admin = True
# # # #             elif user and hasattr(user, 'teacher_profile') and user.teacher_profile.role == 'ADMIN':
# # # #                 is_admin = True

# # # #             if not is_admin:
# # # #                 raise serializers.ValidationError({
# # # #                     "role": "Akses Ditolak: Anda tidak memiliki izin Admin untuk mengubah role pengguna."
# # # #                 })

# # # #         # Update data user (email & full_name)
# # # #         if request and request.data:
# # # #             full_name = request.data.get('full_name', '').strip()
# # # #             email = request.data.get('email', '').strip()
            
# # # #             target_user = instance.user
# # # #             if target_user:
# # # #                 if email:
# # # #                     target_user.email = email
# # # #                 if full_name:
# # # #                     name_parts = full_name.split()
# # # #                     target_user.first_name = name_parts[0]
# # # #                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# # # #                 target_user.save()

# # # #         return super().update(instance, validated_data)


# # # # class CreateTeacherSerializer(serializers.Serializer):
# # # #     username = serializers.CharField(max_length=150)
# # # #     email = serializers.EmailField()
# # # #     password = serializers.CharField(write_only=True, min_length=8)
# # # #     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
# # # #     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
# # # #     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
# # # #     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
# # # #     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
# # # #     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
# # # #     address = serializers.CharField(required=False, allow_blank=True)

# # # #     def validate_username(self, value):
# # # #         if User.objects.filter(username=value).exists():
# # # #             raise serializers.ValidationError("Username ini sudah digunakan.")
# # # #         return value

# # # #     def create(self, validated_data):
# # # #         request = self.context.get('request')
# # # #         if not hasattr(request.user, 'teacher_profile'):
# # # #             raise serializers.ValidationError("User login tidak memiliki profil sekolah yang valid.")

# # # #         school = request.user.teacher_profile.school

# # # #         with transaction.atomic():
# # # #             full_name = validated_data.get('full_name', '').strip()
# # # #             name_parts = full_name.split() if full_name else []
# # # #             first_name = name_parts[0] if name_parts else ''
# # # #             last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

# # # #             user = User.objects.create_user(
# # # #                 username=validated_data['username'],
# # # #                 email=validated_data['email'],
# # # #                 password=validated_data['password'],
# # # #                 first_name=first_name,
# # # #                 last_name=last_name
# # # #             )

# # # #             profile = TeacherProfile.objects.create(
# # # #                 user=user,
# # # #                 school=school,
# # # #                 nip=validated_data.get('nip', ''),
# # # #                 role=validated_data.get('role', 'TEACHER'),
# # # #                 gender=validated_data.get('gender'),
# # # #                 main_subject=validated_data.get('main_subject', ''),
# # # #                 phone_number=validated_data.get('phone_number', ''),
# # # #                 address=validated_data.get('address', '')
# # # #             )
# # # #             return profile

# # # from rest_framework import serializers
# # # from django.contrib.auth.models import User
# # # from django.db import transaction
# # # from .models import TeacherProfile


# # # class TeacherProfileSerializer(serializers.ModelSerializer):
# # #     username = serializers.ReadOnlyField(source='user.username')
# # #     email = serializers.SerializerMethodField()
# # #     full_name = serializers.SerializerMethodField()

# # #     class Meta:
# # #         model = TeacherProfile
# # #         fields = [
# # #             'id', 'username', 'email', 'full_name', 'nip', 
# # #             'role', 'gender', 'main_subject', 'phone_number', 'address'
# # #         ]

# # #     def get_email(self, obj):
# # #         return obj.user.email if obj.user else ''

# # #     def get_full_name(self, obj):
# # #         if obj.user:
# # #             name = obj.user.get_full_name()
# # #             return name if name.strip() else obj.user.username
# # #         return '-'

# # #     def update(self, instance, validated_data):
# # #         request = self.context.get('request')
# # #         user = request.user if request else None

# # #         # CHECK ROLE ACCESS: Jika bukan Admin/Superuser dan mencoba merubah role -> Throw 400 Bad Request
# # #         if 'role' in validated_data and validated_data['role'] != instance.role:
# # #             is_admin = False
# # #             if user and user.is_superuser:
# # #                 is_admin = True
# # #             elif user and hasattr(user, 'teacher_profile') and user.teacher_profile.role == 'ADMIN':
# # #                 is_admin = True

# # #             if not is_admin:
# # #                 raise serializers.ValidationError({
# # #                     "role": "Akses Ditolak: Hanya Admin Sekolah yang diizinkan mengubah role pengguna."
# # #                 })

# # #         # Update data User (email & full_name)
# # #         if request and request.data:
# # #             full_name = request.data.get('full_name', '').strip()
# # #             email = request.data.get('email', '').strip()
            
# # #             target_user = instance.user
# # #             if target_user:
# # #                 if email:
# # #                     target_user.email = email
# # #                 if full_name:
# # #                     name_parts = full_name.split()
# # #                     target_user.first_name = name_parts[0]
# # #                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# # #                 target_user.save()

# # #         return super().update(instance, validated_data)


# # # class CreateTeacherSerializer(serializers.Serializer):
# # #     username = serializers.CharField(max_length=150)
# # #     email = serializers.EmailField()
# # #     password = serializers.CharField(write_only=True, min_length=8)
# # #     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
# # #     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
# # #     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
# # #     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
# # #     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
# # #     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
# # #     address = serializers.CharField(required=False, allow_blank=True)

# # #     def validate_username(self, value):
# # #         if User.objects.filter(username=value).exists():
# # #             raise serializers.ValidationError("Username ini sudah digunakan.")
# # #         return value

# # #     def create(self, validated_data):
# # #         request = self.context.get('request')
# # #         if not hasattr(request.user, 'teacher_profile'):
# # #             raise serializers.ValidationError("User login tidak memiliki profil sekolah yang valid.")

# # #         school = request.user.teacher_profile.school

# # #         with transaction.atomic():
# # #             full_name = validated_data.get('full_name', '').strip()
# # #             name_parts = full_name.split() if full_name else []
# # #             first_name = name_parts[0] if name_parts else ''
# # #             last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

# # #             user = User.objects.create_user(
# # #                 username=validated_data['username'],
# # #                 email=validated_data['email'],
# # #                 password=validated_data['password'],
# # #                 first_name=first_name,
# # #                 last_name=last_name
# # #             )

# # #             profile = TeacherProfile.objects.create(
# # #                 user=user,
# # #                 school=school,
# # #                 nip=validated_data.get('nip', ''),
# # #                 role=validated_data.get('role', 'TEACHER'),
# # #                 gender=validated_data.get('gender'),
# # #                 main_subject=validated_data.get('main_subject', ''),
# # #                 phone_number=validated_data.get('phone_number', ''),
# # #                 address=validated_data.get('address', '')
# # #             )
# # #             return profile


# # from rest_framework import serializers
# # from django.contrib.auth.models import User
# # from django.db import transaction
# # from .models import TeacherProfile

# # class TeacherProfileSerializer(serializers.ModelSerializer):
# #     username = serializers.ReadOnlyField(source='user.username')
# #     email = serializers.SerializerMethodField()
# #     full_name = serializers.SerializerMethodField()

# #     class Meta:
# #         model = TeacherProfile
# #         fields = [
# #             'id', 'username', 'email', 'full_name', 'nip', 
# #             'role', 'gender', 'main_subject', 'phone_number', 'address'
# #         ]

# #     def get_email(self, obj):
# #         return obj.user.email if obj.user else ''

# #     def get_full_name(self, obj):
# #         if obj.user:
# #             name = obj.user.get_full_name()
# #             return name if name.strip() else obj.user.username
# #         return '-'

# #     def update(self, instance, validated_data):
# #         request = self.context.get('request')
# #         user = request.user if request else None

# #         # Proteksi Ubah Role: Harus Admin
# #         if 'role' in validated_data and validated_data['role'] != instance.role:
# #             is_admin = False
# #             if user and (user.is_superuser or user.is_staff):
# #                 is_admin = True
# #             elif user and hasattr(user, 'teacher_profile') and user.teacher_profile.role == 'ADMIN':
# #                 is_admin = True

# #             if not is_admin:
# #                 raise serializers.ValidationError({
# #                     "role": "Hanya Admin Sekolah yang memiliki izin untuk mengubah role pengguna."
# #                 })

# #         # Update User Email & Full Name
# #         if request and request.data:
# #             full_name = request.data.get('full_name', '').strip()
# #             email = request.data.get('email', '').strip()
            
# #             target_user = instance.user
# #             if target_user:
# #                 if email:
# #                     target_user.email = email
# #                 if full_name:
# #                     name_parts = full_name.split()
# #                     target_user.first_name = name_parts[0]
# #                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# #                 target_user.save()

# #         return super().update(instance, validated_data)


# # class CreateTeacherSerializer(serializers.Serializer):
# #     username = serializers.CharField(max_length=150)
# #     email = serializers.EmailField()
# #     password = serializers.CharField(write_only=True, min_length=8)
# #     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
# #     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
# #     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
# #     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
# #     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
# #     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
# #     address = serializers.CharField(required=False, allow_blank=True)

# #     def validate_username(self, value):
# #         if User.objects.filter(username=value).exists():
# #             raise serializers.ValidationError("Username ini sudah digunakan.")
# #         return value

# #     def create(self, validated_data):
# #         request = self.context.get('request')
# #         if not hasattr(request.user, 'teacher_profile'):
# #             raise serializers.ValidationError("User login tidak memiliki profil sekolah yang valid.")

# #         school = request.user.teacher_profile.school

# #         with transaction.atomic():
# #             full_name = validated_data.get('full_name', '').strip()
# #             name_parts = full_name.split() if full_name else []
# #             first_name = name_parts[0] if name_parts else ''
# #             last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

# #             user = User.objects.create_user(
# #                 username=validated_data['username'],
# #                 email=validated_data['email'],
# #                 password=validated_data['password'],
# #                 first_name=first_name,
# #                 last_name=last_name
# #             )

# #             profile = TeacherProfile.objects.create(
# #                 user=user,
# #                 school=school,
# #                 nip=validated_data.get('nip', ''),
# #                 role=validated_data.get('role', 'TEACHER'),
# #                 gender=validated_data.get('gender'),
# #                 main_subject=validated_data.get('main_subject', ''),
# #                 phone_number=validated_data.get('phone_number', ''),
# #                 address=validated_data.get('address', '')
# #             )
# #             return profile

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.db import transaction
# from .models import TeacherProfile

# class TeacherProfileSerializer(serializers.ModelSerializer):
#     username = serializers.ReadOnlyField(source='user.username')
#     email = serializers.SerializerMethodField()
#     full_name = serializers.SerializerMethodField()

#     class Meta:
#         model = TeacherProfile
#         fields = [
#             'id', 'username', 'email', 'full_name', 'nip', 
#             'role', 'gender', 'main_subject', 'phone_number', 'address'
#         ]

#     def get_email(self, obj):
#         return obj.user.email if obj.user else ''

#     def get_full_name(self, obj):
#         if obj.user:
#             name = obj.user.get_full_name()
#             return name if name.strip() else obj.user.username
#         return '-'

#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         if request and request.data:
#             full_name = request.data.get('full_name', '').strip()
#             email = request.data.get('email', '').strip()
            
#             target_user = instance.user
#             if target_user:
#                 if email:
#                     target_user.email = email
#                 if full_name:
#                     name_parts = full_name.split()
#                     target_user.first_name = name_parts[0]
#                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
#                 target_user.save()

#         return super().update(instance, validated_data)


# class CreateTeacherSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True, min_length=8)
#     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
#     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
#     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
#     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
#     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
#     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
#     address = serializers.CharField(required=False, allow_blank=True)

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username ini sudah digunakan.")
#         return value

#     def create(self, validated_data):
#         request = self.context.get('request')
#         school = request.user.teacher_profile.school if hasattr(request.user, 'teacher_profile') else None

#         with transaction.atomic():
#             full_name = validated_data.get('full_name', '').strip()
#             name_parts = full_name.split() if full_name else []
#             first_name = name_parts[0] if name_parts else ''
#             last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

#             user = User.objects.create_user(
#                 username=validated_data['username'],
#                 email=validated_data['email'],
#                 password=validated_data['password'],
#                 first_name=first_name,
#                 last_name=last_name
#             )

#             profile = TeacherProfile.objects.create(
#                 user=user,
#                 school=school,
#                 nip=validated_data.get('nip', ''),
#                 role=validated_data.get('role', 'TEACHER'),
#                 gender=validated_data.get('gender'),
#                 main_subject=validated_data.get('main_subject', ''),
#                 phone_number=validated_data.get('phone_number', ''),
#                 address=validated_data.get('address', '')
#             )
#             return profile



        
# # class TeacherProfileSerializer(serializers.ModelSerializer):
# #     username = serializers.ReadOnlyField(source='user.username')
# #     email = serializers.SerializerMethodField()
# #     full_name = serializers.SerializerMethodField()

# #     class Meta:
# #         model = TeacherProfile
# #         fields = [
# #             'id', 'username', 'email', 'full_name', 'nip', 
# #             'role', 'gender', 'main_subject', 'phone_number', 'address'
# #         ]

# #     def get_email(self, obj):
# #         return obj.user.email if obj.user else ''

# #     def get_full_name(self, obj):
# #         if obj.user:
# #             name = obj.user.get_full_name()
# #             return name if name.strip() else obj.user.username
# #         return '-'

# #     def update(self, instance, validated_data):
# #         request = self.context.get('request')
        
# #         # Update First Name & Last Name & Email di auth_user
# #         if request and request.data:
# #             full_name = request.data.get('full_name', '').strip()
# #             email = request.data.get('email', '').strip()
            
# #             target_user = instance.user
# #             if target_user:
# #                 if email:
# #                     target_user.email = email
# #                 if full_name:
# #                     name_parts = full_name.split()
# #                     target_user.first_name = name_parts[0]
# #                     target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
# #                 target_user.save()

# #         return super().update(instance, validated_data)


# # class CreateTeacherSerializer(serializers.Serializer):
# #     username = serializers.CharField(max_length=150)
# #     email = serializers.EmailField()
# #     password = serializers.CharField(write_only=True, min_length=8)
# #     full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
# #     role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
# #     nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
# #     gender = serializers.ChoiceField(choices=TeacherProfile.GENDER_CHOICES, required=False, allow_null=True)
# #     main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
# #     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
# #     address = serializers.CharField(required=False, allow_blank=True)

# #     def validate_username(self, value):
# #         if User.objects.filter(username=value).exists():
# #             raise serializers.ValidationError("Username ini sudah digunakan.")
# #         return value

# #     def create(self, validated_data):
# #         request = self.context.get('request')
# #         if not hasattr(request.user, 'teacher_profile') and not request.user.is_superuser:
# #             raise serializers.ValidationError("User login tidak memiliki profil sekolah yang valid.")

# #         school = request.user.teacher_profile.school if hasattr(request.user, 'teacher_profile') else None

# #         with transaction.atomic():
# #             full_name = validated_data.get('full_name', '').strip()
# #             name_parts = full_name.split() if full_name else []
# #             first_name = name_parts[0] if name_parts else ''
# #             last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

# #             user = User.objects.create_user(
# #                 username=validated_data['username'],
# #                 email=validated_data['email'],
# #                 password=validated_data['password'],
# #                 first_name=first_name,
# #                 last_name=last_name
# #             )

# #             profile = TeacherProfile.objects.create(
# #                 user=user,
# #                 school=school,
# #                 nip=validated_data.get('nip', ''),
# #                 role=validated_data.get('role', 'TEACHER'),
# #                 gender=validated_data.get('gender'),
# #                 main_subject=validated_data.get('main_subject', ''),
# #                 phone_number=validated_data.get('phone_number', ''),
# #                 address=validated_data.get('address', '')
# #             )
# #             return profile


from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import TeacherProfile

class TeacherProfileSerializer(serializers.ModelSerializer):
    """
    Serializer Read & Update (PATCH) TeacherProfile
    """
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()  # <-- TAMBAHKAN INI (Safe Alias)

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'username', 'email', 'full_name', 'user_full_name', 'nip', 
            'role', 'gender', 'main_subject', 'phone_number', 'address'
        ]

    def get_email(self, obj):
        return obj.user.email if obj.user else ''

    def get_full_name(self, obj):
        if obj.user:
            name = obj.user.get_full_name()
            return name if name.strip() else obj.user.username
        return '-'

    def get_user_full_name(self, obj):
        """Alias method agar kompatibel dengan komponen Next.js jadwal & academics"""
        return self.get_full_name(obj)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.data:
            full_name = str(request.data.get('full_name', '')).strip()
            email = str(request.data.get('email', '')).strip()
            
            target_user = instance.user
            if target_user:
                if email:
                    target_user.email = email
                if full_name:
                    name_parts = full_name.split()
                    target_user.first_name = name_parts[0]
                    target_user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                target_user.save()

        return super().update(instance, validated_data)

class CreateTeacherSerializer(serializers.Serializer):
    """
    Serializer Create User Baru oleh Admin
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=TeacherProfile.ROLE_CHOICES, default='TEACHER')
    nip = serializers.CharField(max_length=30, required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    main_subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username ini sudah digunakan.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email ini sudah terdaftar.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        admin_profile = getattr(request.user, 'teacher_profile', None) if request else None
        school = admin_profile.school if admin_profile else None

        with transaction.atomic():
            full_name = validated_data.get('full_name', '').strip()
            name_parts = full_name.split() if full_name else []
            first_name = name_parts[0] if name_parts else validated_data['username']
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=first_name,
                last_name=last_name
            )

            profile = TeacherProfile.objects.create(
                user=user,
                school=school,
                nip=validated_data.get('nip', ''),
                role=validated_data.get('role', 'TEACHER'),
                gender=validated_data.get('gender') or 'L',
                main_subject=validated_data.get('main_subject', ''),
                phone_number=validated_data.get('phone_number', ''),
                address=validated_data.get('address', '')
            )
            return profile