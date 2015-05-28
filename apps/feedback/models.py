from django.db import models
from django.core import validators
from apps.booking.models import Booking


class FakeQuerySet(list):
    """An object that can be used to 'fake' a queryset, but which is actually a
    list of, for example, unsaved model instances.
    """
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

    def client_feedback_exists(self, job_request):
        """Returns whether or not client feedback exists for the supplied
        job request.
        """
        return self.filter(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                           booking__jobrequest=job_request).exists()

    def client_feedback_from_booking(self, booking):
        """Returns the BookingFeedback given by the client for the supplied
        booking.  Raises DoesNotExist on failure.
        """
        return self.get(author_type=BookingFeedback.AUTHOR_TYPE_CLIENT,
                        booking=booking)


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

    TARGET_MAP = {
        AUTHOR_TYPE_CLIENT:
                lambda booking: booking.freelancer,
        AUTHOR_TYPE_FREELANCER:
                lambda booking: booking.jobrequest.client,
    }

    def get_target(self):
        "Returns the client / freelancer that the feedback is for."
        return self.TARGET_MAP[self.author_type](self.booking)

    def get_author(self):
        "Returns the client / freelancer who authored the feedback."
        # Just get the opposite author type so we can use the TARGET_MAP
        opposite_author_type = [i for i in self.TARGET_MAP.keys()
                               if i != self.author_type][0]
        return self.TARGET_MAP[opposite_author_type](self.booking)
