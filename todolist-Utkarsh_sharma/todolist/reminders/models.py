from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Reminder(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    creator = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')