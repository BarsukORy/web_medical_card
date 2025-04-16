from rest_framework import serializers
from apps.catalog_medical_data.models import Disease, Medication


class DiseaseSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='disease-detail',
        lookup_field='id'
    )

    class Meta:
        model = Disease
        fields = '__all__'


class MedicationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='medication-detail',
        lookup_field='id'
    )

    class Meta:
        model = Medication
        fields = '__all__'

