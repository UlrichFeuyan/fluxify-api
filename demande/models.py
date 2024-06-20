from django.db import models

from users.models import User

class TypeDemande(models.Model):
    nom = models.CharField(max_length=254)
    description = models.TextField(null=True)
    profils_requis = models.ManyToManyField('users.Profil', related_name='types_demandes_requis', blank=True)
    profils_optionnels = models.ManyToManyField('users.Profil', related_name='types_demandes_optionnels', blank=True)
    nombre_validations_min_requis = models.IntegerField(default=1, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Demande(models.Model):
    type_demande = models.ForeignKey(TypeDemande, on_delete=models.PROTECT, related_name='demandes')
    initiateur = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='initiated_demandes')
    validateurs = models.ManyToManyField('users.User', through='DemandeValidation', related_name='demandes_a_valider')
    status = models.IntegerField(default=0)  # status=0: en attente, 1: validé, 2: rejeté
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande {self.id} - {self.type_demande.nom} by {self.initiateur.codeuser}"

    def evaluer_statut(self):
        # Évaluer le statut global de la demande
        validations = self.validations.all()
        validations_requises = [v for v in validations if v.user.profil in self.type_demande.profils_requis.all()]
        validations_optionnelles = [v for v in validations if v.user.profil in self.type_demande.profils_optionnels.all()]

        if all(v.status for v in validations_requises) and len(validations_requises) >= self.type_demande.nombre_validations_min_requis:
            self.status = 'validé'
        elif any(v.status is False for v in validations_requises):
            self.status = 'rejeté'
        else:
            self.status = 'en attente'

        self.save()


class DemandeValidation(models.Model):
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE, related_name='validations')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='demande_validations')
    status = models.IntegerField(default=0)  # status=0: en attente, 1: validé, 2: rejeté

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Validation for Demande {self.demande.id} by {self.user.codeuser}"


class Commentaire(models.Model):
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE, related_name='commentaires')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commentaire par {self.user} pour la demande {self.demande}"
