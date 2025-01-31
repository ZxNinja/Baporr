# Generated by Django 5.1.4 on 2025-01-29 06:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_tap_delete_sharer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tap',
            constraint=models.UniqueConstraint(fields=('accounts', 'artwork'), name='unique_tap'),
        ),
    ]
