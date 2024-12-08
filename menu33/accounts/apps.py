from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu33.accounts'

    def ready(self):
        import menu33.accounts.signals