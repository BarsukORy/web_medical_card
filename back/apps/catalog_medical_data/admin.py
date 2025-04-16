from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.catalog_medical_data.models import Disease, Medication


@admin.register(Disease)
class DiseaseAdmin(ModelAdmin):
    list_display = [
        'name',
        'description'
    ]
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Medication)
class MedicationAdmin(ModelAdmin):
    list_display = [
        'name',
        'form',
        'description'
    ]
    list_filter = ['form']
    search_fields = [
        'name',
        'form',
    ]
