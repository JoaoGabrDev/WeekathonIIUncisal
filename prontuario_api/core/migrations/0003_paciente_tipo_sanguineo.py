# Generated by Django 5.2.1 on 2025-05-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_paciente_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='tipo_sanguineo',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, null=True),
        ),
    ]
