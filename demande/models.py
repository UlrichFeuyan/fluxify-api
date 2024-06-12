from django.db import models

from users.models import User

class TypeDemande(models.Model):
    nom = models.CharField(max_length=254)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class Demande(models.Model):
    type_demande = models.ForeignKey(TypeDemande, on_delete=models.PROTECT, related_name='demandes')
    validated_at = models.DateField(null=True)
    initiateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='initiated_demandes')
    validateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='validated_demandes')
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande {self.id} - {self.type_demande.nom} by {self.user}"

class DemandeValidation(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='validations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demande_validations')
    status = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Validation for Demande {self.demande.id} by {self.user}"


class Commentaire(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='commentaires')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire par {self.user} pour la demande {self.demande}"
