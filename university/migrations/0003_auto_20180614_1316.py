# Generated by Django 2.0.5 on 2018-06-14 11:16

from django.db import migrations, models
import university.validators


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20180614_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universitycontactperson',
            name='email',
            field=models.EmailField(blank=True, help_text='Tylko z domeną UEK', max_length=50, null=True, validators=[university.validators.email_validation], verbose_name='Email'),
        ),
    ]