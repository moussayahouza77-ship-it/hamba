from django.db import models


class OwnerProfile(models.Model):
    nom_complet = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    pseudo_ou_entreprise = models.CharField(max_length=128, blank=True)
    description_professionnelle = models.TextField(blank=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil propriétaire'
        verbose_name_plural = 'Profil propriétaire'

    def __str__(self):
        return self.pseudo_ou_entreprise or self.nom_complet
