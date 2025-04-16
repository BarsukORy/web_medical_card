from rest_framework import serializers
from apps.medical_hub.models import Hospital, Specialty


class ShortHospitalSerializer(serializers.ModelSerializer):
    """Сериализатор для краткой информации о больнице."""
    url = serializers.HyperlinkedIdentityField(
        view_name='hospital-detail',
        lookup_field='id'
    )

    class Meta:
        model = Hospital
        fields = [
            'id',
            'url',
            'name',
            'address'
        ]


class FullHospitalSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о больнице."""
    url = serializers.HyperlinkedIdentityField(
        view_name='hospital-detail',
        lookup_field='id'
    )

    class Meta:
        model = Hospital
        fields = [
            'id',
            'url',
            'name',
            'address',
            'phone_number',
            'email',
        ]


class SpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор для информации о врачебных специальностях."""
    url = serializers.HyperlinkedIdentityField(
        view_name='specialty-detail',
        lookup_field='id'
    )

    class Meta:
        model = Specialty
        fields = [
            'id',
            'url',
            'name',
            'description',
        ]