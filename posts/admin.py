from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation', 'actif', 'image_tag')
    list_filter = ('actif', 'date_creation')
    search_fields = ('titre', 'contenu')

    def image_tag(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' style='height:40px;border-radius:4px;'/>"
        return '-' 
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
