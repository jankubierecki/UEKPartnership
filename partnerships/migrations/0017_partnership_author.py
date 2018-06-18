# Generated by Django 2.0.5 on 2018-06-18 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partnerships', '0016_auto_20180618_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnership',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partnerships', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
    ]
