from django.contrib import admin
from .models import Artist, Artwork, Vote, Leaderboard, Tap


# Inline for artworks related to an artist
class ArtworkInline(admin.TabularInline):
    model = Artwork
    extra = 1


# Register the default User model in the admin

# Admin for Artist
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'user', 'artist_bio')
    inlines = [ArtworkInline]


# Admin for Artwork
@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('artwork_title', 'artist', 'artwork_votes', 'artwork_taps')
    list_filter = ('artist',)
    search_fields = ('artwork_title',)


# Admin for Vote
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('accounts', 'artwork', 'vote_timestamp')
    list_filter = ('vote_timestamp',)
    search_fields = ('accounts__username', 'artwork__artwork_title')

    def save_model(self, request, obj, form, change):
        """Ensure that artists cannot vote for their own artworks."""
        if obj.artwork.artist.user == obj.accounts:
            raise admin.ValidationError("Artists cannot vote for their own artworks.")
        super().save_model(request, obj, form, change)


# Admin for Leaderboard
@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('artwork_title', 'artist', 'votes', 'taps', 'popularity_score', 'last_updated')
    list_filter = ('artist',)
    search_fields = ('artwork_title', 'artist__artist_name')
    ordering = ('rank',)
    readonly_fields = ('popularity_score', 'last_updated')


# Admin for Tap (Updated to handle unlimited taps)
@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    list_display = ('accounts', 'artwork', 'tap_timestamp')
    list_filter = ('tap_timestamp',)
    search_fields = ('accounts__username', 'artwork__artwork_title')
