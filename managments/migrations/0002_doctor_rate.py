# Generated by Django 5.1.7 on 2025-03-12 21:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='rate',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='التقييم'),
            preserve_default=False,
        ),
    ]
