

from django.urls import path
from .views import (HomePageView, AboutPageView, ArtistListView, ArtistDetailView,
                    ArtistCreateView, ArtistUpdateView, ArtistDeleteView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),

path('view', ArtistListView.as_view(), name='artist-list'),
    path('<int:pk>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('create/', ArtistCreateView.as_view(), name='artist-create'),
    path('<int:pk>/update/', ArtistUpdateView.as_view(), name='artist-update'),
    path('<int:pk>/delete/', ArtistDeleteView.as_view(), name='artist-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
