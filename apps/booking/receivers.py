from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Booking
from apps.job.models import DriverJobRequest


@receiver(post_save, sender=Booking)
def notify_freelancer_on_booking(sender, instance, created, **kwargs):
    "Notifies the freelancer when a booking is created."
    if created:
        subject = 'Confirmation of booking %s' % instance.reference_number
        content = render_to_string(
            'booking/email/includes/freelancer_booking_confirmation.html',
            {
                'object': instance,
                'driverjobrequest':
                    DriverJobRequest.objects.get_from_jobrequest(
                                                        instance.jobrequest)
             }
        )
        send_mail(instance.freelancer.user.email,
                  subject,
                  'email/base',
                  {'title': 'Confirmation of booking',
                   'content': content},
                  from_email=settings.BOOKINGS_EMAIL)


# @receiver(post_save, sender=Booking)
# def notify_client_on_booking(sender, instance, created, **kwargs):
#     "Notifies the client when a booking is created."
#     if created:
#         subject = 'Your driver has now been confirmed'
#         content = render_to_string(
#             'booking/email/includes/client_booking_confirmation.html',
#             {'object': instance})
#
#         send_mail(instance.jobrequest.client.user.email,
#                   subject,
#                   'email/base',
#                   {'title': subject,
#                    'content': content},
#                   from_email=settings.BOOKINGS_EMAIL)
