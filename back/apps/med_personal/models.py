from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from apps.medical_hub.models import Hospital, Specialty
from apps.custom_user.models import CustomUser


class MedPersonalStaff(models.Model):
    """Абстрактная модель для медицинского персонала."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Связанный пользователь'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Имя сотрудника'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        help_text='Фамилия сотрудника'
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Отчество',
        help_text='Отчество сотрудника (не обязательно)'
    )
    phone_number = PhoneNumberField(
        region='RU',
        unique=True,
        verbose_name='Номер телефона',
        help_text='Уникальный телефон формата +7**********'
    )

    class Meta:
        abstract = True

    @property
    def full_name(self) -> str:
        if not self.middle_name:
            return f'{self.last_name} {self.first_name}'
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def __str__(self):
        return self.full_name


class Doctor(MedPersonalStaff):
    """Модель для хранения информации о врачах."""
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='doctors',
        verbose_name='Мед учереждение',
        help_text='Мед учреждение, к которому прикреплен врач'
    )
    specialization = models.ManyToManyField(
        Specialty,
        related_name='doctors_specializations',
        verbose_name='Специализация',
        help_text='Специализации врача'
    )

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    @property
    def specialties(self) -> str:
        return ', '.join(self.specialization.values_list('name', flat=True))


class Registrar(MedPersonalStaff):
    """Модель для хранения информации о регистраторах."""
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='registrars',
        verbose_name='Мед учереждение',
        help_text='Мед учреждение, к которому прикреплен регистратор'
    )

    class Meta:
        verbose_name = 'Регистратура'
        verbose_name_plural = 'Регистратура'




