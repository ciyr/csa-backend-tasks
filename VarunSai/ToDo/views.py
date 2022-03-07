from multiprocessing import context
from typing import List
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import(
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
) 
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'ToDo/home.html' #To which template should the view map to.
    context_object_name = 'tasks' #To use 'tasks' instead of 'objects'
    ordering = ['-date_posted']  #To order in descending order of date.

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'is_done'] #All the fields to be displayed in the create view
    
    #To check if the form is valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) #super() is used since we modify the default behaviour of the class

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'ToDo/task-update.html'
    fields = ['title', 'description', 'due_date', 'is_done']
    
    #To check if the form is valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) #super() is used since we modify the default behaviour of the class

    #To check if the task authoor is the user logged in
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/task' #URL to redirect after the delete is done 

    #To check if the task authoor is the user logged in
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False

class TaskListTodayView(ListView):
    model = Task
    template_name = 'ToDo/task_today.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']

class TaskListLateView(ListView):
    model = Task
    template_name = 'ToDo/task_late.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']