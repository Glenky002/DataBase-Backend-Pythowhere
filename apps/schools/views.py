from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import School
from .serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk kelola data Sekolah / Multi-Tenancy.
    """
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.]

    def get_queryset(self):
        """
        Secara default hanya menampilkan sekolah yang aktif.
        Jika query params `?include_deleted=true` dikirim oleh Superuser,
        tampilkan seluruh sekolah termasuk yang sudah di-soft-delete.
        """
        include_deleted = self.request.query_params.get('include_deleted', 'false').lower() == 'true'
        
        if include_deleted and self.request.user.is_superuser:
            return School.all_objects.all()
        
        return School.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Override fungsi DELETE agar melakukan Soft Delete alih-alih hard delete.
        """
        instance = self.get_object()
        instance.soft_delete()
        return Response(
            {"detail": f"Akun sekolah '{instance.name}' berhasil dinonaktifkan (Soft Delete)."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='restore')
    def restore_school(self, request, pk=None):
        """
        Custom Action: POST /api/v1/schools/{id}/restore/
        Digunakan oleh Admin untuk mengembalikan akun sekolah yang pernah dihapus.
        """
        try:
            school = School.all_objects.get(pk=pk)
        except School.DoesNotExist:
            return Response({"detail": "Sekolah tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        if not school.deleted_at:
            return Response({"detail": "Sekolah ini sudah dalam keadaan aktif."}, status=status.HTTP_400_BAD_REQUEST)

        school.restore()
        serializer = self.get_serializer(school)
        return Response(
            {
                "detail": f"Akun sekolah '{school.name}' berhasil dipulihkan.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )