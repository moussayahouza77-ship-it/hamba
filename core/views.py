from django.shortcuts import render
from posts.models import Post


def home(request):
    posts = Post.objects.filter(actif=True).order_by('-date_creation')[:10]
    return render(request, 'core/home.html', {'posts': posts})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')
