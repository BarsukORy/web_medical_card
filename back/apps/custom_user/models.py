from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя с ролями."""
    class Roles(models.TextChoices):
        DOCTOR = 'doctor', 'Doctor',
        REGISTRAR = 'registrar', 'Registrar',
        ADMIN = 'admin', 'Admin',

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        verbose_name='Роль',
        help_text='Роль пользователя в системе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


