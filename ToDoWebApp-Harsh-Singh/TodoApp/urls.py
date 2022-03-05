from django.urls import path
from .views import register, home_user, CreateTodo, EditTodo, DeleteTodo, ViewTodo
from django.contrib.auth.views import LoginView, LogoutView

app_name = "todo"

urlpatterns = [
    path('register', register, name='register'),
    path('login', LoginView.as_view(template_name='todoapp/login.html'), name='login'),
    path('home', home_user, name='home_user'),
    path('logout', LogoutView.as_view(template_name='todoapp/logout.html'), name='logout'),
    path('create', CreateTodo.as_view(), name='create'),
    path('edit/<pk>', EditTodo.as_view(), name='edit'),
    path('delete/<pk>', DeleteTodo.as_view(), name='delete'),
    path('view/<pk>', ViewTodo.as_view(), name='view')
]