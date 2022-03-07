from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    #Checks if the request method is POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): #Checks if the form is valid
            form.save() #Saves the form to the database
            messages.success(request, f'Account Created! You are now able to Login') #Prints out a flas message
            return redirect('login') #Redirects back to the login page
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
