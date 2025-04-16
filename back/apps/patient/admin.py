from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.medical_card.models import MedicalCard
from apps.patient.models import Patient


class MedicalCardInline(TabularInline):
    model = MedicalCard
    extra = 1
    list_display = [
        'blood_type',
        'attachment_hospital'
    ]


@admin.register(Patient)
class PatientAdmin(ModelAdmin):
    list_display = [
        'id',
        'uuid',
        'first_name',
        'last_name',
        'birth_date',
        'snils',
        'gender',
        'registration_address',
        'actual_address',
    ]
    list_filter = [
        'gender',
        'birth_date'
    ]
    search_fields = [
        'first_name',
        'last_name',
        'birth_date',
        'snils',
    ]
    ordering = ['birth_date']