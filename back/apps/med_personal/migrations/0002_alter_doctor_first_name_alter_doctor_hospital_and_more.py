# Generated by Django 5.1.3 on 2025-03-08 21:36

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_personal', '0001_initial'),
        ('medical_hub', '0002_alter_hospital_address_alter_hospital_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='first_name',
            field=models.CharField(help_text='Имя сотрудника', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(blank=True, help_text='Мед учреждение, к которому прикреплен врач', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='medical_hub.hospital', verbose_name='Мед учереждение'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='last_name',
            field=models.CharField(help_text='Фамилия сотрудника', max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='middle_name',
            field=models.CharField(blank=True, default='', help_text='Отчество сотрудника (не обязательно)', max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Уникальный телефон формата +7**********', max_length=128, region='RU', unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.ManyToManyField(help_text='Специализации врача', related_name='doctors_specializations', to='medical_hub.specialty', verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(help_text='Связанный пользователь', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='first_name',
            field=models.CharField(help_text='Имя сотрудника', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='hospital',
            field=models.ForeignKey(blank=True, help_text='Мед учреждение, к которому прикреплен регистратор', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrars', to='medical_hub.hospital', verbose_name='Мед учереждение'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='last_name',
            field=models.CharField(help_text='Фамилия сотрудника', max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='middle_name',
            field=models.CharField(blank=True, default='', help_text='Отчество сотрудника (не обязательно)', max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Уникальный телефон формата +7**********', max_length=128, region='RU', unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='user',
            field=models.OneToOneField(help_text='Связанный пользователь', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
