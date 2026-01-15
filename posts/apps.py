from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    verbose_name = 'Publications'
    def ready(self):
        # import signals to ensure thumbnail generation
        from . import signals  # noqa
