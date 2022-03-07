from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Song)
admin.site.register(Singer)
admin.site.register(Like)
admin.site.register(Playlist)