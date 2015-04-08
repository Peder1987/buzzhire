from django.db import models
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
    vehicle_types = models.ManyToManyField(VehicleType, related_name='drivers')

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

    own_vehicle = models.BooleanField('I have my own vehicle',
                                      default=False)

    objects = models.Manager()
    published_objects = PublishedFreelancerManager()
