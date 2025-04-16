from django.db.models import FloatField
from django.db.models.expressions import RawSQL
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from apps.medical_card.models import MedicalCard
from apps.patient.models import Patient
from apps.patient.serializers import FullPatientSerializer
from apps.med_personal.permissions import IsRegistrarOrAdmin
from core.face_utils import search_similar_faces_sync
from apps.medical_card.serializers import ShortMedicalCardSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """API для пациентов."""
    queryset = Patient.objects.all()
    serializer_class = FullPatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegistrarOrAdmin]
    lookup_field = 'id'

    @action(detail=False, methods=['GET'], url_path='search-by-snils-or-fio')
    def search_patient_by_snils_or_FIO(self, request):
        """Функция для поиска пациентов по ФИО и снилс."""
        snils = request.query_params.get('snils')
        full_name = request.query_params.get('full_name', '').strip()

        if snils:
            result = Patient.objects.filter(snils=snils)
        elif full_name:
            result = Patient.objects.annotate(
                similarity=RawSQL(
                    "public.similarity(last_name::text, %s::text) + "
                    "public.similarity(first_name::text, %s::text) + "
                    "public.similarity(middle_name::text, %s::text)",
                    (full_name, full_name, full_name),
                    output_field=FloatField()
                )
            ).filter(similarity__gt=0.3).order_by('-similarity')
        else:
            return Response({'detail': 'Не указаны snils или full_name'}, status=status.HTTP_400_BAD_REQUEST)

        if not result.exists():
            return Response({'detail': 'Пациенты  не  найдены'}, status=status.HTTP_404_NOT_FOUND)

        medical_cards = MedicalCard.objects.filter(patient__in=result)
        serializer = ShortMedicalCardSerializer(medical_cards, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='search-by-face', parser_classes=[MultiPartParser, FormParser])
    def search_patient_by_face(self, request):
        """Функция для поиска пациентов по лицу."""
        if 'photo' not in request.FILES and 'photo' not in request.data:
            return Response({'detail': 'Не указана фотография'}, status=status.HTTP_400_BAD_REQUEST)
        photo = request.data.get('photo') or request.FILES.get('photo')
        similar_patients = search_similar_faces_sync(photo)
        if not similar_patients.exists():
            return Response({'detail': 'Пациенты  не  найдены'}, status=status.HTTP_404_NOT_FOUND)
        medical_cards = MedicalCard.objects.filter(patient__in=similar_patients)
        serializer = ShortMedicalCardSerializer(medical_cards, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

