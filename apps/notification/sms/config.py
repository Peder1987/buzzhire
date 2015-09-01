from django.apps import AppConfig


class SMSConfig(AppConfig):

    name = 'apps.notification.sms'
    verbose_name = 'SMS Notification'

    def ready(self):

        # import signal handlers
        from . import receivers
