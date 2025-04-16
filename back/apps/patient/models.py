from datetime import date
import uuid
from django.db import models
from pgvector.django import VectorField
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from core.file_handler import FileHandler
from apps.patient.utils import patient_photo_path, prepare_photo_directory, generate_face_vector


def validate_birth_date(value):
    if value > date.today():
        raise ValidationError('Дата рождения не может быть в будущем')


class Patient(models.Model):
    """Модель для хранения информации о пациентах."""
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Уникальный идентификатор',
        help_text='Уникальный идентификатор'
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Имя пациента'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        help_text='Фамилия пациента'
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Отчество',
        help_text='Отчество пациента (не обязательно)'
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        help_text='Дата рождения пациента',
        validators=[validate_birth_date]
    )
    snils = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='СНИЛС',
        help_text='Уникальный СНИЛС пациента'
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name='Пол',
        help_text='Пол пациента'
    )
    registration_address = models.CharField(
        max_length=500,
        verbose_name='Адрес регистрации',
        help_text='Адрес регистрации пациента'
    )
    actual_address = models.CharField(
        max_length=500,
        verbose_name='Фактический адрес',
        help_text='Фактический адрес проживания пациента'
    )
    photo = models.ImageField(
        upload_to=patient_photo_path,
        verbose_name='Фотография',
        help_text='Фотография пациента для распознавания'
    )
    face_vector = VectorField(
        dimensions=512,
        blank=True,
        null=True,
        verbose_name='Вектор лица',
        help_text='Векторное представление лица пациента'
    )

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['snils']
        indexes = [
            models.Index(fields=['snils']),
        ]

    def save(self, *args, **kwargs):
        old_photo_name = None
        if self.pk:
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_photo_name = old_instance.photo.name if old_instance.photo else None
        new_photo_name = self.photo.name if self.photo else None
        photo_changed = old_photo_name != new_photo_name and old_photo_name is not None
        super().save(*args, **kwargs)
        if photo_changed:
            FileHandler.delete_file(old_photo_name)
        if self.photo:
            prepare_photo_directory(self)
            if not default_storage.exists(self.photo.name):
                FileHandler.save_file(self, 'photo', patient_photo_path)
            if self.face_vector is None or photo_changed:
                generate_face_vector(self)
                super().save(update_fields=['face_vector'])

    def delete(self, *args, **kwargs):
        FileHandler.delete_patient_folder(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.snils}'

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name}'
        return f'{self.last_name} {self.first_name}'