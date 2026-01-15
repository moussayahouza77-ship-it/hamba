from .models import OwnerProfile


def owner_profile(request):
    # Returns the single OwnerProfile instance if exists, else None
    owner = OwnerProfile.objects.first()
    context = {'owner_profile': owner}

    # Add unread notifications count for authenticated users (if notifications app available)
    try:
        if request.user.is_authenticated:
            from notifications.models import Notification
            unread = Notification.objects.filter(destinataire=request.user, lu=False).count()
            context['unread_notifications'] = unread
        else:
            context['unread_notifications'] = 0
    except Exception:
        # Notifications app may not be fully configured yet; fail gracefully
        context['unread_notifications'] = 0

    return context
