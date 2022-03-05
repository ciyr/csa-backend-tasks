from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('new/', views.NewReminderView.as_view(), name='new_reminder'),
    path('<int:pk>/', views.ReminderView.as_view(), name='reminder'),
    path('<int:pk>/complete/', views.CompleteView, name='completed'),
    path('<int:pk>/edit/', views.EditReminderView.as_view(), name='edit_reminder'),
    path('<int:pk>/delete/', views.DeleteReminderView.as_view(), name='delete_reminder'),
]