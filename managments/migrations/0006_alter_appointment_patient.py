# Generated by Django 5.1.7 on 2025-03-13 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managments', '0005_alter_patient_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managments.patient'),
        ),
    ]
