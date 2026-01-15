from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'post', 'date_creation')
    search_fields = ('auteur__username', 'contenu')
