from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from posts.models import Post
from notifications.models import Notification


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def profile_view(request):
    # simple dashboard for the user
    my_posts = Post.objects.filter(auteur=request.user).order_by('-date_creation')[:10]
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date_creation')[:20]
    return render(request, 'accounts/profile.html', {'my_posts': my_posts, 'notifications': notifications})
