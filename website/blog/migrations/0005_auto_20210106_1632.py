# Generated by Django 3.1.5 on 2021-01-06 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpage_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpage',
            options={'ordering': ['-date']},
        ),
    ]
