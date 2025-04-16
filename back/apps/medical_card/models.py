from datetime import date
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.db import models
from core.file_handler import FileHandler
from apps.medical_card.utils import medical_card_entry_file_path
from apps.patient.models import Patient
from apps.medical_hub.models import Hospital
from apps.catalog_medical_data.models import Disease, Medication
from apps.med_personal.models import Doctor


class MedicalCard(models.Model):
    """Модель медицинская карта."""
    class BloodType(models.TextChoices):
        O_POSITIVE = 'O+', 'O (I) Rh+'
        O_NEGATIVE = 'O-', 'O (I) Rh-'
        A_POSITIVE = 'A+', 'A (II) Rh+'
        A_NEGATIVE = 'A-', 'A (II) Rh-'
        B_POSITIVE = 'B+', 'B (III) Rh+'
        B_NEGATIVE = 'B-', 'B (III) Rh-'
        AB_POSITIVE = 'AB+', 'AB (IV) Rh+'
        AB_NEGATIVE = 'AB-', 'AB (IV) Rh-'

    patient = models.OneToOneField(
        Patient,
        on_delete=models.PROTECT,
        related_name='patient_medical_card',
        verbose_name='Пациент',
        help_text='Привязанный пациент'
    )
    attachment_hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='hospital_medical_card',
        verbose_name='Прикрепленная больница',
        help_text='Основное медучреждение для пациента'
    )
    blood_type = models.CharField(
        max_length=6,
        choices=BloodType.choices,
        verbose_name='Группа крови',
        help_text='Полная группа крови с резус-фактором'
    )
    allergies = models.TextField(
        blank=True,
        default='',
        verbose_name='Аллергии',
        help_text='Список аллергенов и реакций'
    )
    chronic_diseases = models.TextField(
        blank=True,
        default='',
        verbose_name='Хронические заболевания',
        help_text='Список хронических заболеваний'
    )

    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = 'Медицинские карты'
        indexes = [
            models.Index(fields=['blood_type']),
        ]

    def __str__(self):
        return f"Медкарта пациента '{self.patient.full_name}'"

    @property
    def blood_group(self):
        """Возвращает только группу крови."""
        return self.blood_type[:-1] if self.blood_type else None

    @property
    def rh_factor(self):
        """Возвращает только резус-фактор."""
        return self.blood_type[-1] if self.blood_type else None

    def clean(self):
        super().clean()
        if not self.blood_type:
            raise ValidationError({'blood_type': 'Группа крови обязательна для заполнения'})
        if self.blood_type not in dict(self.BloodType.choices):
            raise ValidationError({'blood_type': 'Недопустимое значение группы крови'})


def validate_visit_date(value):
    if value > date.today():
        raise ValidationError('Дата визита не может быть позже текущей даты')


