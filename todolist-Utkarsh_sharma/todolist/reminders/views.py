from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Reminder

# Create your views here.
class HomeView(generic.ListView):
    model = Reminder
    template_name = 'reminders/home.html'
    context_object_name = 'reminders'
    ordering = ['-date_posted']

class NewReminderView(LoginRequiredMixin, generic.CreateView):
    model = Reminder
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class ReminderView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Reminder
    template_name = 'reminders/detail.html'
    context_object_name = 'reminder'

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.creator:
            return True
        return False

class EditReminderView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Reminder
    fields = ['title', 'body']

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.creator:
            return True
        return False

class DeleteReminderView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Reminder
    success_url = '/'

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.creator:
            return True
        return False

@login_required
def CompleteView(request, pk):
    reminder = Reminder.objects.filter(id=pk)

    if reminder.filter(completed=False):
        reminder.update(completed=True)

    else:
        reminder.update(completed=False)

    return HttpResponseRedirect(reverse('home'))

