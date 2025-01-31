from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Artist, Artwork, Tap, Vote, Leaderboard
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


def search(request):
    query = request.GET.get('q')
    if query:
        # Search across multiple models
        artists = Artist.objects.filter(Q(artist_name__icontains=query) | Q(artist_bio__icontains=query))
        artworks = Artwork.objects.filter(Q(artwork_title__icontains=query) | Q(artwork_description__icontains=query))
        taps = Tap.objects.filter(artwork__artwork_title__icontains=query)
        votes = Vote.objects.filter(artwork__artwork_title__icontains=query)
        leaderboards = Leaderboard.objects.filter(
            Q(artist__artist_name__icontains=query) | Q(artwork_title__icontains=query))

        context = {
            'query': query,
            'artists': artists,
            'artworks': artworks,
            'taps': taps,
            'votes': votes,
            'leaderboards': leaderboards,
        }
        return render(request, 'app/search_results.html', context)
    else:
        return render(request, 'app/search_results.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')


# Home and About Views
class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'


# Artist Views
class ArtistListView(ListView):
    model = Artist
    template_name = 'app/artist_list.html'
    context_object_name = 'artists'


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'app/artist_detail.html'
    context_object_name = 'artist'


@method_decorator(login_required, name='dispatch')
class ArtistCreateView(CreateView):
    model = Artist
    fields = ['artist_name', 'artist_bio', 'artist_profile_picture']
    template_name = 'app/artist_form.html'
    success_url = reverse_lazy('artist-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArtistUpdateView(UpdateView):
    model = Artist
    fields = ['artist_name', 'artist_bio', 'artist_profile_picture']
    template_name = 'app/artist_form.html'
    success_url = reverse_lazy('artist-list')


class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = 'app/artist_confirm_delete.html'
    success_url = reverse_lazy('artist-list')


# Artwork Views
class ArtworkListView(ListView):
    model = Artwork
    template_name = 'app/artwork_list.html'
    context_object_name = 'artworks'


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'app/artwork_detail.html'
    context_object_name = 'artwork'


class ArtworkCreateView(CreateView):
    model = Artwork
    fields = ['artist', 'artwork_title', 'artwork_description', 'artwork_image']
    template_name = 'app/artwork_form.html'
    success_url = reverse_lazy('artwork-list')


class ArtworkUpdateView(UpdateView):
    model = Artwork
    fields = ['artist', 'artwork_title', 'artwork_description', 'artwork_image']
    template_name = 'app/artwork_form.html'
    success_url = reverse_lazy('artwork-list')


class ArtworkDeleteView(DeleteView):
    model = Artwork
    template_name = 'app/artwork_confirm_delete.html'
    success_url = reverse_lazy('artwork-list')


# Tap Views
class TapListView(ListView):
    model = Tap
    template_name = 'app/tap_list.html'
    context_object_name = 'taps'


class TapDetailView(DetailView):
    model = Tap
    template_name = 'app/tap_detail.html'
    context_object_name = 'tap'


class TapCreateView(CreateView):
    model = Tap
    fields = ['accounts', 'artwork']
    template_name = 'app/tap_form.html'
    success_url = reverse_lazy('tap-list')


class TapUpdateView(UpdateView):
    model = Tap
    fields = ['accounts', 'artwork']
    template_name = 'app/tap_form.html'
    success_url = reverse_lazy('tap-list')


class TapDeleteView(DeleteView):
    model = Tap
    template_name = 'app/tap_confirm_delete.html'
    success_url = reverse_lazy('tap-list')


# Vote Views
class VoteListView(ListView):
    model = Vote
    template_name = 'app/vote_list.html'
    context_object_name = 'votes'


class VoteDetailView(DetailView):
    model = Vote
    template_name = 'app/vote_detail.html'
    context_object_name = 'vote'


class VoteCreateView(CreateView):
    model = Vote
    fields = ['accounts', 'artwork']
    template_name = 'app/vote_form.html'
    success_url = reverse_lazy('vote-list')


class VoteUpdateView(UpdateView):
    model = Vote
    fields = ['accounts', 'artwork']
    template_name = 'app/vote_form.html'
    success_url = reverse_lazy('vote-list')


class VoteDeleteView(DeleteView):
    model = Vote
    template_name = 'app/vote_confirm_delete.html'
    success_url = reverse_lazy('vote-list')


# Leaderboard Views
class LeaderboardListView(ListView):
    model = Leaderboard
    template_name = 'app/leaderboard_list.html'
    context_object_name = 'leaderboards'

    def get_queryset(self):
        return Leaderboard.objects.all().order_by('rank')


class LeaderboardDetailView(DetailView):
    model = Leaderboard
    template_name = 'app/leaderboard_detail.html'
    context_object_name = 'leaderboard'


class LeaderboardCreateView(CreateView):
    model = Leaderboard
    fields = ['artist', 'rank', 'votes', 'taps', 'artwork_title', 'artwork_description', 'artwork_image']
    template_name = 'app/leaderboard_form.html'
    success_url = reverse_lazy('leaderboard-list')


class LeaderboardUpdateView(UpdateView):
    model = Leaderboard
    fields = ['artist', 'rank', 'votes', 'taps', 'artwork_title', 'artwork_description', 'artwork_image']
    template_name = 'app/leaderboard_form.html'
    success_url = reverse_lazy('leaderboard-list')


class LeaderboardDeleteView(DeleteView):
    model = Leaderboard
    template_name = 'app/leaderboard_confirm_delete.html'
    success_url = reverse_lazy('leaderboard-list')


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('artist-create')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})
