import os
from pathlib import Path
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.conf import settings
from django.views.generic import DetailView, CreateView, DeleteView,ListView,UpdateView
from .models import *
from rest_framework.views import APIView
from django.core.files import File
# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request,"spotify/login.html")


class SongsListView(ListView,LoginRequiredMixin):
    model= Song
    template_name = 'spotify/home.html'
    context_object_name='songs'


class SongDetails(APIView,LoginRequiredMixin):


    def get(self, request, *args, **kwargs):
        song = Song.objects.filter(id=kwargs['pk'])[0]
        liked = False
        if Like.objects.filter(song = song,liked_by=self.request.user).exists():
            liked = True
        return  render(request,template_name="spotify/song.html",context={"song":song,"liked":liked})

    def post(self,request,pk):
        like = request.POST.get("like",None)
        play = request.POST.get("play", None)
        dislike = request.POST.get("dislike",None)
        song = Song.objects.filter(id=pk)[0]
        if like:
            like_user,created = Like.objects.get_or_create(song = song,liked_by = self.request.user)
            if created:
                messages.info(request,"Song liked")
            else:
                messages.error(request, "You have already liked the song")
        elif dislike:
            like_user = Like.objects.filter(song=song, liked_by=self.request.user)
            if not like_user.exists():
                messages.error(request, "You have already disliked the song")
                return redirect("../song/" + str(pk))
            like_user.delete()
            messages.info(request, "Song disliked")
        if play:
            song.times_played += 1
            song.save()
            messages.info(request, "Song is being played")
            p = Path(settings.MEDIA_ROOT  + "/" + song.lyrics.url)
            with open(p) as f:
                lines = []
                for line in f:
                    lines.append(line)
            return render(request,'spotify/play_song.html',context={"audio":song.song,"lyrics":lines})
        return redirect("../song/"+str(pk))

class UserPlaylistListView(ListView,LoginRequiredMixin):
        model = Playlist
        template_name = 'spotify/playlists.html'
        context_object_name = 'playlists'
        def get_queryset(self):
            return self.model.objects.filter(user = self.request.user)
        


class UserPlaylistCreateView(CreateView):
    model = Playlist
    fields = ['name','songs']
    template_name = 'spotify/playlist_create.html'

    def form_valid(self, form):
        form.instance.writer=self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        songs_id = request.POST.getlist("songs")
        user = self.request.user
        playlist = Playlist.objects.create(name = name,user = user)
        songs = Song.objects.filter(id__in = songs_id)
        playlist.songs.set(songs)
        playlist.save()
        return redirect("playlist-list")

class PlaylistDetails(APIView,LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        playlist = Playlist.objects.filter(id=kwargs['pk'])[0]
        return  render(request,template_name="spotify/playlist_details.html",context={"playlist":playlist})

class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = 'spotify/playlist_delete.html'
    context_object_name = 'playlist'
    success_url = '/spotify/playlists/'

class PlaylistSongAddView(UpdateView):
    model = Playlist
    template_name = 'spotify/playlist_songadd.html'
    context_object_name = 'playlist'
    success_url = '/spotify/playlists/'
    fields = ['songs',]



