from django import template
from ..models import Booking, Availability
from ..forms import AvailabilityForm

register = template.Library()

@register.filter
def booking_exists_for_freelancer(jobrequest, freelancer):
    """Returns whether or not the freelancer is booked onto
    this job request.
    
    Usage:
        {% if jobrequest|booking_exists_for_freelancer:freelancer %}
            <p>Booking exists!</p>
        {% endif %}
    """
    return Booking.objects.filter(jobrequest=jobrequest,
                                  freelancer=freelancer).exists()

@register.filter
def availability_form_for_freelancer(freelancer):
    """Returns an availability form for the supplied freelancer,
    or False if it hasn't been filled out yet.
    """
    try:
        availability = freelancer.availability
    except Availability.DoesNotExist:
        return False
    return AvailabilityForm(instance=availability)
