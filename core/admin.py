from django.contrib import admin
from .models import OwnerProfile


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('pseudo_ou_entreprise', 'nom_complet', 'date_mise_a_jour')
    readonly_fields = ('date_mise_a_jour',)
