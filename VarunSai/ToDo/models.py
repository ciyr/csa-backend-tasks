from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#This class basicaly represents a database and its properties are the fields in the database.
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #Foreign key refers to the primary key of another table.
    is_done = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.now)

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})
   