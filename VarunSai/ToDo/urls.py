from django.urls import path, include

from ToDo.models import Task
from .views import(
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListTodayView,
    TaskListLateView
) 

urlpatterns = [
    path('task/', TaskListView.as_view(), name='home'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/today/', TaskListTodayView.as_view(), name='task-today'),
    path('task/late/', TaskListLateView.as_view(), name='task-late'),
]