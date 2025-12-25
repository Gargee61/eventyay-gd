from django.apps import AppConfig


class EventyayApiConfig(AppConfig):
    name = 'eventyay.api'
    label = 'api'

    def ready(self):
        from . import signals, webhooks  # noqa


default_app_config = 'eventyay.api.EventyayApiConfig'

from django.apps import AppConfig

class EventyayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventyay'
    
    def ready(self):
        import eventyay.signals  