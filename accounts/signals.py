from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.conf import settings
from pathlib import Path
from utils.image_utils import create_thumbnail
from django.core.files.storage import default_storage


@receiver(post_save, sender=UserProfile)
def generate_profile_thumbnail(sender, instance, created, **kwargs):
    if not instance.photo:
        return
    name = Path(instance.photo.name).name
    thumb_path = f'profiles/thumbs/{name}.jpg'
    media_root = Path(settings.MEDIA_ROOT)
    src = media_root / Path(instance.photo.name)
    dst = media_root / Path(thumb_path)
    if not default_storage.exists(thumb_path):
        try:
            create_thumbnail(str(src), str(dst), size=(200,200))
        except Exception:
            pass
