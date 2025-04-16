from rest_framework import viewsets, response
from core.pagination import CustomPageNumberPagination
from apps.medical_hub.models import Hospital, Specialty
from apps.medical_hub.serializers import FullHospitalSerializer, SpecialtySerializer
from core.permissions import OnlyReadOrAdmin


class HospitalViewSet(viewsets.ModelViewSet):
    """API для больниц."""
    queryset = Hospital.objects.all()
    serializer_class = FullHospitalSerializer
    permission_classes = [OnlyReadOrAdmin]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        count = Hospital.objects.count()
        return response.Response({'count_hospital': count})

    def get_queryset(self):
        return Hospital.objects.all().order_by('id')


class SpecialtyViewSet(viewsets.ModelViewSet):
    """API для врачебных специальностей."""
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [OnlyReadOrAdmin]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        count = Specialty.objects.count()
        return response.Response({'count_specialty': count})




