from decimal import Decimal
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.core import validators
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from django.contrib.humanize.templatetags.humanize import apnumber
from django.template.defaultfilters import pluralize
from apps.location.models import Postcode
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


class PublishedFreelancerManager(models.GeoManager):
    """Manager for published freelancers.
    Note that models inheriting Freelancer should redeclare it:
    
        class SpecialFreelancer(Freelancer):
            objects = models.Manager()
            published_objects = PublishedFreelancerManager()
    """
    def get_queryset(self):
        return self.model.objects.filter(published=True)
        queryset = super(PublishedFreelancerManager, self).get_queryset()
        return queryset.filter(published=True)


class Freelancer(models.Model):
    "A freelancer is a person offering a professional service."

    published = models.BooleanField(default=True,
        help_text='Whether or not the freelancer shows up in search '
        'results. Note it is still possible for members of the public to '
        'view the freelancer if they know the link.')

    # A link to a user account.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=13, validators=[
            validators.RegexValidator(r'^07[0-9 ]*$',
                           'Please enter a valid UK mobile phone number in '
                           'the form 07xxx xxx xxx')])

    FLUENCY_BASIC = 'BA'
    FLUENCY_CONVERSATIONAL = 'CO'
    FLUENCY_FLUENT = 'FL'
    FLUENCY_NATIVE = 'NA'
    FLUENCY_CHOICES = (
        (FLUENCY_BASIC, 'Basic'),
        (FLUENCY_CONVERSATIONAL, 'Conversational'),
        (FLUENCY_FLUENT, 'Fluent'),
        (FLUENCY_NATIVE, 'Native'),
    )
    english_fluency = models.CharField(max_length=2, choices=FLUENCY_CHOICES)
    eligible_to_work = models.BooleanField('I am eligible to work in the UK.',
                                           default=False)

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
    phone_type = models.CharField(max_length=2, choices=PHONE_TYPE_CHOICES,
                                  blank=True)

    DAYS_OF_WEEK_CHOICES = [(calendar.day_abbr[i].lower(),
                               calendar.day_name[i]) for i in range(7)]
    days_available = MultiSelectField(
                'Which days of the week are you available to work?',
                choices=DAYS_OF_WEEK_CHOICES,
                blank=True)

    HOURS_AVAILABLE_MORNINGS = 'MO'
    HOURS_AVAILABLE_AFTERNOONS = 'AF'
    HOURS_AVAILABLE_EVENINGS = 'EV'
    HOURS_AVAILABLE_NIGHT = 'NI'
    HOURS_AVAILABLE_CHOICES = (
        (HOURS_AVAILABLE_MORNINGS, 'Mornings'),
        (HOURS_AVAILABLE_AFTERNOONS, 'Afternoons'),
        (HOURS_AVAILABLE_EVENINGS, 'Evenings'),
        (HOURS_AVAILABLE_NIGHT, 'Night'),
    )
    # Mornings, Afternoons, Evenings, Night, Flexible
    hours_available = MultiSelectField(
                            'What are your preferred working hours?',
                            choices=HOURS_AVAILABLE_CHOICES,
                            blank=True)

    minimum_pay_per_hour = MoneyField(max_digits=5, decimal_places=2,
                  default_currency='GBP', default=Decimal(8.50),
                  help_text='The minimum pay per hour you will accept.')

    postcode = models.ForeignKey(Postcode, blank=True, null=True)

    DISTANCE_CHOICES = [(i, "%s mile%s" % (str(apnumber(i)).capitalize(),
                                           pluralize(i))) \
                                        for i in (1, 2, 5, 10, 20, 50)]
    travel_distance = models.PositiveSmallIntegerField(
        choices=DISTANCE_CHOICES, default=5,
        help_text='The maximum distance you are prepared to travel to a job.')

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()

    @property
    def reference_number(self):
        "Returns a reference number for this freelancer."
        return 'FR%s' % str(self.pk).zfill(7)

    def get_full_name(self):
        "Returns the full name of the freelancer."
        return '%s %s' % (self.first_name,
                          self.last_name)

    def __unicode__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('freelancer_detail', args=(self.pk,))

    class Meta:
        ordering = 'last_name',
