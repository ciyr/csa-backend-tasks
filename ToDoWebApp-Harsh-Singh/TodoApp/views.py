from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:login')
    else:
        form = UserCreationForm()

    return render(request, 'todoapp/register.html', {'form': form})


@login_required
def home_user(request):
    todo_list = request.user.todo_set.all()
    context = {
        'user': request.user.username,
        'todo_list': todo_list,
    }
    return render(request, 'todoapp/home.html', context)


class CreateTodo(CreateView, LoginRequiredMixin):
    model = Todo
    form_class = TodoForm
    template_name = 'todoapp/create_todo.html'

    def form_valid(self, form):
        user = self.request.user
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')
        Todo.objects.create(user=user, title=title, content=content)
        return redirect('todo:home_user')


class EditTodo(UpdateView, LoginRequiredMixin):
    model = Todo
    form_class = TodoForm
    template_name = 'todoapp/create_todo.html'
    success_url = reverse_lazy('todo:home_user')


class DeleteTodo(DeleteView, LoginRequiredMixin):
    model = Todo
    template_name = 'todoapp/delete_todo.html'
    success_url = reverse_lazy('todo:home_user')

    def get_context_data(self, **kwargs):
        context = {
            'todo': self.request.user.todo_set.get(id=self.kwargs['pk']).title
        }
        return context


class ViewTodo(DetailView):
    model = Todo
    template_name = 'todoapp/details_todo.html'

    def get_context_data(self, **kwargs):
        context = {
            'todo': self.request.user.todo_set.get(id=self.kwargs['pk'])
        }
        return context
