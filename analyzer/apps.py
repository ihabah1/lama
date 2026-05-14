from django.apps import AppConfig


class AnalyzerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "analyzer"
    verbose_name = "Lotto analyzer"

    def ready(self):
        from .services import init_data

        init_data()
