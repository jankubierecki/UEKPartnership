# Generated by Django 2.0.6 on 2018-09-10 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='instituteunittouniversitycontactperson',
            unique_together={('institute_unit', 'university_contact_person')},
        ),
    ]