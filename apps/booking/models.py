from django.db import models
from django import forms
from datetime import date
import calendar
from apps.freelancer.models import Freelancer
from apps.job.models import JobRequest


class BookingQuerySet(models.QuerySet):
    "Custom queryset for Bookings."

    def future(self):
        """Filter by job requests that are in the future (i.e. started
        today or later.
        TODO - we may need to improve this so it takes into account duration.
        """
        return self.filter(jobrequest__date__gte=date.today())

    def past(self):
        """Filter by job requests that are in the past (i.e. started
        yesterday or before."""
        return self  # TODO
        return self.exclude(jobrequest__date__gte=date.today())

    def for_freelancer(self, freelancer):
        "Filters by job requests that a freelancer has been allocated to."
        return self.filter(freelancer=freelancer)


class Booking(models.Model):
    """A Booking is an allocation of a single freelancer to a JobRequest.
    JobRequests can potentially have multiple Bookings.
    """
    freelancer = models.ForeignKey(Freelancer, related_name='bookings')
    jobrequest = models.ForeignKey(JobRequest, related_name='jobrequests')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.reference_number

    @property
    def reference_number(self):
        "Returns a reference number for this booking."
        return 'BK%s' % str(self.pk).zfill(7)

    class Meta:
        # A single freelancer can't be booked in twice for the same job
        unique_together = (("freelancer", "jobrequest"),)


    objects = BookingQuerySet.as_manager()



class Availability(models.Model):
    """A model for storing the general availability
    of a particular freelancer."""
    freelancer = models.OneToOneField(Freelancer)

    # Specify the two dimensions for the fields, to help with processing
    SHIFTS = ('early_morning', 'morning', 'afternoon', 'evening', 'night')
    DAYS = [day.lower() for day in calendar.day_name]


    AVAILABILITY_CHOICES = ((True, 'Available'), (False, 'Not available'))
    FIELD_KWARGS = {
        'choices': AVAILABILITY_CHOICES,
        'default': True,
    }
    # Define all the shifts for the week as separate fields
    # Obviously this isn't very DRY, but it's simple to read and will
    # perform better than having them in separate tables
    monday_early_morning = models.BooleanField(help_text='2am - 7am',
                                               **FIELD_KWARGS)
    monday_morning = models.BooleanField(help_text='7am - 12pm',
                                         **FIELD_KWARGS)
    monday_afternoon = models.BooleanField(help_text='12pm - 5pm',
                                           **FIELD_KWARGS)
    monday_evening = models.BooleanField(help_text='5pm - 10pm',
                                         **FIELD_KWARGS)
    monday_night = models.BooleanField(help_text='10pm - 2am',
                                       **FIELD_KWARGS)

    tuesday_early_morning = models.BooleanField(**FIELD_KWARGS)
    tuesday_morning = models.BooleanField(**FIELD_KWARGS)
    tuesday_afternoon = models.BooleanField(**FIELD_KWARGS)
    tuesday_evening = models.BooleanField(**FIELD_KWARGS)
    tuesday_night = models.BooleanField(**FIELD_KWARGS)

    wednesday_early_morning = models.BooleanField(**FIELD_KWARGS)
    wednesday_morning = models.BooleanField(**FIELD_KWARGS)
    wednesday_afternoon = models.BooleanField(**FIELD_KWARGS)
    wednesday_evening = models.BooleanField(**FIELD_KWARGS)
    wednesday_night = models.BooleanField(**FIELD_KWARGS)

    thursday_early_morning = models.BooleanField(**FIELD_KWARGS)
    thursday_morning = models.BooleanField(**FIELD_KWARGS)
    thursday_afternoon = models.BooleanField(**FIELD_KWARGS)
    thursday_evening = models.BooleanField(**FIELD_KWARGS)
    thursday_night = models.BooleanField(**FIELD_KWARGS)

    friday_early_morning = models.BooleanField(**FIELD_KWARGS)
    friday_morning = models.BooleanField(**FIELD_KWARGS)
    friday_afternoon = models.BooleanField(**FIELD_KWARGS)
    friday_evening = models.BooleanField(**FIELD_KWARGS)
    friday_night = models.BooleanField(**FIELD_KWARGS)

    saturday_early_morning = models.BooleanField(**FIELD_KWARGS)
    saturday_morning = models.BooleanField(**FIELD_KWARGS)
    saturday_afternoon = models.BooleanField(**FIELD_KWARGS)
    saturday_evening = models.BooleanField(**FIELD_KWARGS)
    saturday_night = models.BooleanField(**FIELD_KWARGS)

    sunday_early_morning = models.BooleanField(**FIELD_KWARGS)
    sunday_morning = models.BooleanField(**FIELD_KWARGS)
    sunday_afternoon = models.BooleanField(**FIELD_KWARGS)
    sunday_evening = models.BooleanField(**FIELD_KWARGS)
    sunday_night = models.BooleanField(**FIELD_KWARGS)
