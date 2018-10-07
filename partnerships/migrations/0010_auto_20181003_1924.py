# Generated by Django 2.0.6 on 2018-10-03 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partnerships', '0009_auto_20181003_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='company',
        ),
        migrations.AlterField(
            model_name='contract',
            name='company_contact_persons',
            field=models.ManyToManyField(help_text='Osoby do kontaktu firmy związane z tą umową', to='company.CompanyContactPerson', verbose_name='Osoby do kontaktu firmy'),
        ),
    ]