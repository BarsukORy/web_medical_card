from django.contrib import admin
from unfold.admin import ModelAdmin
from django import forms
from apps.med_personal.models import Doctor, Registrar
from apps.custom_user.models import CustomUser


class DoctorForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    role = forms.ChoiceField(choices=CustomUser.Roles.choices, label='Роль')

    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'hospital',
            'specialization'
        ]

    def save(self, commit=True):
        # Создаём или получаем CustomUser
        user_data = {
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
            'role': self.cleaned_data['role'],
        }
        user, created = CustomUser.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password(self.cleaned_data['password'])
            user.save()

        # Устанавливаем связь с Doctor
        doctor = super().save(commit=False)
        doctor.user = user  # Привязываем пользователя
        if commit:
            doctor.save()
            # Синхронизируем поля MedPersonalStaff с данными формы
            doctor.first_name = self.cleaned_data['first_name']
            doctor.last_name = self.cleaned_data['last_name']
            doctor.middle_name = self.cleaned_data['middle_name']
            doctor.phone_number = self.cleaned_data['phone_number']
            doctor.hospital = self.cleaned_data['hospital']
            doctor.specialization.set(self.cleaned_data['specialization'])
            doctor.save()
        return doctor


class RegistrarForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    role = forms.ChoiceField(choices=CustomUser.Roles.choices, label='Роль')

    class Meta:
        model = Registrar
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'hospital'
        ]

    def save(self, commit=True):
        # Создаём или получаем CustomUser
        user_data = {
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
            'role': self.cleaned_data['role'],
        }
        user, created = CustomUser.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password(self.cleaned_data['password'])
            user.save()

        # Устанавливаем связь с Registrar
        registrar = super().save(commit=False)
        registrar.user = user  # Привязываем пользователя
        if commit:
            registrar.save()
            # Синхронизируем поля MedPersonalStaff с данными формы
            registrar.first_name = self.cleaned_data['first_name']
            registrar.last_name = self.cleaned_data['last_name']
            registrar.middle_name = self.cleaned_data['middle_name']
            registrar.phone_number = self.cleaned_data['phone_number']
            registrar.hospital = self.cleaned_data['hospital']
            registrar.save()
        return registrar


@admin.register(Doctor)
class DoctorAdmin(ModelAdmin):
    form = DoctorForm
    list_display = [
        'first_name',
        'last_name',
        'middle_name',
        'specialties',
        'hospital',
        'phone_number'
    ]
    search_fields = [
        'first_name',
        'last_name',
        'middle_name',
        'phone_number',
        'hospital__name'
    ]
    list_filter = ['hospital', 'specialization']
    filter_horizontal = ['specialization']

    def specialties(self, obj):
        return ", ".join(obj.specialization.values_list('name', flat=True))


@admin.register(Registrar)
class RegistrarAdmin(ModelAdmin):
    form = RegistrarForm
    list_display = [
        'first_name',
        'last_name',
        'middle_name',
        'hospital',
        'phone_number'
    ]
    search_fields = [
        'first_name',
        'last_name',
        'middle_name',
        'phone_number',
        'hospital__name'
    ]
    list_filter = ['hospital']