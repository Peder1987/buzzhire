from huey.djhuey import crontab, db_periodic_task, db_task
from apps.core.email import send_mail
from .models import JobRequest
import logging


logger = logging.getLogger('project')

# @db_periodic_task(crontab(minute='*'))
def complete_job_requests():
    """Checks any open job requests to see if they need moving over to being complete.
    """
    pass


# @periodic_task(crontab(hour='10', minute='00'))
# def send_customer_reminder_emails():
#     "Send reminder emails to any customers with slots coming up tomorrow."
#     slots = Slot.objects.booked_for_tomorrow()
#     total = slots.count()
#     count = 0
#     for slot in slots:
#         try:
#             subject = 'Reminder: your booking with with %s' % \
#                                                             slot.practitioner
#             send_mail(slot.customer.user,
#                       subject,
#                       'booking/email/booking_reminder',
#                       {'object': slot})
#             count += 1
#         except Exception as e:
#             logger.error('Could not send a reminder email for slot '
#                          'number %d: %s' % (slot.pk, e))
#     logger.info('Sent %d of %d reminder emails.' % (count, total))
