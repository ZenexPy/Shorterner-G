from django.apps import AppConfig


class ShorternerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shorterner'


    def ready(self):
        import shorterner.signals
