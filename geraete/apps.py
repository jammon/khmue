from django.apps import AppConfig


class GeraeteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geraete"

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
