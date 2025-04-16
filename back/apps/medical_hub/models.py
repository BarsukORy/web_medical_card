from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Hospital(models.Model):
    """Модель для хранения информации о больницах."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название больницы'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес',
        help_text='Адрес больницы'
    )
    phone_number = PhoneNumberField(
        region='RU',
        unique=True,
        verbose_name='Номер телефона',
        help_text='Уникальный телефон больницы'
    )
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='Email',
        help_text='Электронная почта больницы'
    )

    class Meta:
        verbose_name = 'Больница'
        verbose_name_plural = 'Больницы'
        indexes = [
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'address'],
                name='unique_name_address'
            ),
        ]

    def __str__(self):
        return self.name


class Specialty(models.Model):
    """Модель для хранения информации о специализациях."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Название специализации'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание',
        help_text='Описание специализации'
    )

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

