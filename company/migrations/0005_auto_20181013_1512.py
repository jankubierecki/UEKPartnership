# Generated by Django 2.0.6 on 2018-10-13 13:12

import company.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20181002_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(help_text='Pod spodem pokażą się firmy o podobnej nazwie, które są już w systemie', max_length=255, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='company',
            name='nip_code',
            field=models.CharField(max_length=10, validators=[company.validators.validate_nip], verbose_name='Numer NIP'),
        ),
    ]
