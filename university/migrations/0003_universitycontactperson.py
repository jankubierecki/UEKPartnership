# Generated by Django 2.0.5 on 2018-05-23 17:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20180523_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Imię')),
                ('last_name', models.CharField(max_length=255, verbose_name='Nazwisko')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, validators=[django.core.validators.EmailValidator(whitelist=['@uek.krakow.pl'])], verbose_name='Email')),
                ('academic_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tytuł naukowy')),
            ],
            options={
                'verbose_name': 'Jednostka Współpracująca UEK',
                'verbose_name_plural': 'Jednostki Współpracująca UEK',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
