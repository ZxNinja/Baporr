# Generated by Django 5.1.4 on 2025-01-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_tap_unique_tap_remove_tap_tap_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaderboard',
            old_name='votes',
            new_name='total_taps',
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]
