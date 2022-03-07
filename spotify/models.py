from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

SONG_TYPES = [
    ('album','album'),
    ('movie','movie')
]
def lyrics_path(instance, filename):
    return instance.name + "lyrics"
def audio_path(instance, filename):
    return instance.name + " audio.mp3"

class Song(models.Model):

    name = models.CharField(max_length=50)
    song_type = models.CharField(max_length=10,choices=SONG_TYPES)
    singers = models.ManyToManyField("Singer",related_name="songs")
    lyrics = models.FileField(upload_to=lyrics_path,null=True)
    song = models.FileField(upload_to=audio_path,null=True)
    times_played = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        all_singers = ""
        for singer in self.singers.all():
            all_singers += singer.name + ", "
        return f'{self.name} by {all_singers}'

    @property
    def total_likes(self):
        return Like.objects.filter(song = self).count()

class Singer(models.Model):

    name = models.CharField(max_length=50)
    country = models.CharField(max_length=20)

    def __str__(self):
        return  self.name


class Like(models.Model):

    song = models.ForeignKey(Song,related_name="likes",on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User,related_name='song_like',on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return  f'{self.song.name} liked by {self.liked_by.username}'

class Playlist(models.Model):

    name = models.CharField(max_length=20,blank=True,null=True)
    user = models.ForeignKey(User,related_name="playlists",on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song,related_name="playlists",null=True,blank=True)

    def __str__(self):
        return self.name