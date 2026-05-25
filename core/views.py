from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def index_view(request):
    return render(request, 'core/index.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, f'Welcome to Wikishelf, {user.username}!')
            return redirect('index')
    else:
        form = RegisterForm()
 
    return render(request, 'core/auth/register.html', {'form': form})
 
 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
 
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
    else:
        form = LoginForm(request)
 
    return render(request, 'core/auth/login.html', {'form': form})
 
