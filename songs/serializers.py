from unicodedata import name
from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField()
    country = serializers.CharField()

class SongSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name =serializers.CharField()
    author = AuthorSerializer()
    song = serializers.URLField()
    song_type = serializers.CharField()
    times_played = serializers.IntegerField()
    lyrics = serializers.URLField()

class PlayListSerializer(serializers.Serializer):
    name =serializers.CharField()
    songs = SongSerializer(many = True)

        