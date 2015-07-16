from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Client


@receiver(post_save)
def welcome_client_on_sign_up(sender, instance, created, **kwargs):
    "Sends a welcome email when a client signs up."
    if created and isinstance(instance, Client):
        subject = 'Welcome to Buzzhire!'
        content = render_to_string(
            'client/email/includes/client_welcome.html',
            {'object': instance}
        )
        send_mail(instance.user.email,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content})
