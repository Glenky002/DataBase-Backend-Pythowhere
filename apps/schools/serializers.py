from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    """Serializer untuk membaca dan membuat data sekolah"""
    class Meta:
        model = School
        fields = [
            'id', 
            'name', 
            'npsn', 
            'address', 
            'phone_number',
            'email',
            'created_at', 
            'updated_at', 
            'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

    def validate_code(self, value):
        """Memastikan kode sekolah di-uppercase secara otomatis"""
        return value.upper()