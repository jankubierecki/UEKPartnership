# Generated by Django 2.0.5 on 2018-06-14 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partnerships', '0011_auto_20180614_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnershipLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')),
                ('description', models.TextField(verbose_name='Opis')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_log_entries', to=settings.AUTH_USER_MODEL, verbose_name='Utworzono przez')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_log_entries', to=settings.AUTH_USER_MODEL, verbose_name='Zaktualizowano przez')),
            ],
            options={
                'verbose_name': 'Notatka',
                'verbose_name_plural': 'Notatki',
                'ordering': ['updated_by'],
            },
        ),
    ]