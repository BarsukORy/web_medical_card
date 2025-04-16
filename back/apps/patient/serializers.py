from datetime import date
from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.medical_card.models import MedicalCard
from apps.patient.models import Patient


class ShortPatientSerializer(serializers.ModelSerializer):
    """Сериализатор для короткой информации о пациенте."""
    url = serializers.HyperlinkedIdentityField(
        view_name='patient-detail',
        lookup_field='id'
    )

    class Meta:
        model = Patient
        fields = [
            'id',
            'url',
            'full_name',
            'snils'
        ]


class FullPatientSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о пациенте."""
    url = serializers.HyperlinkedIdentityField(
        view_name='patient-detail',
        lookup_field='id'
    )
    medical_card = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'url',
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'snils',
            'gender',
            'registration_address',
            'actual_address',
            'photo',
            'face_vector',
            'medical_card'
        ]
        read_only_fields = [
            'id',
            'face_vector'
        ]

    def get_medical_card(self, obj):
        """Функция для получения мед карты, если она есть."""
        try:
            medical_card = obj.patient_medical_card
        except MedicalCard.DoesNotExist:
            return None
        return {
            'id': medical_card.id,
            'full_name': obj.full_name,
            'url': reverse('medical-card-detail', args=[medical_card.id], request=self.context['request']),
        }

    # def is_valid_snils(self, snils: str) -> bool:
    #     """Функция для валидации снилса."""
    #     if len(snils) != 11 or not snils.isdigit():
    #         return False
    #     digits = list(map(int, snils[:9]))
    #     weights = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    #     total = sum(d * w for d, w in zip(digits, weights))
    #     if total > 101:
    #         total %= 101
    #     if total == 100 or total == 101:
    #         total = 0
    #     calculated_control = f"{total:02d}"
    #     actual_control = snils[-2:]
    #     return calculated_control == actual_control

    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата рождения не может быть в будущем")
        return value

    def validate(self, data):
        if 'snils' in data:
            snils = data.get('snils')
            if not snils: #or not self.is_valid_snils(snils):
                raise serializers.ValidationError('Invalid snils')
        return data