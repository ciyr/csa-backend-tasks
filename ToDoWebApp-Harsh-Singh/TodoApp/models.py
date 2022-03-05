from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
