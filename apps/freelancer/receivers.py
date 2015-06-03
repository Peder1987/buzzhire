from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Freelancer


@receiver(post_save)
def notify_admin_on_freelancer_created(sender, instance, created, **kwargs):
    "Notifies the admin when a freelancer is created."
    if created and isinstance(instance, Freelancer):
        subject = 'New freelancer sign up: %s' % instance.get_full_name()
        content = render_to_string(
            'freelancer/email/includes/freelancer_created.html',
            {
                'object': instance,
             }
        )
        send_mail(settings.CONTACT_EMAIL,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content},
                  from_email=settings.CONTACT_EMAIL)