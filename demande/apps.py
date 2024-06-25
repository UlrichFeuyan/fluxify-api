from django.apps import AppConfig


class DemandeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demande'

    def ready(self):
        import demande.signals
