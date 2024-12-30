from django.apps import AppConfig


class BuymeacoffeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_buymeacoffee'
    verbose_name = 'Buy Me a Coffee'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        You can add any initialization code here.
        """
        pass
