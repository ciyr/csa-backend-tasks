from multiprocessing import AuthenticationError
from django.contrib import admin
from .models import *

admin.site.register(Song)
admin.site.register(Author)
admin.site.register(LikeORDislike)
admin.site.register(Playlist)