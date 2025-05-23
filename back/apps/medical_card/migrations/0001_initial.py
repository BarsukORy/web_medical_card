# Generated by Django 5.1.3 on 2025-03-02 14:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog_medical_data', '0001_initial'),
        ('med_personal', '0001_initial'),
        ('medical_hub', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('O+', 'O (I) Rh+'), ('O-', 'O (I) Rh-'), ('A+', 'A (II) Rh+'), ('A-', 'A (II) Rh-'), ('B+', 'B (III) Rh+'), ('B-', 'B (III) Rh-'), ('AB+', 'AB (IV) Rh+'), ('AB-', 'AB (IV) Rh-')], help_text='Полная группа крови с резус-фактором', max_length=6, verbose_name='Группа крови')),
                ('allergies', models.TextField(blank=True, default='', help_text='Список аллергенов и реакций', verbose_name='Аллергии')),
                ('chronic_diseases', models.TextField(blank=True, default='', help_text='Список хронических заболеваний', verbose_name='Хронические заболевания')),
                ('attachment_hospital', models.ForeignKey(blank=True, help_text='Основное медучреждение для пациента', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospital_medical_card', to='medical_hub.hospital', verbose_name='Прикрепленная больница')),
                ('patient', models.OneToOneField(help_text='Привязанный пациент', on_delete=django.db.models.deletion.PROTECT, related_name='patient_medical_card', to='patient.patient', verbose_name='Пациент')),
            ],
            options={
                'verbose_name': 'Медицинская карта',
                'verbose_name_plural': 'Медицинские карты',
            },
        ),
        migrations.CreateModel(
            name='MedicalCardEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField(help_text='Фактическая дата приема пациента', verbose_name='Дата визита')),
                ('custom_diagnosis', models.CharField(blank=True, default='', help_text='Уточненный или дополнительный диагноз', max_length=300, verbose_name='Индивидуальный диагноз')),
                ('treatment', models.TextField(blank=True, default='', help_text='Стандартизированный протокол лечения', verbose_name='План лечения')),
                ('custom_treatment', models.CharField(blank=True, default='', help_text='Особые назначения и рекомендации', max_length=300, verbose_name='Индивидуальное лечение')),
                ('notes', models.TextField(blank=True, default='', help_text='Дополнительные комментарии и наблюдения', verbose_name='Примечания')),
                ('diagnosis', models.ForeignKey(blank=True, help_text='Диагноз из классификатора заболеваний', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='diagnosis_entries', to='catalog_medical_data.disease', verbose_name='Основной диагноз')),
                ('doctor', models.ForeignKey(blank=True, help_text='Ответственный медицинский специалист', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_entries', to='med_personal.doctor', verbose_name='Лечащий врач')),
                ('hospital', models.ForeignKey(blank=True, help_text='Учреждение где проводился прием', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospital_entries', to='medical_hub.hospital', verbose_name='Мед учреждение')),
                ('medical_card', models.ForeignKey(help_text='Медицинская карта, для которой создается запись', on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='medical_card.medicalcard', verbose_name='Медицинская карта')),
            ],
            options={
                'verbose_name': 'Запись медкарты',
                'verbose_name_plural': 'Записи медкарт',
                'ordering': ['-visit_date'],
            },
        ),
        migrations.CreateModel(
            name='MedicalCardEntryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Файл, прикрепленный к записи медкарты', upload_to='medical_card_entries/files/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])], verbose_name='Файл медзаписи')),
                ('medical_card_entry', models.ForeignKey(help_text='Запись медицинской карты, к которой прикреплен файл', on_delete=django.db.models.deletion.CASCADE, related_name='files', to='medical_card.medicalcardentry', verbose_name='Запись медкарты')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administration_notes', models.TextField(blank=True, default='', help_text='Общие указания для всех препаратов', verbose_name='Особые указания')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('medical_card_entry', models.ForeignKey(help_text='Связанная медицинская запись', on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='medical_card.medicalcardentry', verbose_name='Запись в карте')),
            ],
            options={
                'verbose_name': 'Назначение',
                'verbose_name_plural': 'Назначения',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PrescriptionMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.CharField(help_text='Количество препарата на прием (в мг, мл и т.д.)', max_length=100, verbose_name='Дозировка')),
                ('frequency', models.CharField(blank=True, default='', help_text='Пример: 3 раза в день, каждые 8 часов', max_length=100, verbose_name='Частота приема')),
                ('duration', models.CharField(help_text='Пример: 7 дней, до окончания симптомов', max_length=100, verbose_name='Продолжительность')),
                ('individual_notes', models.TextField(blank=True, default='', help_text='Способ применения и дополнительные условия', verbose_name='Особые указания')),
                ('medication', models.ForeignKey(help_text='Лекарственное средство', on_delete=django.db.models.deletion.PROTECT, related_name='medications', to='catalog_medical_data.medication', verbose_name='Препарат')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_medications', to='medical_card.prescription', verbose_name='Назначение')),
            ],
            options={
                'verbose_name': 'Назначенный препарат',
                'verbose_name_plural': 'Назначенные препараты',
            },
        ),
        migrations.AddIndex(
            model_name='medicalcard',
            index=models.Index(fields=['blood_type'], name='medical_car_blood_t_7daef3_idx'),
        ),
        migrations.AddConstraint(
            model_name='medicalcardentry',
            constraint=models.CheckConstraint(condition=models.Q(('diagnosis__isnull', False), ('custom_diagnosis__isnull', False), _connector='OR'), name='check_diagnosis_required'),
        ),
        migrations.AddConstraint(
            model_name='medicalcardentry',
            constraint=models.CheckConstraint(condition=models.Q(('diagnosis__isnull', False), ('custom_diagnosis__isnull', False), _negated=True), name='check_single_diagnosis_required'),
        ),
        migrations.AddConstraint(
            model_name='prescriptionmedication',
            constraint=models.UniqueConstraint(fields=('prescription', 'medication'), name='prescription_medication'),
        ),
    ]
