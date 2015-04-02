from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from .models import DriverJobRequest
from django.template.loader import render_to_string


@receiver(post_save, sender=DriverJobRequest)
def notify_admin_on_job_request(sender, instance, created, **kwargs):
    "Notifies the bookings email address when a new job request is submitted."
    if created:
        subject = 'New job request %s' % instance.reference_number
        send_mail(settings.BOOKINGS_EMAIL,
                  subject,
                  'email/base',
                  {'title': 'New job request',
                   'content': render_to_string(
                            'job/email/includes/driverjobrequest.html',
                            {'object': instance, 'admin': True})})


@receiver(post_save, sender=DriverJobRequest)
def notify_client_on_job_request(sender, instance, created, **kwargs):
    """Sends a confirmation email to the client when they submit
    a new job request."""
    if created:
        content = render_to_string(
            'job/email/includes/driverjobrequest_confirmation.html',
            {'object': instance,
             'admin': False})
        send_mail(instance.client.user.email,
              'Thank you for your booking',
              'email/base',
              {'title': 'Thank you for your booking',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
              from_email=settings.BOOKINGS_EMAIL)

#
#
# @receiver(jobrequest_cancelled)
# def notify_client_on_job_request_cancelled(sender, jobrequest, **kwargs):
#     """Sends a notification email to the client when a job request
#     is cancelled."""
#     send_mail(jobrequest.email,
#               'Your job request has been cancelled',
#               'job/email/jobrequest_cancelled',
#               {'object': jobrequest,
#                'bookings_email': settings.BOOKINGS_EMAIL},
#               from_email=settings.BOOKINGS_EMAIL)
