from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Booking
from apps.job.models import JobRequest
from .signals import booking_created, invitation_created
from django_fsm.signals import post_transition
from apps.notification.models import Notification
from . import tasks


@receiver(post_transition)
def invite_matching_freelancers(sender, instance, name,
                                source, target, **kwargs):
    """Invites all freelancers who match the job request,
    when a new job request is opened."""
    if name == 'open' and issubclass(sender, JobRequest):
        tasks.invite_matching_freelancers(instance)


@receiver(booking_created)
def notify_freelancer_on_booking(sender, booking, **kwargs):
    "Notifies the freelancer when a booking is created."
    subject = 'Confirmation of booking for %s' % \
                booking.jobrequest.reference_number
    content = render_to_string(
        'booking/email/includes/freelancer_booking_confirmation.html',
        {'object': booking.jobrequest})
    send_mail(booking.freelancer.user.email,
              subject,
              'email/base',
              {'title': 'Confirmation of booking',
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)


@receiver(booking_created)
def notify_admin_on_booking(sender, booking, **kwargs):
    "Notifies the admin when a booking is created that fully books a job."
    job_request = booking.jobrequest
    if job_request.is_full:
        subject = 'Job request %s now awaiting confirmation' % \
                job_request.reference_number

        content = render_to_string(
            'booking/email/includes/admin_fully_booked.html',
            {'object': job_request}
        )

        send_mail(settings.BOOKINGS_EMAIL,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content})


@receiver(invitation_created)
def notify_freelancer_on_invitation(sender, invitation, **kwargs):
    "Notifies the freelancer when they are invited to book a job."
    title = 'A new job was just posted'
    content = render_to_string(
        'booking/email/includes/freelancer_invitation.html',
        {
            'object': invitation,
            'job_request': invitation.jobrequest
         }
    )
    send_mail(invitation.freelancer.user.email,
              title,
              'email/base',
              {'title': title,
               'content': content},
              from_email=settings.BOOKINGS_FROM_EMAIL)

    # Create notification
    Notification.objects.create(
            message='A new job was just posted.',
            category='freelancer_invitation',
            related_object=invitation.jobrequest,
            user=invitation.freelancer.user)

# @receiver(booking_created)
# def notify_client_on_booking(sender, booking, **kwargs):
#     "Notifies the client when a booking is created."
#     subject = 'Confirmation of booking %s' % booking.reference_number
#     content = render_to_string(
#         'booking/email/includes/client_booking_confirmation.html',
#         {
#             'object': booking,
#             'driverjobrequest': booking.jobrequest
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
