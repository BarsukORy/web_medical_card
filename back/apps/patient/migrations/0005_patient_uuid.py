# Generated by Django 5.1.3 on 2025-04-02 12:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_patient_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Уникальный идентификатор', unique=True, verbose_name='Уникальный идентификатор'),
        ),
    ]
