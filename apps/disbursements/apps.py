from django.apps import AppConfig


class DisbursementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.disbursements'

    def ready(self):
        import apps.disbursements.signals  # noqa: F401
