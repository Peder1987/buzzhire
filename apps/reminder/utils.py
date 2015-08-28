from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from apps.job.models import JobRequest
from apps.notification.models import Notification

class ScheduledReminderSet(object):
    """A set of reminders that should be scheduled for a job request.
    
    This is a serializable object that can be passed to a task queue, 
    and handles checking that the reminders should still be sent, and the
    sending.
    
    For use with tasks.send_reminders().
    
    """

    def __init__(self, job_request, title, scheduled_datetime):
        self.title = title
        self.job_request_id = job_request.id
        self.start_datetime_when_scheduled = job_request.start_datetime
        self.scheduled_datetime = scheduled_datetime

    def __getstate__(self):
        "Method to allow serialization."
        return {
            'title': self.title,
            'job_request_id': self.job_request_id,
            'start_datetime_when_scheduled':
                                        self.start_datetime_when_scheduled,
            'scheduled_datetime': self.scheduled_datetime,
        }

    def __setstate__(self, dict):
        "Method to allow serialization."
        self.title = dict['title']
        self.job_request_id = dict['job_request_id']
        self.start_datetime_when_scheduled = \
                                        dict['start_datetime_when_scheduled']
        self.scheduled_datetime = dict['scheduled_datetime']

    @property
    def job_request(self):
        "Returns the job request."
        if not getattr(self, '_job_request', None):
            self._job_request = JobRequest.objects.get(id=self.job_request_id)
        return self._job_request

    def get_job_request_display(self):
        """Robustly returns a display of the job request.
        Will not raise exception if the JobRequest cannot be found."""
        try:
            return str(self.job_request)
        except JobRequest.DoesNotExist:
            return 'missing job request id %s' % self.job_request_id

    def is_still_valid(self):
        """Returns whether it is still valid to send the reminders.
        """
        # Only remind if the status is confirmed (so we don't remind
        # for cancelled jobs)
        if self.job_request.status != JobRequest.STATUS_CONFIRMED:
            return False

        # Test to check the start_datetime hasn't changed; if it has,
        # new reminders will have been scheduled
        # TODO - there is a slight problem with this logic - if the job
        # request is changed and then changed back, multiple reminders
        # will be sent out
        return self.start_datetime_when_scheduled == \
                                            self.job_request.start_datetime

    def send_to_recipient(self, recipient, recipient_type):
        "Sends reminders to a single recipient."
        content = render_to_string(
            'reminder/email/includes/jobrequest_reminder_%s.html' \
                                                        % recipient_type,
            {'object': self.job_request,
             'base_url': settings.BASE_URL})

        send_mail(recipient.user.email,
              self.title,
              'email/base',
              {'title': self.title,
               'content': content,
               'bookings_email': settings.BOOKINGS_EMAIL},
              from_email=settings.BOOKINGS_FROM_EMAIL)

        Notification.objects.create(
                message=self.title,
                category='%s_reminder' % recipient_type,
                related_object=self.job_request,
                user=recipient.user)

    def send(self):
        """Sends out reminders to freelancers and client
        from the supplied reminder set.
        """
        self.send_to_recipient(self.job_request.client, 'client')
        for booking in self.job_request.bookings.all():
            self.send_to_recipient(booking.freelancer, 'freelancer')
