# urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView  # Import LoginView and LogoutView
from .views import (
    HomePageView, AboutPageView, ArtistListView, ArtistDetailView,
    ArtistCreateView, ArtistUpdateView, ArtistDeleteView,
    ArtworkListView, ArtworkDetailView, ArtworkCreateView,
    ArtworkUpdateView, ArtworkDeleteView, TapListView, TapDetailView,
    TapCreateView, TapUpdateView, TapDeleteView, VoteListView, VoteDetailView,
    VoteCreateView, VoteUpdateView, VoteDeleteView, LeaderboardListView, LeaderboardDetailView,
    LeaderboardCreateView, LeaderboardUpdateView, LeaderboardDeleteView, RegisterView, search  # Import RegisterView
)
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('about/', login_required(AboutPageView.as_view()), name='about'),
    path('view', login_required(ArtistListView.as_view()), name='artist-list'),
    path('<int:pk>/', login_required(ArtistDetailView.as_view()), name='artist-detail'),
    path('create/', login_required(ArtistCreateView.as_view()), name='artist-create'),
    path('<int:pk>/update/', login_required(ArtistUpdateView.as_view()), name='artist-update'),
    path('<int:pk>/delete/', login_required(ArtistDeleteView.as_view()), name='artist-delete'),

    # Artwork URLs
    path('artworks/', login_required(ArtworkListView.as_view()), name='artwork-list'),
    path('artworks/<int:pk>/', login_required(ArtworkDetailView.as_view()), name='artwork-detail'),
    path('artworks/create/', login_required(ArtworkCreateView.as_view()), name='artwork-create'),
    path('artworks/<int:pk>/update/', login_required(ArtworkUpdateView.as_view()), name='artwork-update'),
    path('artworks/<int:pk>/delete/', login_required(ArtworkDeleteView.as_view()), name='artwork-delete'),

    # Tap URLs
    path('taps/', login_required(TapListView.as_view()), name='tap-list'),
    path('taps/<int:pk>/', login_required(TapDetailView.as_view()), name='tap-detail'),
    path('taps/create/', login_required(TapCreateView.as_view()), name='tap-create'),
    path('taps/<int:pk>/update/', login_required(TapUpdateView.as_view()), name='tap-update'),
    path('taps/<int:pk>/delete/', login_required(TapDeleteView.as_view()), name='tap-delete'),

    # Vote URLs
    path('votes/', login_required(VoteListView.as_view()), name='vote-list'),
    path('votes/<int:pk>/', login_required(VoteDetailView.as_view()), name='vote-detail'),
    path('votes/create/', login_required(VoteCreateView.as_view()), name='vote-create'),
    path('votes/<int:pk>/update/', login_required(VoteUpdateView.as_view()), name='vote-update'),
    path('votes/<int:pk>/delete/', login_required(VoteDeleteView.as_view()), name='vote-delete'),

    # Leaderboard URLs
    path('leaderboard/', login_required(LeaderboardListView.as_view()), name='leaderboard-list'),
    path('leaderboards/<int:pk>/', login_required(LeaderboardDetailView.as_view()), name='leaderboard-detail'),
    path('leaderboards/create/', login_required(LeaderboardCreateView.as_view()), name='leaderboard-create'),
    path('leaderboards/<int:pk>/update/', login_required(LeaderboardUpdateView.as_view()), name='leaderboard-update'),
    path('leaderboards/<int:pk>/delete/', login_required(LeaderboardDeleteView.as_view()), name='leaderboard-delete'),

    # Login and Register URLs (no login_required)
    # Other URLs
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='app/register.html'), name='register'),
    path('register/', views.register, name='register'),  # Registration URL
    path('search/', search, name='search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
