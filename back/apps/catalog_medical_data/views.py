from rest_framework import viewsets
from core.pagination import CustomPageNumberPagination
from apps.catalog_medical_data.serializers import DiseaseSerializer, MedicationSerializer
from apps.catalog_medical_data.models import Disease, Medication
from core.permissions import OnlyReadOrAdmin


class DiseaseViewSet(viewsets.ModelViewSet):
    """API для болезней."""
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [OnlyReadOrAdmin]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        return Disease.objects.all().order_by('id')


class MedicationViewSet(viewsets.ModelViewSet):
    """API для лекарств."""
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [OnlyReadOrAdmin]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        return Medication.objects.all().order_by('id')