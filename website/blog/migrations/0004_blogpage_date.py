# Generated by Django 3.1.5 on 2021-01-06 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210106_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
    ]
