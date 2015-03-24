from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.core import validators
from multiselectfield import MultiSelectField
import calendar

def _is_freelancer(self):
    """Custom method on User model.
    Returns whether or not the user account is a freelancer account,
    i.e. has a freelancer profile.
    ."""
    return Freelancer.objects.filter(user=self).exists()
User.is_freelancer = property(_is_freelancer)


def _freelancer(self):
    """Custom method on User model.
    Returns the Freelancer for the user.  If it doesn't, raises
    Freelancer.DoesNotExist.
    """
    return self.freelancer_set.get()
User.freelancer = property(_freelancer)


class Freelancer(models.Model):
    "A freelancer is a person offering a professional service."

    published = models.BooleanField(default=False,
        help_text='Whether or not the freelancer shows up in search '
        'results. Note it is still possible for members of the public to '
        'view the freelancer if they know the link.')

    # A link to a user account.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    name = models.CharField(max_length=60)
    mobile = models.CharField(max_length=13, validators=[
            validators.RegexValidator(r'^07[0-9 ]*$',
                           'Please enter a valid UK mobile phone number in '
                           'the form 07xxx xxx xxx')])

    FLUENCY_BASIC = 'BA'
    FLUENCY_CONVERSATIONAL = 'CO'
    FLUENCY_FLUENT = 'FL'
    FLUENCY_NATIVE = 'NA'
    FLUENCY_CHOICES = (
        (FLUENCY_BASIC, 'Basic',)
        (FLUENCY_CONVERSATIONAL, 'Conversational',)
        (FLUENCY_FLUENT, 'Fluent',)
        (FLUENCY_NATIVE, 'Native',)
    )
    english_fluency = models.ChoiceField(max_length=2, choices=FLUENCY_CHOICES)
    eligible_to_work = models.BooleanField('I am eligible to work in the UK.')


    PHONE_TYPE_ANDROID = 'AN'
    PHONE_TYPE_IPHONE = 'IP'
    PHONE_TYPE_WINDOWS = 'WI'
    PHONE_TYPE_OTHER = 'OT'
    PHONE_TYPE_NON_SMARTPHONE = 'NS'
    PHONE_TYPE_CHOICES = (
        (PHONE_TYPE_ANDROID, 'Android'),
        (PHONE_TYPE_IPHONE, 'iPhone'),
        (PHONE_TYPE_WINDOWS, 'Windows'),
        (PHONE_TYPE_OTHER, 'Other smartphone'),
        (PHONE_TYPE_NON_SMARTPHONE, 'Non smartphone'),
    )
    phone_type = models.ChoiceField(max_length=2, choices=PHONE_TYPE_CHOICES,
                                  blank=True)

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
    vehicle_types = MultiSelectField(max_length=2,
                                     choices=VEHICLE_TYPE_CHOICES)

    motorcycle_licence = models.BooleanField(
        help_text='If you are a motorcycle/scooter driver, do you have your'
        'CBT/full motorcycle license? ')

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
    driving_experience = models.ChoiceField(max_length=3,
                                            choices=DRIVING_EXPERIENCE_CHOICES)
    own_vehicle = models.BooleanField('Do you have your own vehicle?')

    DAYS_OF_WEEK_CHOICES = [(calendar.day_abbr[i].lower(),
                               calendar.day_name[i]) for i in range(7)]
    days_available = MultiSelectField(max_length=3,
                                      choices=DAYS_OF_WEEK_CHOICES,
                help_text='Which days of the week are you available to work?',
                blank=True)

    HOURS_AVAILABLE_MORNINGS = 'MO'
    HOURS_AVAILABLE_AFTERNOONS = 'AF'
    HOURS_AVAILABLE_EVENINGS = 'EV'
    HOURS_AVAILABLE_NIGHT = 'NI'
    HOURS_AVAILABLE_FLEXIBLE = 'FL'
    HOURS_AVAILABLE_CHOICES = (
        (HOURS_AVAILABLE_MORNINGS)
    )
    # Mornings, Afternoons, Evenings, Night, Flexible
    hours_available = MultiSelectField(
                            max_length=2,
                            choices=HOURS_AVAILABLE_CHOICES,
                            help_text='What are your preferred working hours?',
                            blank=True)



    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('freelancer_detail', kwargs={'slug': self.slug})

    def years_since_accreditation(self):
        "Returns the number of years since accreditation."
        if self.accreditation_year:
            return date.today().year - self.accreditation_year
        return None


    def save(self, *args, **kwargs):
        # Make the slug unique
        rebuild_slug = kwargs.pop('rebuild_slug', False)
        if not self.pk or rebuild_slug:
            unique_slugify(self, str(self))
        return super(Freelancer, self).save(*args, **kwargs)

    class Meta:
        ordering = 'last_name',
