# Generated by Django 5.1.6 on 2025-03-11 19:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weathers', '0010_alter_cityslug_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='cityweathers',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cityweathers',
            name='wind_speed',
            field=models.FloatField(default=0),
        ),
    ]
