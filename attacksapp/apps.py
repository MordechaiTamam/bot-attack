from django.apps import AppConfig


class AttacksappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attacksapp'

    def ready(self):
        import attacksapp.signals
