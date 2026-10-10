from django.contrib import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'npsn', 'phone_number', 'created_at', 'deleted_at', 'is_active')
    list_filter = ('deleted_at', 'created_at')
    search_fields = ('name', 'npsn', 'phone_number')
    readonly_fields = ('id', 'created_at', 'updated_at')

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = "Status Aktif"