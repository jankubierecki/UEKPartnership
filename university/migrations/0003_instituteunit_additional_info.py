# Generated by Django 2.0.6 on 2018-09-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20180910_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteunit',
            name='additional_info',
            field=models.TextField(blank=True, null=True, verbose_name='Dodatkowe Informacje'),
        ),
    ]
