from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomRegisterForm

def register(request):
    if request.method == "POST":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid:
            register_form.save()
            messages.success(request, ("New user account created. Login to get started."))
            return redirect('todolist')
    else: 
        register_form = CustomRegisterForm()
        context = {
            'register_form': register_form,
        }
    return render(request, 'users_app/register.html', context)
