# Generated by Django 5.1.3 on 2025-03-08 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('registrar', 'Registrar'), ('admin', 'Admin')], help_text='Роль пользователя в системе', max_length=10, verbose_name='Роль'),
        ),
    ]
