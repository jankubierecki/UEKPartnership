# Generated by Django 2.0.6 on 2018-10-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partnerships', '0006_auto_20180915_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnership',
            name='last_contact_date',
            field=models.DateField(verbose_name='Data ostatniego kontaktu'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='start_date',
            field=models.DateField(verbose_name='Data nawiązania Współpracy'),
        ),
    ]
