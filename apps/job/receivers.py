from django.dispatch import receiver
from .signals import driverjobrequest_created
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import DriverJobRequest, JobRequest
from django_fsm.signals import post_transition


@receiver(post_transition, sender=DriverJobRequest)
def notifications_on_job_request_opened(sender, instance, name,
                                source, target, **kwargs):
    "Sends notifies when a new job request is opened."
    if name == 'open':

        # First, notify the bookings email address
        subject = 'New job request %s' % instance.reference_number
        send_mail(settings.BOOKINGS_EMAIL,
                  subject,
                  'email/base',
                  {'title': 'New job request',
                   'content': render_to_string(
                            'job/email/includes/admin_driverjobrequest.html',
                        {'object': instance, 'admin': True})})


        # Next, send a confirmation email to the client
        content = render_to_string(
            'job/email/includes/driverjobrequest_created.html',
            {'object': instance,
             'admin': False})
        send_mail(instance.client.user.email,
              'Thank you for your booking',
              'email/base',
              {'title': 'Thank you for your booking',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
              from_email=settings.BOOKINGS_EMAIL)


@receiver(post_transition)
def notify_client_on_jobrequest_confirmed(sender, instance, name,
                                          source, target, **kwargs):
    """Sends a notification email to the client when a job request
    is confirmed."""
    if issubclass(sender, JobRequest):
        # Only do JobRequests, or subclasses.
        if sender is JobRequest:
            # For now, we just manually load the DriverJobRequest
            instance = DriverJobRequest.objects.get(pk=instance.pk)

        if target == DriverJobRequest.STATUS_CONFIRMED:
            content = render_to_string(
                'job/email/includes/driverjobrequest_confirmed.html',
                {'object': instance})
            send_mail(instance.client.user.email,
                  'Your job request is now confirmed',
                  'email/base',
                  {'title': 'Your job request is now confirmed',
                   'content': content,
                   'bookings_email': settings.BOOKINGS_EMAIL},
                  from_email=settings.BOOKINGS_EMAIL)

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
