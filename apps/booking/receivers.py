from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Booking
from apps.job.models import DriverJobRequest
from .signals import booking_created, invitation_created


@receiver(booking_created)
def notify_freelancer_on_booking(sender, booking, **kwargs):
    "Notifies the freelancer when a booking is created."
    subject = 'Confirmation of booking %s' % booking.reference_number
    content = render_to_string(
        'booking/email/includes/freelancer_booking_confirmation.html',
        {
            'object': booking,
            'driverjobrequest':
                DriverJobRequest.objects.get_from_jobrequest(
                                                    booking.jobrequest)
         }
    )
    send_mail(booking.freelancer.user.email,
              subject,
              'email/base',
              {'title': 'Confirmation of booking',
               'content': content},
              from_email=settings.BOOKINGS_EMAIL)


@receiver(invitation_created)
def notify_freelancer_on_invitation(sender, invitation, **kwargs):
    "Notifies the freelancer when they are invited to book a job."
    title = 'A new job was just posted'
    content = render_to_string(
        'booking/email/includes/freelancer_invitation.html',
        {
            'object': invitation,
            'driverjobrequest':
                DriverJobRequest.objects.get_from_jobrequest(
                                                    invitation.jobrequest)
         }
    )
    send_mail(invitation.freelancer.user.email,
              title,
              'email/base',
              {'title': title,
               'content': content},
              from_email=settings.BOOKINGS_EMAIL)

# @receiver(booking_created)
# def notify_client_on_booking(sender, booking, **kwargs):
#     "Notifies the client when a booking is created."
#     subject = 'Confirmation of booking %s' % booking.reference_number
#     content = render_to_string(
#         'booking/email/includes/client_booking_confirmation.html',
#         {
#             'object': booking,
#             'driverjobrequest':
#                 DriverJobRequest.objects.get_from_jobrequest(
#                                                     booking.jobrequest)
#          }
#     )
#     send_mail(booking.jobrequest.client.user.email,
#               subject,
#               'email/base',
#               {'title': 'Your booking has been confirmed',
#                'content': content},
#               from_email=settings.BOOKINGS_EMAIL)

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
