# Generated by Django 5.1.4 on 2025-01-01 05:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=255)),
                ('artist_bio', models.TextField()),
                ('artist_profile_picture', models.ImageField(blank=True, null=True, upload_to='artist_profiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artwork_title', models.CharField(max_length=255)),
                ('artwork_description', models.TextField()),
                ('artwork_image', models.ImageField(blank=True, null=True, upload_to='artworks/')),
                ('artwork_votes', models.IntegerField(default=0)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='app.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField()),
                ('votes', models.IntegerField()),
                ('artist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard', to='app.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Sharer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharer_name', models.CharField(max_length=255)),
                ('share_timestamp', models.DateTimeField(auto_now_add=True)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='app.artwork')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_timestamp', models.DateTimeField(auto_now_add=True)),
                ('accounts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='app.artwork')),
            ],
        ),
    ]
