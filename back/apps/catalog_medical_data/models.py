from django.db import models


class Disease(models.Model):
    """Модель для хранения информации о заболеваниях."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное название заболевания'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание',
        help_text='Подробное описание заболевания'
    )

    class Meta:
        verbose_name = 'Заболевание'
        verbose_name_plural = 'Заболевания'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Medication(models.Model):
    """Модель для хранения информации о лекарственных препаратах."""
    class Forms(models.TextChoices):
        PILLS = 'таблетки', 'Таблетки'
        CAPSULES = 'капсулы', 'Капсулы'
        SYRUP = 'сироп', 'Сироп'
        AEROSOL = 'аэрозоль', 'Аэрозоль'
        INJECTION = 'инъекции', 'Инъекции'

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное название препарата'
    )
    form = models.CharField(
        max_length=20,
        choices=Forms.choices,
        verbose_name='Форма выпуска',
        help_text='Форма выпуска препарата'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание',
        help_text='Подробное описание препарата'
    )

    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.form})"