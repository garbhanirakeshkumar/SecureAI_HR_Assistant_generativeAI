from django.apps import AppConfig


class HrassistantappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "HRassistantApp"

    def ready(self):
        import HRassistantApp.signals