from django.dispatch import receiver
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from apps.job.models import JobRequest
from apps.service.driver.models import DriverJobRequest
from django_fsm.signals import post_transition


@receiver(post_transition)
def prompt_client_and_drivers_for_feedback(sender, instance, name,
                                          source, target, **kwargs):
    """Emails the client and the drivers for feedback, when a job request
    is finished."""
    # Only do JobRequests, or subclasses
    if issubclass(sender, JobRequest) and \
                                target == DriverJobRequest.STATUS_COMPLETE:

        # For now, we just manually load the DriverJobRequest
        if sender is JobRequest:
            instance = DriverJobRequest.objects.get(pk=instance.pk)

        # Email client
        content = render_to_string(
            'feedback/email/includes/feedback_prompt.html',
            {'object': instance,
             'client': instance.client})

        send_mail(instance.client.user.email,
              'Tell us how it went',
              'email/base',
              {'title': 'Tell us how it went',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
               from_email=settings.BOOKINGS_EMAIL)

        # Email freelancers

        content = render_to_string(
            'feedback/email/includes/feedback_prompt.html',
            {'object': instance})
        recipients = [booking.freelancer.user.email \
                                    for booking in instance.bookings.all()]

        send_mail(recipients,
              'Tell us how it went',
              'email/base',
              {'title': 'Tell us how it went',
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
               from_email=settings.BOOKINGS_EMAIL)
