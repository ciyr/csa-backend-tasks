from django.db import models


class Reminders(models.Model):
    reminder_name = models.CharField(max_length=200)
    reminder_time = models.DateTimeField(blank=True, null=True)
    reminder_Completed = models.BooleanField(default=False)

    def __str__(self):
        return self.reminder_name
