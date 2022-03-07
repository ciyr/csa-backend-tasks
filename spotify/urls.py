from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('home/',SongsListView.as_view(),name = "home"),
    path('song/<int:pk>',SongDetails.as_view(),name = "song-detail"),
    path('playlists/',UserPlaylistListView.as_view(),name = "playlist-list"),
    path('playlists_create/',UserPlaylistCreateView.as_view(),name = "playlist-create"),
    path('song/<int:pk>',SongDetails.as_view(),name = "song-detail"),
    path('playlists/<int:pk>',PlaylistDetails.as_view(),name = "playlist-detail"),
    path('playlist_delete/<int:pk>',PlaylistDeleteView.as_view(),name = "playlist-delete"),
    path('playlist_addsong/<int:pk>',PlaylistSongAddView.as_view(),name = "playlist-add-song"),
]