class MedicalCardEntry(models.Model):
    """Модель для записей медицинской карты."""
    medical_card = models.ForeignKey(
        MedicalCard,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Медицинская карта',
        help_text='Медицинская карта, для которой создается запись'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='doctor_entries',
        verbose_name='Лечащий врач',
        help_text='Ответственный медицинский специалист'
    )
    visit_date = models.DateField(
        verbose_name='Дата визита',
        help_text='Фактическая дата приема пациента',
        validators=[validate_visit_date]
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='hospital_entries',
        verbose_name='Мед учреждение',
        help_text='Учреждение где проводился прием',
    )
    diagnosis = models.ForeignKey(
        Disease,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='diagnosis_entries',
        verbose_name='Основной диагноз',
        help_text='Диагноз из классификатора заболеваний'
    )
    custom_diagnosis = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name='Индивидуальный диагноз',
        help_text='Уточненный или дополнительный диагноз'
    )
    treatment = models.TextField(
        blank=True,
        default='',
        verbose_name='План лечения',
        help_text='Стандартизированный протокол лечения'
    )
    custom_treatment = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name='Индивидуальное лечение',
        help_text='Особые назначения и рекомендации'
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Примечания',
        help_text='Дополнительные комментарии и наблюдения'
    )

    class Meta:
        verbose_name = 'Запись медкарты'
        verbose_name_plural = 'Записи медкарт'
        ordering = ['-visit_date']
        constraints = [
            models.CheckConstraint(
                check=Q(diagnosis__isnull=True) | Q(custom_diagnosis=''),
                name='check_one_diagnosis_only'
            ),
            models.CheckConstraint(
                check=Q(diagnosis__isnull=False) | ~Q(custom_diagnosis=''),
                name='check_one_diagnosis_required'
            )
        ]

    def __str__(self):
        diagnosis_text = self.diagnosis or self.custom_diagnosis
        return f"Запись от {self.visit_date} ({diagnosis_text})"

    def check_duplicate(self, doctor, visit_date, diagnosis=None, custom_diagnosis=None):
        qs = self.__class__.objects.filter(
            medical_card=self.medical_card,
            doctor=doctor,
            visit_date=visit_date
        )
        if diagnosis is not None:
            qs = qs.filter(diagnosis=diagnosis)
        elif custom_diagnosis:
            qs = qs.filter(custom_diagnosis=custom_diagnosis)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        return qs.exists()

    def clean(self):
        super().clean()
        if self.diagnosis and self.custom_diagnosis:
            raise ValidationError({
                'diagnosis': 'Выберите только один тип диагноза',
                'custom_diagnosis': 'Выберите только один тип диагноза'
            })
        if not self.diagnosis and not self.custom_diagnosis:
            raise ValidationError({
                'diagnosis': 'Необходимо указать диагноз',
                'custom_diagnosis': 'Необходимо указать диагноз'
            })

    @property
    def get_diagnosis(self):
        if self.diagnosis:
            return self.diagnosis.name
        return self.custom_diagnosis


class MedicalCardEntryFile(models.Model):
    """Модель для файлов для записей мед карты."""
    medical_card_entry = models.ForeignKey(
        MedicalCardEntry,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Запись медкарты',
        help_text='Запись медицинской карты, к которой прикреплен файл'
    )
    file = models.FileField(
        upload_to=medical_card_entry_file_path,
        max_length=500,
        verbose_name='Файл медзаписи',
        help_text='Файл, прикрепленный к записи медкарты',
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])]
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def save(self, *args, **kwargs):
        old_file_name = None
        if self.pk:
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_file_name = old_instance.file.name if old_instance.file else None
        new_file_name = self.file.name if self.file else None
        file_changed = old_file_name != new_file_name and old_file_name is not None
        if file_changed:
            FileHandler.delete_file(old_file_name)
        if self.file:
            FileHandler.save_file(self, 'file', medical_card_entry_file_path)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        FileHandler.delete_file_and_delete_directory_is_empty(self.file.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Файл для {self.medical_card_entry} ({self.file.name})"


class Prescription(models.Model):
    """Модель для назначения на прием препаратов."""
    medical_card_entry = models.ForeignKey(
        MedicalCardEntry,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Запись в карте',
        help_text='Связанная медицинская запись'
    )
    administration_notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Особые указания',
        help_text='Общие указания для всех препаратов'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['medical_card_entry'])
        ]

    def __str__(self):
        return f'Назначение от {self.created_at} для {self.medical_card_entry}'


class PrescriptionMedication(models.Model):
    """Промежуточная модель для назначения препаратов."""
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        verbose_name='Назначение',
        related_name='prescription_medications'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT,
        verbose_name='Препарат',
        help_text='Лекарственное средство',
        related_name='medications'
    )
    dosage = models.CharField(
        max_length=100,
        verbose_name='Дозировка',
        help_text='Количество препарата на прием (в мг, мл и т.д.)'
    )
    frequency = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Частота приема',
        help_text='Пример: 3 раза в день, каждые 8 часов'
    )
    duration = models.CharField(
        max_length=100,
        verbose_name='Продолжительность',
        help_text='Пример: 7 дней, до окончания симптомов'
    )
    individual_notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Особые указания',
        help_text='Способ применения и дополнительные условия'
    )

    class Meta:
        verbose_name = 'Назначенный препарат'
        verbose_name_plural = 'Назначенные препараты'
        indexes = [
            models.Index(fields=['prescription'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['prescription', 'medication'],
                name='prescription_medication'
            )
        ]

    def __str__(self):
        return f'{self.medication_id} - ({self.dosage})'

    def clean(self):
        super().clean()
        if not self.dosage:
            raise ValidationError({
                'dosage': 'Обязательное поле'
            })
