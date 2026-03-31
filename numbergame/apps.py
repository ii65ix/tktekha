from django.apps import AppConfig


class NumbergameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "numbergame"
    verbose_name = "Number guessing (online)"

    def ready(self) -> None:
        # Register signals for Profile auto-creation.
        import numbergame.signals  # noqa: F401
