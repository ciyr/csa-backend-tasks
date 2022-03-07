from django.shortcuts import render
from .models import Reminders


def reminder_list(request):
    reminder = Reminders.objects.all()
    return render(request, 'RemindersWebApp/reminder_list.html', {'reminder':reminder})
