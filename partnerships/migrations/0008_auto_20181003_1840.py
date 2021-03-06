# Generated by Django 2.0.6 on 2018-10-03 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partnerships', '0007_auto_20181002_1729'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contracttocompanycontactperson',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='contracttocompanycontactperson',
            name='company_contact_person',
        ),
        migrations.RemoveField(
            model_name='contracttocompanycontactperson',
            name='contract',
        ),
        migrations.AlterUniqueTogether(
            name='contracttouniversitycontactperson',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='contracttouniversitycontactperson',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='contracttouniversitycontactperson',
            name='university_contact_person',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='company_contact_persons',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='university_contact_persons',
        ),
        migrations.DeleteModel(
            name='ContractToCompanyContactPerson',
        ),
        migrations.DeleteModel(
            name='ContractToUniversityContactPerson',
        ),
    ]
