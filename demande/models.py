from django.db import models
from users.models import User


class TypeDemande(models.Model):
    nom = models.CharField(max_length=254)
    description = models.TextField(null=True)
    nombre_validations_min_requis = models.IntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class TypeDemandeValidator(models.Model):
    type_demande = models.ForeignKey(TypeDemande, on_delete=models.CASCADE, related_name='validators')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    interrupt_chain_on_rejection = models.BooleanField(default=False)

    class Meta:
        ordering = ['rank']
        unique_together = ('type_demande', 'user')

    def __str__(self):
        return f"{self.type_demande.nom} - {self.user.codeuser} (Rank {self.rank})"


class Demande(models.Model):
    type_demande = models.ForeignKey(TypeDemande, on_delete=models.PROTECT, related_name='demandes')
    initiateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='initiated_demandes')
    status = models.IntegerField(default=0)  # status=0: en attente, 1: validé, 2: rejeté
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande {self.id} - {self.type_demande.nom} by {self.initiateur.codeuser}"

    def evaluer_statut(self):
        # Évaluer le statut global de la demande
        validations = self.validations.all()
        validations_requises = [v for v in validations if v.user in self.type_demande.validators.filter(rank=v.rank)]
        validations_optionnelles = [v for v in validations if v.user in self.type_demande.validators.filter(rank=v.rank)]

        if self.type_demande.nombre_validations_min_requis:
            # If a minimum number of validations is defined
            valid_count = sum(1 for v in validations_requises if v.status == 1)
            if valid_count >= self.type_demande.nombre_validations_min_requis:
                self.status = 1  # validé
            elif any(v.status == 2 for v in validations_requises):
                self.status = 2  # rejeté
            else:
                self.status = 0  # en attente
        else:
            # If no minimum number of validations is defined, all required validations must be 1
            if all(v.status == 1 for v in validations_requises):
                self.status = 1  # validé
            elif any(v.status == 2 for v in validations_requises):
                self.status = 2  # rejeté
            else:
                self.status = 0  # en attente

        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.pk:
            first_validator = self.type_demande.validators.order_by('rank').first()
            if first_validator:
                DemandeValidation.objects.create(demande=self, user=first_validator.user, rank=first_validator.rank)

class DemandeValidation(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='validations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demande_validations')
    status = models.IntegerField(default=0)  # status=0: en attente, 1: validé, 2: rejeté
    rank = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Validation for Demande {self.demande.id} by {self.user.codeuser}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 1:  # Validated
            next_validator = self.demande.type_demande.validators.filter(rank=self.rank + 1).first()
            if next_validator:
                DemandeValidation.objects.create(demande=self.demande, user=next_validator.user, rank=next_validator.rank)
        elif self.status == 2:  # Rejected
            validator = self.demande.type_demande.validators.filter(user=self.user, rank=self.rank).first()
            if validator and validator.interrupt_chain_on_rejection:
                self.demande.status = 2  # Mark demande as rejected
                self.demande.save()


class Commentaire(models.Model):
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE, related_name='commentaires')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commentaire par {self.user} pour la demande {self.demande}"
