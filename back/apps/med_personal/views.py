from rest_framework import viewsets, permissions
from .serializers import FullDoctorSerializer, RegistrarSerializer
from apps.med_personal.models import Doctor, Registrar
from apps.med_personal.permissions import IsOwnerOrAdmin


class DoctorViewSet(viewsets.ModelViewSet):
    """API для доктора."""
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = FullDoctorSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Doctor.objects.all()
        return Doctor.objects.filter(user=user)


class RegistrarViewSet(viewsets.ModelViewSet):
    """API для регистратуры."""
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = RegistrarSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Registrar.objects.all()
        return Registrar.objects.filter(user=user)




