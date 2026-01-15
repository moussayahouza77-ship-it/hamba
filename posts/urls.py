from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('search/', views.post_search, name='search'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('create/', views.post_create, name='create'),
    path('<int:pk>/edit/', views.post_edit, name='edit'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
]
