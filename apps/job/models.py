from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import date, datetime
from django.core import validators
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from apps.driver.models import Driver, VehicleType, \
                                DriverVehicleType, FlexibleVehicleType
from apps.client.models import Client
from apps.location.models import Postcode
from apps.freelancer.models import client_to_freelancer_rate
from decimal import Decimal
from django_fsm import FSMField, transition
from boto.ec2.instancestatus import Status


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
    STATUS_OPEN = 'OP'  # Client has paid; the job request now ready for booking
    STATUS_CONFIRMED = 'CF'  # Freelancers have been assigned
    STATUS_COMPLETE = 'CP'  # The work has been completed
    STATUS_CHECKOUT = 'IC'  # The client has not yet paid
    STATUS_CANCELLED = 'CA'  # Job request cancelled
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_CHECKOUT, 'In checkout'),
        (STATUS_CANCELLED, 'Cancelled'),
    )
    status = FSMField(max_length=2, choices=STATUS_CHOICES,
                              default=STATUS_CHECKOUT, protected=True)

    @transition(field=status, source=STATUS_CHECKOUT, target=STATUS_OPEN,
                custom={'button_name':'Open'})
    def open(self):
        """Marks a job as open.
        NB be wary of changing this method name as it will affect the
        way receivers handle the signals."""
        pass

    @transition(field=status, source=[STATUS_CONFIRMED, STATUS_COMPLETE,
                        STATUS_CANCELLED, STATUS_OPEN], target=STATUS_CHECKOUT,
                custom={'button_name':'Back to checkout'})
    def back_to_checkout(self):
        """Marks a job as in the checkout again
        (unlikely to need this transition, but just in case)."""
        pass

    @transition(field=status, source=STATUS_OPEN, target=STATUS_CONFIRMED,
                custom={'button_name':'Confirm'})
    def confirm(self):
        """Marks a job as confirmed - i.e. the freelancers are all booked.
        Note because of the decorator, this method doesn't need to do anything,
        just avoid raising an exception."""
        pass

    @transition(field=status, source=[STATUS_CONFIRMED, STATUS_COMPLETE,
                                        STATUS_CANCELLED], target=STATUS_OPEN,
                custom={'button_name':'Reopen'})
    def reopen(self):
        "Marks a job as open - i.e. it needs some freelancers to be booked in."
        pass

    @transition(field=status, source=[STATUS_OPEN, STATUS_CHECKOUT],
                target=STATUS_CANCELLED,
                custom={'button_name':'Cancel'})
    def cancel(self):
        "Marks a job as cancelled."
        pass

    @transition(field=status, source=STATUS_CONFIRMED,
                target=STATUS_COMPLETE,
                custom={'button_name':'Complete'})
    def complete(self):
        "Marks a job as complete - the job has been performed."
        pass

    # The date this form was submitted
    date_submitted = models.DateTimeField(auto_now_add=True)

    client_pay_per_hour = MoneyField('Pay per hour',
                  max_digits=5, decimal_places=2,
                  default_currency='GBP',
                  default=Decimal(settings.CLIENT_MIN_WAGE),
                  help_text='How much you will pay per hour, for each driver.',
                  validators=[
                    validators.MinValueValidator(settings.CLIENT_MIN_WAGE)])

    tips_included = models.BooleanField('Inclusive of tips', default=False,
                                        blank=False)

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
    postcode = models.ForeignKey(Postcode)


    PHONE_REQUIREMENT_NOT_REQUIRED = 'NR'
    PHONE_REQUIREMENT_ANY = 'AY'
    PHONE_REQUIREMENT_ANDROID = 'AN'
    PHONE_REQUIREMENT_IPHONE = 'IP'
    PHONE_REQUIREMENT_WINDOWS = 'WI'

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
    def freelancer_pay_per_hour(self):
        "Returns the freelancer pay per hour for this job."
        return client_to_freelancer_rate(self.client_pay_per_hour)

    @property
    def client_total_cost(self):
        "Returns the total cost to the client for this job."
        return self.client_pay_per_hour * self.duration \
                * self.number_of_freelancers

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
    # To delete
    vehicle_types_old = models.ManyToManyField(VehicleType,
           related_name='jobrequests_old', blank=True, null=True)

    vehicle_type = models.ForeignKey(FlexibleVehicleType,
           related_name='jobrequests',
           blank=True, null=True,
           help_text="Which type of vehicle would be appropriate for the job. ")

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

    def get_vehicle_type_display(self):
        "Returns the vehicle type, or 'Any' if there is none."
        if self.vehicle_type:
            return self.vehicle_type
        return 'Any'