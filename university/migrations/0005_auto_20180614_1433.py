# Generated by Django 2.0.5 on 2018-06-14 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0004_auto_20180614_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='university_faculty',
        ),
        migrations.AlterModelOptions(
            name='instituteunit',
            options={'ordering': ['name'], 'verbose_name': 'Jednostka Współpracująca UEK', 'verbose_name_plural': 'Jednostki Współpracujące UEK'},
        ),
        migrations.RemoveField(
            model_name='instituteunit',
            name='institute',
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
        migrations.DeleteModel(
            name='UniversityFaculty',
        ),
    ]