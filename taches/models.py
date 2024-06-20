from django.db import models
from users.models import User
# Create your models here.

#
#
# CLASS STATUT
# un utilisateur doit pouvoir creer un STATUT, qui sera attribuer aux taches du workflow de l'entreprise
#
class Statut(models.Model):
    intitule = models.CharField(max_length=255, blank=True, null=True)
    couleur = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.intitule}"





#
#
# CLASS TACHE
# un utilisateur doit pouvoir creer une tache, la delimiter dans le temps et l'attribuer
#
class Tache(models.Model):
    intitule = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    initiateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='initiated_taches')
    executeur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='executed_taches')
    statut = models.ForeignKey(Statut, on_delete=models.CASCADE, related_name='statut')
    date_debut_tache = models.DateTimeField(blank=True, null=True)
    date_fin_tache = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tache - {self.intitule} : {self.statut}"

