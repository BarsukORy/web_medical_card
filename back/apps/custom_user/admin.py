from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.custom_user.models import CustomUser
from apps.med_personal.models import Doctor, Registrar


class DoctorInline(TabularInline):
    model = Doctor
    extra = 0
    list_display = [
        'first_name',
        'last_name',
        'phone_number',
        'specialties',
        'hospital'
    ]
    can_delete = False
    verbose_name = 'Врач'
    verbose_name_plural = 'Врачи'


class RegistrarInline(TabularInline):
    model = Registrar
    extra = 0
    list_display = [
        'first_name',
        'last_name',
        'phone_number',
        'hospital'
    ]
    can_delete = False
    verbose_name = 'Регистратура'
    verbose_name_plural = 'Регистратура'


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = [
        'username',
        'email'
    ]
    search_fields = [
        'username',
        'email'
    ]

