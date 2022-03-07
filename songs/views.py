import os
import random
from pathlib import Path
from .models import *
from urllib import request
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.conf import settings
from django.views.generic import DetailView, CreateView, DeleteView,ListView,UpdateView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings

def generate_random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    return p

def get_jwt_with_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    #print(token)
    return token

@csrf_exempt
@api_view(['POST'])
def auth(request):
    try:
        id_token = request.data["id_token"]
    except KeyError:
        return Response(
            {"error": "No id_token provided"}, status=status.HTTP_403_FORBIDDEN
        )

    id_info = googleIdToken.verify_oauth2_token(
        id_token, google_requests.Request())
    if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response(
            {"error": "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN
        )
    email = id_info["email"]
    username, domain = email.split('@')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create(username = username, first_name = id_info["given_name"], last_name = id_info["family_name"])
        user.set_password(generate_random_password())
        user.save()
    token = get_jwt_with_user(user)
    return Response({"JWT":token})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect('auth')


class SongList(generics.GenericAPIView, LoginRequiredMixin):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("auth")
        song_serialized = SongSerializer(Song.objects.all(),many=True)
        return Response(song_serialized.data) 


class SongDetails(generics.GenericAPIView ,LoginRequiredMixin):
    def get(self, request ,pk ,*args, **kwargs):
        song = Song.objects.get(id = pk)

        song_serialized = SongSerializer(song)
        return Response(song_serialized.data) 

    def post(self,request,pk):
        action = request.data["action"].strip().lower()
        song = Song.objects.get(id = pk)
        if action == "like":
            like_user,created = LikeORDislike.objects.get_or_create(song = song,liked_by = request.user)
            if created:
                like_user.status = '1'
                return Response({"message":"Song liked."})
            else:
                like_user.status = '1'
                return Response({"message":"Song liked."})
        elif action == 'dislike':
            like_user,created = LikeORDislike.objects.get_or_create(song = song,liked_by = request.user)
            if created:
                like_user.status = '0'
                return Response({"message":"Song disliked."})
            else:
                like_user.status = '0'
                return Response({"message":"Song disliked."})
        if action == 'play':
            song.times_played += 1
            song.save()
            return Response({"message":"Song is being is played."})

class UserPlayList(generics.GenericAPIView,LoginRequiredMixin):
    def get(self, request):
        pl = Playlist.objects.filter(user = request.user)
        if len(pl) == 0:
            return Response({"error":"You dont have any playlist."})
        else:
            pl_serialized = PlayListSerializer(pl, many = True)
            return Response(pl_serialized.data) 

class CreatePlayList(generics.GenericAPIView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        name = request.data["name"]
        songs_id = request.data["songs"]
        user = request.user
        playlist = Playlist.objects.create(name = name,user = user)
        for song_id in songs_id:
            songs = Song.objects.get(id = song_id)
            playlist.songs.add(songs)
            playlist.save()
        pl_serialized = PlayListSerializer(playlist)
        return Response(pl_serialized.data) 

class PlaylistDetails(LoginRequiredMixin, generics.GenericAPIView):

    def get(self, request, pk, *args, **kwargs):
        playlist = Playlist.objects.get(id = pk)
        pl_serialized = PlayListSerializer(playlist)
        return Response(pl_serialized.data) 

class DeletePlayList(DeleteView):
    
    def post(self, request,pk,*args, **kwargs):
        playlist = Playlist.objects.get(id = pk)
        if playlist.user != request.user:
            return Response({"error" : "unauthorized access"})
        return Response({"message":"Playlist successfully deleted"})

class AddSongToPlayList(generics.GenericAPIView, LoginRequiredMixin):
    def post(self, request,pk ,*args, **kwargs):
        playlist = Playlist.objects.get(id = pk)
        song_id = request.data["song_id"]
        song = Song.objects.get(id = song_id)

        if playlist.user != request.user:
            return Response({"error" : "unauthorized access"})

        playlist.songs.add(song)
        playlist.save()
        return Response({"message":"Playlist updated successfully."})



