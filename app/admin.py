from django.contrib import admin
from .models import Artist, Artwork, Vote, Leaderboard, Sharer

# Inline for artworks related to an artist
class ArtworkInline(admin.TabularInline):
    model = Artwork
    extra = 1

# Admin for Artist
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'artist_bio')
    inlines = [ArtworkInline]

# Admin for Artwork
@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('artwork_title', 'artist', 'artwork_votes')
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
        if obj.artwork.artist.artist_name == obj.accounts.username:
            raise admin.ValidationError("Artists cannot vote for their own artworks.")
        super().save_model(request, obj, form, change)

# Admin for Leaderboard
@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('artist', 'rank', 'votes')
    list_editable = ('rank',)
    ordering = ('rank',)

# Admin for Sharer
@admin.register(Sharer)
class SharerAdmin(admin.ModelAdmin):
    list_display = ('sharer_name', 'artwork', 'share_timestamp')
    list_filter = ('share_timestamp',)
