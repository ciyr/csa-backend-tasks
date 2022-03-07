from django.forms import ModelForm
from .models import *
from django.forms import HiddenInput
from django import forms

class AddSongPlaylistForm(ModelForm):

    class Meta:
        model = Playlist
        fields = ['songs']

