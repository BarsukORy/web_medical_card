from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.medical_hub.models import Hospital, Specialty


@admin.register(Hospital)
class HospitalAdmin(ModelAdmin):
    list_display = [
        'name',
        'address',
        'phone_number',
        'email',
    ]
    search_fields = [
        'name',
        'address',
        'phone_number',
        'email',
    ]


@admin.register(Specialty)
class SpecialtyAdmin(ModelAdmin):
    list_display = [
        'name',
        'description',
    ]
    search_fields = ['name']
