# Generated by Django 5.1.6 on 2025-03-13 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weathers', '0016_alter_cityslug_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cityslug',
            name='slug',
            field=models.SlugField(),
        ),
    ]
