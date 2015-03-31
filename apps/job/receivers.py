from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
# from .models import JobRequest
# from .signals import jobrequest_cancelled, jobrequest_opened


# @receiver(post_save, sender=JobRequest)
# def notify_admin_on_job_request(sender, instance, created, **kwargs):
#     "Notifies the bookings email address when a new job request is submitted."
#     if created:
#         subject = 'New job request from %s' % instance.full_name
#         send_mail(settings.BOOKINGS_EMAIL,
#                   subject,
#                   'job/email/jobrequest_created',
#                   {'object': instance})
#
#
# @receiver(post_save, sender=JobRequest)
# def notify_client_on_job_request(sender, instance, created, **kwargs):
#     """Sends a confirmation email to the client when they submit
#     a new job request."""
#     if created:
#         send_mail(instance.email,
#                   'Thank you for your job request',
#                   'job/email/jobrequest_confirmation',
#                   {'object': instance,
#                    'bookings_email': settings.BOOKINGS_EMAIL},
#                   from_email=settings.BOOKINGS_EMAIL)
#
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
