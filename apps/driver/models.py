from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer


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
    return self.driver_set.get()
User.driver = property(_driver)


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
    vehicle_types = MultiSelectField(choices=VEHICLE_TYPE_CHOICES)

    motorcycle_licence = models.BooleanField('I have a CBT/full motorcycle license.',
                                             default=False)

    DRIVING_EXPERIENCE_LESS_ONE = '0-1'
    DRIVING_EXPERIENCE_ONE_THREE = '1-3'
    DRIVING_EXPERIENCE_THREE_FIVE = '3-5'
    DRIVING_EXPERIENCE_FIVE_PLUS = '5+'
    DRIVING_EXPERIENCE_CHOICES = (
        (DRIVING_EXPERIENCE_LESS_ONE, 'Less than 1 year'),
        (DRIVING_EXPERIENCE_ONE_THREE, '1 - 3 years'),
        (DRIVING_EXPERIENCE_THREE_FIVE, '3 - 5 year'),
        (DRIVING_EXPERIENCE_FIVE_PLUS, 'More than 5 years'),
    )
    driving_experience = models.CharField(max_length=3,
                                            choices=DRIVING_EXPERIENCE_CHOICES)
    own_vehicle = models.BooleanField('I have my own vehicle',
                                      default=False)
