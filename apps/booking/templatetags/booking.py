from django import template
from ..models import Booking


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
