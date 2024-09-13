from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'auth/register.html', {
        'form': form,
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You\'ve successfully logged in')
            return redirect('index')
        except:
            messages.add_message(request, messages.ERROR, 'Error logging in')
            return render(request, "auth/login.html")

    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    logout(request)

    return redirect('/')


def register_redirect(request):
    return render(request, 'auth/register.html')


def login_redirect(request):
    return render(request, 'auth/login.html')
