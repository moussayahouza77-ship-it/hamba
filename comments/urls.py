from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('like-toggle/', views.like_toggle, name='like_toggle'),
]
