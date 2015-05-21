from django.db import models
from django.core import validators
from apps.booking.models import Booking


class BookingFeedback(models.Model):
    """A feedback associated with a booking, for a client or freelancer."""
    AUTHOR_TYPE_CLIENT = 'CL'
    AUTHOR_TYPE_FREELANCER = 'FR'
    AUTHOR_TYPE_CHOICES = (
        (AUTHOR_TYPE_CLIENT, 'Client'),
        (AUTHOR_TYPE_FREELANCER, 'Freelancer'),
    )

    author_type = models.CharField(max_length=2,
              choices=AUTHOR_TYPE_CHOICES,
              help_text='Whether the author of the feedback is '
                            'the client or the freelancer.')
    booking = models.ForeignKey(Booking)

    score = models.PositiveSmallIntegerField(
                            validators=[validators.MinValueValidator(1),
                                        validators.MaxValueValidator(5)])
