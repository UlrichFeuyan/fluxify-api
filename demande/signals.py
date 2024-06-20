from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DemandeValidation

@receiver(post_save, sender=DemandeValidation)
def update_demande_status(sender, instance, **kwargs):
    instance.demande.evaluer_statut()
