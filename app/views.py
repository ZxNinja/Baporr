from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Artist

class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'


class ArtistListView(ListView):
    model = Artist
    template_name = 'app/artist_list.html'
    context_object_name = 'artists'

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'app/artist_detail.html'
    context_object_name = 'artist'

class ArtistCreateView(CreateView):
    model = Artist
    fields = ['artist_name', 'artist_bio', 'artist_profile_picture']
    template_name = 'app/artist_form.html'
    success_url = reverse_lazy('artist-list')

class ArtistUpdateView(UpdateView):
    model = Artist
    fields = ['artist_name', 'artist_bio', 'artist_profile_picture']
    template_name = 'app/artist_form.html'
    success_url = reverse_lazy('artist-list')

class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = 'app/artist_confirm_delete.html'
    success_url = reverse_lazy('artist-list')