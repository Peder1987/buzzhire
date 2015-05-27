from django.db import models
from django.core import validators
from apps.booking.models import Booking

class FakeQuerySet(list):
    ordered = True

class BookingFeedbackManager(models.Manager):
    "Model manager for BookingFeedbacks."

    def feedback_list(self, job_request):
        """Returns a list of non-saved BookingFeedback objects for the
        job request.
        """
        feedback_list = FakeQuerySet()
        for booking in job_request.bookings.all():
            feedback = BookingFeedback(
                booking=booking,
                author_type=BookingFeedback.AUTHOR_TYPE_CLIENT
            )
            feedback_list.append(feedback)

        return feedback_list


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

    comment = models.TextField(blank=True)

    objects = BookingFeedbackManager()

    def get_target(self):
        "Returns the client / freelancer that the feedback is for."
        MAP = {
            self.AUTHOR_TYPE_CLIENT:
                    lambda booking: booking.freelancer,
            self.AUTHOR_TYPE_FREELANCER:
                    lambda booking: booking.jobrequest.client,
        }
        return MAP[self.author_type](self.booking)
