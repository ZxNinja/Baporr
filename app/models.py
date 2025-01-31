from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist_profile", null=True, blank=True)
    artist_name = models.CharField(max_length=255)
    artist_bio = models.TextField()
    artist_profile_picture = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)

    def __str__(self):
        return self.artist_name

    @property
    def total_votes(self):
        return self.artworks.aggregate(total_votes=Count('votes'))['total_votes'] or 0

    @property
    def total_taps(self):
        return self.artworks.aggregate(total_taps=Count('taps'))['total_taps'] or 0


class Artwork(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artworks")
    artwork_title = models.CharField(max_length=255)
    artwork_description = models.TextField()
    artwork_image = models.ImageField(upload_to='artworks/', blank=True, null=True)

    def __str__(self):
        return self.artwork_title

    @property
    def artwork_votes(self):
        return self.votes.count()

    @property
    def artwork_taps(self):
        return self.taps.count()  # Count the number of taps for the artwork


class Vote(models.Model):
    accounts = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="votes")
    vote_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accounts', 'artwork'], name='unique_vote')
        ]

    def __str__(self):
        return f"Vote by {self.accounts.username} on {self.artwork.artwork_title}"


class Leaderboard(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE, related_name="leaderboard")
    rank = models.PositiveIntegerField()
    votes = models.IntegerField(default=0)
    taps = models.IntegerField(default=0)
    artwork_title = models.CharField(max_length=255, blank=True, null=True)
    artwork_description = models.TextField(blank=True, null=True)
    artwork_image = models.ImageField(upload_to='leaderboard_artworks/', blank=True, null=True)
    popularity_score = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leaderboard - {self.artist.artist_name}: Rank {self.rank}"

    def update_popularity_score(self):

        self.popularity_score = (self.votes * 1.0) + (self.taps * 0.5)
        self.save()

    @classmethod
    def update_leaderboard(cls):

        artists = Artist.objects.annotate(
            total_votes=Count('artworks__votes'),
            total_taps=Count('artworks__taps')
        ).order_by('-total_votes', '-total_taps')


        cls.objects.all().delete()

        rank = 1
        for artist in artists:

            most_popular_artwork = artist.artworks.annotate(
                total_votes=Count('votes'),
                total_taps=Count('taps')
            ).order_by('-total_votes', '-total_taps').first()


            assigned_rank = rank if artist.total_votes > 0 or artist.total_taps > 0 else 0


            leaderboard_entry = cls(
                artist=artist,
                rank=assigned_rank,
                votes=artist.total_votes,
                taps=artist.total_taps,
                artwork_title=most_popular_artwork.artwork_title if most_popular_artwork else None,
                artwork_description=most_popular_artwork.artwork_description if most_popular_artwork else None,
                artwork_image=most_popular_artwork.artwork_image if most_popular_artwork else None,
            )
            leaderboard_entry.update_popularity_score()
            leaderboard_entry.save()

            if artist.total_votes > 0 or artist.total_taps > 0:
                rank += 1



class Tap(models.Model):
    accounts = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taps")
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="taps")
    tap_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tap by {self.accounts.username} on {self.artwork.artwork_title} at {self.tap_timestamp}"
