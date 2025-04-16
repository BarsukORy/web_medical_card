from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from apps.medical_card.models import (MedicalCard, MedicalCardEntry, MedicalCardEntryFile, Prescription,
                               PrescriptionMedication)


class MedicalCardEntryInline(TabularInline):
    model = MedicalCardEntry
    extra = 1
    fields = [
        'doctor',
        'visit_date',
        'hospital',
        'diagnosis'
    ]
    autocomplete_fields = [
        'doctor',
        'hospital',
        'diagnosis'
    ]


@admin.register(MedicalCard)
class MedicalCardAdmin(ModelAdmin):
    list_display = [
        'patient',
        'blood_type',
        'attachment_hospital',
        'get_allergies_short'
    ]
    list_filter = [
        'blood_type',
        'attachment_hospital'
    ]
    search_fields = [
        'patient__first_name',
        'patient__last_name',
        'patient__snils'
    ]
    inlines = [
        MedicalCardEntryInline
    ]
    autocomplete_fields = [
        'patient',
        'attachment_hospital'
    ]

    def get_allergies_short(self, obj):
        return obj.allergies[:50] + '...' if len(obj.allergies) > 50 else obj.allergies
    get_allergies_short.short_description = 'Аллергии(коротко)'


class MedicalCardEntryFileInline(TabularInline):
    model = MedicalCardEntryFile
    extra = 0
    fields = ['file']


class PrescriptionMedicationInline(StackedInline):
    model = PrescriptionMedication
    extra = 1
    fields = [
        'medication',
        'dosage',
        'frequency',
        'duration',
        'individual_notes'
    ]

    autocomplete_fields = ['medication']


class PrescriptionInline(TabularInline):
    model = Prescription
    extra = 0
    fields = [
        'administration_notes',
        'created_at'
    ]
    readonly_fields = ['created_at']


@admin.register(MedicalCardEntry)
class MedicalCardEntryAdmin(ModelAdmin):
    list_display = [
        'get_patient',
        'doctor',
        'visit_date',
        'hospital',
        'get_diagnosis'
    ]
    list_filter = [
        'visit_date',
        'hospital',
        'doctor'
    ]
    search_fields = [
        'medical_card__patient__first_name',
        'medical_card__patient__last_name',
        'medical_card__patient__snils'
    ]
    inlines = [
        MedicalCardEntryFileInline,
        PrescriptionInline
    ]
    date_hierarchy = 'visit_date'
    autocomplete_fields = [
        'doctor',
        'hospital',
        'diagnosis'
    ]

    def get_patient(self, obj):
        return obj.medical_card.patient
    get_patient.short_description = 'Пациент'

    def get_diagnosis(self, obj):
        return obj.diagnosis or obj.custom_diagnosis
    get_diagnosis.short_description = 'Диагноз'


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    list_display = [
        'get_medical_card_entry',
        'get_visit_date',
        'created_at'
    ]
    list_filter = ['created_at']
    inlines = [PrescriptionMedicationInline]

    def get_medical_card_entry(self, obj):
        return str(obj.medical_card_entry)
    get_medical_card_entry.short_description = 'Запись медкарты'

    def get_visit_date(self, obj):
        return obj.medical_card_entry.visit_date
    get_visit_date.short_description = 'Дата визита'