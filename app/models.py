from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Artist(models.Model):
    artist_name = models.CharField(max_length=255)
    artist_bio = models.TextField()
    artist_profile_picture = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)

    def __str__(self):
        return self.artist_name

    @property
    def total_votes(self):
        return self.artworks.aggregate(total_votes=Count('votes'))['total_votes'] or 0


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

    def __str__(self):
        return f"Leaderboard - {self.artist.artist_name}: Rank {self.rank}"

    @classmethod
    def get_leaderboard(cls):
        artists = Artist.objects.annotate(total_votes=Count('artworks__votes')).order_by('-total_votes')

        leaderboard = []
        rank = 1
        for artist in artists:
            leaderboard.append({
                'rank': rank,
                'artist_name': artist.artist_name,
                'total_votes': artist.total_votes,
            })
            rank += 1
        return leaderboard


class Sharer(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="shares")
    sharer_name = models.CharField(max_length=255)
    share_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shared by {self.sharer_name} on {self.artwork.artwork_title}"
