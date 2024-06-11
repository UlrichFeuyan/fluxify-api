from django.contrib import admin

from users.models import *
from .models import *

admin.site.register(User)
admin.site.register(Demande)
admin.site.register(TypeDemande)
admin.site.register(DemandeValidation)
