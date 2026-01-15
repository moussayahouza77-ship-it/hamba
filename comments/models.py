from django.db import models
from django.conf import settings
from posts.models import Post


class Comment(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return f'Commentaire by {self.auteur} on {self.post}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', null=True, blank=True, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user cannot like the same target twice
        unique_together = (('user', 'post'), ('user', 'comment'))

    def __str__(self):
        target = self.post or self.comment
        return f'Like by {self.user} on {target}'
