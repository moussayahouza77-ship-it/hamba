from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'destinataire', 'emetteur', 'lu', 'date_creation')
    list_filter = ('type', 'lu')
