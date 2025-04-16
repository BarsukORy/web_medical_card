from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from apps.medical_card.models import MedicalCardEntry
from apps.catalog_medical_data.models import Disease
from apps.med_personal.models import Doctor


class MedicalCardEntryFilter(FilterSet):
    visit_date = DateFilter(
        field_name='visit_date',
        lookup_expr='exact'
    )
    doctor = ModelChoiceFilter(
        queryset=Doctor.objects.all(),
        field_name='doctor'
    )
    diagnosis = ModelChoiceFilter(
        queryset=Disease.objects.all(),
        field_name='diagnosis'
    )

    class Meta:
        model = MedicalCardEntry
        fields = [
            'visit_date',
            'doctor',
            'diagnosis'
        ]