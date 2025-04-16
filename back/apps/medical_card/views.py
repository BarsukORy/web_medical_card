import django_filters
from rest_framework import viewsets, permissions
from core.pagination import CustomPageNumberPagination, MedicalCardEntryPagination
from apps.medical_card.models import (
    MedicalCard, MedicalCardEntry, MedicalCardEntryFile, Prescription, PrescriptionMedication
)
from apps.medical_card.serializers import (
    ShortMedicalCardSerializer, FullMedicalCardSerializer, MedicalCardEntrySerializer, MedicalCardEntryFileSerializer,
    PrescriptionSerializer, PrescriptionMedicationSerializer
)
from apps.medical_card.filters import MedicalCardEntryFilter


class MedicalCardViewSet(viewsets.ModelViewSet):
    """API для мед карты."""
    permission_classes = [permissions.IsAuthenticated]
    queryset = MedicalCard.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortMedicalCardSerializer
        return FullMedicalCardSerializer


class MedicalCardEntryViewSet(viewsets.ModelViewSet):
    """API для записей мед карты."""
    serializer_class = MedicalCardEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MedicalCardEntryPagination
    lookup_field = 'id'
    filterset_class = MedicalCardEntryFilter
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        medical_card_id = self.kwargs.get('medical_card_id')
        if medical_card_id:
            return MedicalCardEntry.objects.filter(medical_card_id=medical_card_id).order_by('id')
        return MedicalCardEntry.objects.none()


class MedicalCardEntryFileViewSet(viewsets.ModelViewSet):
    """API для файлов для записей мед карты."""
    serializer_class = MedicalCardEntryFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        medical_card_entry_id = self.kwargs.get('medical_card_entry_id')
        return MedicalCardEntryFile.objects.filter(medical_card_entry_id=medical_card_entry_id)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """API для назначений."""
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        medical_card_entry_id = self.kwargs.get('medical_card_entry_id')
        return Prescription.objects.filter(medical_card_entry_id=medical_card_entry_id)


class PrescriptionMedicationViewSet(viewsets.ModelViewSet):
    """API для назначения на прием препаратов."""
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        prescription_id = self.kwargs.get('prescription_id')
        return PrescriptionMedication.objects.filter(prescription_id=prescription_id)