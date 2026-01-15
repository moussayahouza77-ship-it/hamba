from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.conf import settings
from pathlib import Path
from utils.image_utils import create_thumbnail
from django.core.files.storage import default_storage


@receiver(post_save, sender=Post)
def generate_post_thumbnail(sender, instance, created, **kwargs):
    if not instance.image:
        return
    thumb_path = instance.thumbnail_path()
    if not thumb_path:
        return
    # compute absolute paths
    media_root = Path(settings.MEDIA_ROOT)
    src = media_root / Path(instance.image.name)
    dst = media_root / Path(thumb_path)
    # if destination missing or older, create thumbnail
    if not default_storage.exists(thumb_path):
        try:
            create_thumbnail(str(src), str(dst))
        except Exception:
            # fail silently to not break save
            pass
