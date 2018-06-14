# Generated by Django 2.0.5 on 2018-06-14 12:23

import company.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20180614_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='nip_code',
            field=models.CharField(default='numer nip', max_length=10, validators=[company.validators.validate_nip], verbose_name='Numer NIP'),
        ),
    ]
