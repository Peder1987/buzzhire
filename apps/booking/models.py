from django.db import models
from datetime import date
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
