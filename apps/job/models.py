from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import date, datetime
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from apps.driver.models import Driver
from apps.client.models import Client


class JobRequestQuerySet(models.QuerySet):
    "Custom queryset for JobRequests."

    def future(self):
        """Filter by job requests that are in the future (i.e. started
        today or later.
        TODO - we may need to improve this so it takes into account duration.
        """
        return self.filter(date__gte=date.today())

    def past(self):
        """Filter by job requests that are in the past (i.e. started
        yesterday or before."""
        return self.exclude(date__gte=date.today())

    def for_client(self, client):
        "Filters by job requests that a client has requested."
        return self.filter(client=client)


class JobRequest(models.Model):
    """A request by a client for a service for a particular
    period of time, to be performed by one or more freelancers.
    
    For the moment, we will not really use this model directly,
    but will use the DriverJobRequest model.  But it's sensible to split
    up the generic job request code from the driver specific stuff
    from the beginning.
    """

    # The client who is making the job request
    client = models.ForeignKey(Client, related_name='job_requests')

    # Status - for admin purposes
    STATUS_OPEN = 'OP'
    STATUS_CONFIRMED = 'CF'
    STATUS_COMPLETE = 'CP'
    STATUS_CANCELLED = 'CA'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_CANCELLED, 'Cancelled'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=STATUS_OPEN)

    # The date this form was submitted
    date_submitted = models.DateTimeField(auto_now_add=True)

    pay_per_hour = MoneyField(max_digits=5, decimal_places=2,
                              default_currency='GBP')
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default=datetime.now)
    duration = models.PositiveSmallIntegerField(default=1,
                    help_text='Length of the job, in hours.')
    number_of_freelancers = models.PositiveSmallIntegerField(
                                'Number of people required',
                                choices=[(i, i) for i in range(1, 10)],
                                default=1)

    POSTCODE_CENTRAL = 'C'
    POSTCODE_WEST = 'W'
    POSTCODE_SOUTH_WEST = 'SW'
    POSTCODE_SOUTH_EAST = 'SE'
    POSTCODE_EAST = 'E'
    POSTCODE_NORTH = 'N'
    POSTCODE_NORTH_WEST = 'NW'
    POSTCODE_CHOICES = (
        (POSTCODE_CENTRAL, 'Central London (Postcodes: EC, WC)'),
        (POSTCODE_WEST, 'West London (Postcodes: W)'),
        (POSTCODE_SOUTH_WEST, 'South West London (Postcodes: SW)'),
        (POSTCODE_SOUTH_EAST, 'South East London (Postcodes: SE)'),
        (POSTCODE_EAST, 'East London (Postcodes: E)'),
        (POSTCODE_NORTH, 'North London (Postcodes: N)'),
        (POSTCODE_NORTH_WEST, 'North West London (Postcodes: NW)'),
    )
    postcode_area = models.CharField('Location',
                                     max_length=2, choices=POSTCODE_CHOICES)

    objects = JobRequestQuerySet.as_manager()

    def __unicode__(self):
        return self.reference_number

    @property
    def reference_number(self):
        "Returns a reference number for this request."
        return 'JR%s' % str(self.pk).zfill(5)

    def get_absolute_url(self):
        return reverse('jobrequest_detail', args=(self.pk,))

    class Meta:
        ordering = '-date_submitted',


class DriverJobRequestManager(models.Manager):
    """Manager for DriverJobRequests."""

    def get_from_jobrequest(self, jobrequest):
        "Gets a DriverJobRequest object from the JobRequest."""
        return self.get(pk=jobrequest.pk)


class DriverJobRequest(JobRequest):
    """A JobRequest that is specifically for drivers to complete.
    """
    vehicle_types = MultiSelectField(choices=Driver.VEHICLE_TYPE_CHOICES)
    driving_experience = models.CharField('Minimum driving experience',
                                max_length=3,
                                choices=Driver.DRIVING_EXPERIENCE_CHOICES,
                                default=Driver.DRIVING_EXPERIENCE_LESS_ONE)

    own_vehicle = models.BooleanField(
                            'The driver must supply their own vehicle.',
                            default=True)

    objects = DriverJobRequestManager.from_queryset(JobRequestQuerySet)()
