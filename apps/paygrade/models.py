from django.db import models
from django.core import validators
from djmoney.models.fields import MoneyField
from decimal import Decimal
from apps.job.models import JobRequest
from django.conf import settings


class BasePayGrade(models.Model):
    """A means of specifying minimum rates of pay for different services.
    
    This is an abstract class that should be subclassed by each service.
    """
    years_experience = models.PositiveSmallIntegerField(
                                'Minimum years of experience',
                                choices=JobRequest.YEARS_EXPERIENCE_CHOICES)

    min_client_pay_per_hour = MoneyField('Minimum client cost per hour',
              max_digits=5, decimal_places=2,
              default_currency='GBP',
              default=Decimal(settings.CLIENT_MIN_WAGE),
              validators=[
                validators.MinValueValidator(settings.CLIENT_MIN_WAGE)])

    def __unicode__(self):
        return '%s: %s at %s' % (self.__class__,
                                 self.years_experience,
                                 self.min_client_pay_per_hour)

    class Meta:
        abstract = True
