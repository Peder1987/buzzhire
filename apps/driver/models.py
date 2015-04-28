from django.contrib.gis.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer, PublishedFreelancerManager


def _is_driver(self):
    """Custom method on User model.
    Returns whether or not the user account is a driver account,
    i.e. has a driver profile.
    ."""
    return Driver.objects.filter(user=self).exists()
User.is_driver = property(_is_driver)


def _driver(self):
    """Custom method on User model.
    Returns the Freelancer for the user.  If it doesn't, raises
    Freelancer.DoesNotExist.
    """
    return Driver.objects.get(user=self)
User.driver = property(_driver)


class VehicleType(models.Model):
    """A type of vehicle that the driver may drive.
    """
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Driver(Freelancer):
    "A driver is a freelancer whose service is driving."

    VEHICLE_TYPE_MOTORCYCLE = 'MC'
    VEHICLE_TYPE_BICYCLE = 'BI'
    VEHICLE_TYPE_CAR = 'CA'
    VEHICLE_TYPE_VAN = 'VA'
    VEHICLE_TYPE_CHOICES = (
        (VEHICLE_TYPE_BICYCLE, 'Bicycle'),
        (VEHICLE_TYPE_MOTORCYCLE, 'Motorcycle/scooter'),
        (VEHICLE_TYPE_CAR, 'Car'),
        (VEHICLE_TYPE_VAN, 'Van'),
    )
    vehicle_types_old = MultiSelectField(choices=VEHICLE_TYPE_CHOICES,
                                         blank=True)

    vehicle_types = models.ManyToManyField(VehicleType,
             verbose_name='Vehicles',
             through='DriverVehicleType',
             blank=True,
             related_name='drivers',
             help_text='Which vehicles you are able and licensed to drive. '
                    'You do not need to provide the vehicle for the booking.')

    # TODO - remove
    motorcycle_licence = models.BooleanField('I have a CBT/full motorcycle license.',
                                             default=False)

    # The integer stored in driving experience denotes that they have
    # AT LEAST that number of years driving experience.
    DRIVING_EXPERIENCE_LESS_ONE = 0
    DRIVING_EXPERIENCE_ONE = 1
    DRIVING_EXPERIENCE_THREE = 3
    DRIVING_EXPERIENCE_FIVE = 5
    DRIVING_EXPERIENCE_CHOICES = (
        (DRIVING_EXPERIENCE_LESS_ONE, 'Less than 1 year'),
        (DRIVING_EXPERIENCE_ONE, '1 - 3 years'),
        (DRIVING_EXPERIENCE_THREE, '3 - 5 years'),
        (DRIVING_EXPERIENCE_FIVE, 'More than 5 years'),
    )
    # Legacy field - to be deleted once has migrated
    driving_experience_old = models.CharField(blank=True,
                                            max_length=3,
                                            choices=DRIVING_EXPERIENCE_CHOICES)
    driving_experience = models.PositiveSmallIntegerField(default=1,
                                        choices=DRIVING_EXPERIENCE_CHOICES)

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()

    def get_absolute_url(self):
        return reverse('driver_detail', args=(self.pk,))


class DriverVehicleTypeQuerySet(models.QuerySet):
    "Custom queryset for DriverVehicleTypes."

    def owned(self):
        """Filter by driver vehicles that the driver can provide for a booking.
        """
        return self.filter(own_vehicle=True)


class DriverVehicleType(models.Model):
    """'Through' model for storing information for a driver about
    a particular vehicle.
    """
    driver = models.ForeignKey(Driver)
    vehicle_type = models.ForeignKey(VehicleType,
        help_text='Note: you may only create one vehicle of each type.')

    own_vehicle = models.BooleanField(
                            'I can provide this vehicle on a job.',
                            default=False)
    # We store deliver box sizes as integers so we can do simple
    # greater than / less than searches
    DELIVERY_BOX_NONE = 0
    DELIVERY_BOX_STANDARD = 2
    DELIVERY_BOX_PIZZA = 4
    DELIVERY_BOX_CHOICES = (
        (DELIVERY_BOX_NONE, 'None'),
        (DELIVERY_BOX_STANDARD, 'Standard'),
        (DELIVERY_BOX_PIZZA, 'Pizza'),
    )
    delivery_box = models.PositiveSmallIntegerField(
                'Minimum delivery box size', choices=DELIVERY_BOX_CHOICES,
                default=DELIVERY_BOX_NONE,
                help_text='What size delivery box does your vehicle have? '
                    '(Scooters, motorcycles and bicycles only.)')

    objects = DriverVehicleTypeQuerySet.as_manager()

    def __unicode__(self):
        return unicode(self.vehicle_type)

    class Meta:
        unique_together = ('driver', 'vehicle_type')
        ordering = ('vehicle_type__title',)
