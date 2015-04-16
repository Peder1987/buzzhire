from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import date, datetime
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from apps.driver.models import Driver, VehicleType, DriverVehicleType
from apps.client.models import Client
from decimal import Decimal


# The percent commission we charge on client rates
COMMISSION_PERCENT = 15
# Number of pence to round to
COMMISSION_ROUND_PENCE = 25


def client_to_driver_rate(client_rate):
    """Given a client rate as a moneyed.Money object,
    return the driver rate, also as a Money object.
    """
    driver_rate = client_rate * (1 - (Decimal(COMMISSION_PERCENT) / 100))

    # Round driver rate to nearest 25p
    # TB the "%.2f" conversion ensures it's to two decimal places
    ROUNDING = float(COMMISSION_ROUND_PENCE) / 100
    driver_rate.amount = Decimal(
            "%.2f" % (round(float(driver_rate.amount) / ROUNDING) * ROUNDING))
    return driver_rate


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

    client_pay_per_hour = MoneyField(max_digits=5, decimal_places=2,
                  default_currency='GBP', default=Decimal(8.50),
                  help_text='How much you will pay per hour, for each driver.')
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default='9:00 AM')
    duration = models.PositiveSmallIntegerField(default=1,
                    help_text='Length of the job, in hours.')
    number_of_freelancers = models.PositiveSmallIntegerField(
                                'Number of drivers required',
                                choices=[(i, i) for i in range(1, 10)],
                                default=1)

    address1 = models.CharField('Address line 1', max_length=75)
    address2 = models.CharField('Address line 2', max_length=75, blank=True)

    # Specify only London - we do it as a field just for ease of handling
    # it on forms etc.
    CITY_LONDON = 'L'
    CITY_CHOICES = (
        (CITY_LONDON, 'London'),
    )
    city = models.CharField(max_length=1, blank=True,
                    choices=CITY_CHOICES, default=CITY_LONDON,
                    help_text='We currently only accept bookings in London.')
    postcode = models.CharField(max_length=10)


    PHONE_REQUIREMENT_NOT_REQUIRED = 'NR'
    PHONE_REQUIREMENT_ANY = 'AY'
    PHONE_REQUIREMENT_ANDROID = 'AN'
    PHONE_REQUIREMENT_IPHONE = 'IP'
    PHONE_REQUIREMENT_WINDOWS = 'WI'
    PHONE_REQUIREMENT_OTHER = 'OT'

    PHONE_REQUIREMENT_CHOICES = (
        (PHONE_REQUIREMENT_NOT_REQUIRED, 'No smart phone needed'),
        (PHONE_REQUIREMENT_ANY, 'Any smart phone'),
        (PHONE_REQUIREMENT_ANDROID, 'Android'),
        (PHONE_REQUIREMENT_IPHONE, 'iPhone'),
        (PHONE_REQUIREMENT_WINDOWS, 'Windows'),
    )
    phone_requirement = models.CharField(max_length=2,
            choices=PHONE_REQUIREMENT_CHOICES,
            default=PHONE_REQUIREMENT_NOT_REQUIRED,
            help_text='Whether the driver needs a smart phone to do '
                'this job (for example, if you need them to run an app).')

    comments = models.TextField(
                    blank=True,
                    help_text='Anything else to tell the driver.')

    objects = JobRequestQuerySet.as_manager()

    def __unicode__(self):
        return self.reference_number

    @property
    def driver_pay_per_hour(self):
        "Returns the driver pay per hour for this job."
        return client_to_driver_rate(self.client_pay_per_hour)

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
    vehicle_types = models.ManyToManyField(VehicleType,
           related_name='jobrequests',
           help_text="Which types of vehicle would be appropriate for the job. "
            "(N.B. if you require a specific mixture of vehicles, "
            "such as one car and one van, then you should create these as "
            "separate bookings.)")
    minimum_delivery_box = models.PositiveSmallIntegerField(
            choices=DriverVehicleType.DELIVERY_BOX_CHOICES,
            default=DriverVehicleType.DELIVERY_BOX_NONE,
            help_text='For scooters, motorcycles and bicycles, '
                        'the minimum delivery box size.')

    driving_experience = models.PositiveSmallIntegerField(
                                'Minimum driving experience',
                                choices=Driver.DRIVING_EXPERIENCE_CHOICES,
                                default=Driver.DRIVING_EXPERIENCE_LESS_ONE)

    own_vehicle = models.BooleanField(
                            'The driver must supply their own vehicle.',
                            default=True)

    objects = DriverJobRequestManager.from_queryset(JobRequestQuerySet)()
