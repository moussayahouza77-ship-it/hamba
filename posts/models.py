from pathlib import Path

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage


class Post(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    # simple category field to allow filtering
    CATEGORIES = [
        ('general', 'Général'),
        ('tech', 'Tech'),
        ('news', 'Actualités'),
        ('life', 'Lifestyle'),
    ]
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='general')
    contenu = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def like_count(self):
        # avoid circular import at module import time
        from comments.models import Like
        return Like.objects.filter(post=self).count()

    def image_url(self):
        return self.image.url if self.image else None

    def thumbnail_path(self):
        if not self.image:
            return None
        name = Path(self.image.name).name
        return f'posts/thumbs/{name}.jpg'

    def thumbnail_url(self):
        tp = self.thumbnail_path()
        if not tp:
            return None
        if default_storage.exists(tp):
            return default_storage.url(tp)
        return None
