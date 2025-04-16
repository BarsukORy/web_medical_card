# Generated by Django 5.1.3 on 2025-03-09 21:36

import apps.patient.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patient_options_alter_patient_actual_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.ImageField(help_text='Фотография пациента для распознавания', upload_to=apps.patient.models.patient_photo_path, verbose_name='Фотография'),
        ),
    ]
