from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    deadline=models.DateTimeField(default=timezone.now)
    task_image = models.ImageField(
        null=True, blank=True, upload_to='task_pics')
    task_done=models.BooleanField(default=False)
    
    def __str__(self):
        return self.task

    def get_absolute_url(self):
        return reverse("todo:task-detail", kwargs={"pk": self.pk})