from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

SONG_TYPES = [
    ('album','album'),
    ('movie','movie')
]
STATUS = [
    ('0','Like'),
    ('1','Dislike')
]

def lyrics_path(instance, filename):
    return instance.name + "lyrics"
def audio_path(instance, filename):
    return instance.name + " audio.mp3"

class Song(models.Model):
    name = models.CharField(max_length=50)
    song_type = models.CharField(max_length=10,choices=SONG_TYPES)
    author = models.ForeignKey("Author",related_name="songs", on_delete=models.CASCADE)
    lyrics = models.FileField(upload_to='song/lyrics/',null=True)
    song = models.FileField(upload_to='song/audio/',null=True)
    times_played = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return f'{self.name} by {self.author.name}'

    @property
    def likes(self):
        return self.like_song.count()

class Author(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=20)

    def __str__(self):
        return  self.name


class LikeORDislike(models.Model):
    song = models.ForeignKey(Song,related_name="like_song",on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User,related_name='like_liked_by',on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=3, choices= STATUS, default='1')

    def __str__(self):
        return  f'{self.song.name} liked by {self.liked_by.username}'

class Playlist(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    user = models.ForeignKey(User,related_name="playlist_user",on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song,related_name="playlist_songs",null=True,blank=True)

    def __str__(self):
        return self.name