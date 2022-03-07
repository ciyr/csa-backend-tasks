from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('home/',SongList.as_view(),name = "home"),
    path('song/<int:pk>',SongDetails.as_view(),name = "song-detail"),
    path('playlists/',UserPlayList.as_view(),name = "user-playlist"),
    path('playlists_create/',CreatePlayList.as_view(),name = "playlist-create"),
    path('song/<int:pk>',SongDetails.as_view(),name = "song-detail"),
    path('playlist/<int:pk>',PlaylistDetails.as_view(),name = "playlist-detail"),
    path('playlist_delete/<int:pk>',DeletePlayList.as_view(),name = "playlist-delete"),
    path('playlist_addsong/<int:pk>',AddSongToPlayList.as_view(),name = "playlist-add-song"),
]