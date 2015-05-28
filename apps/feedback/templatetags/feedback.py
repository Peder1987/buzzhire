from django import template
from ..models import BookingFeedback


register = template.Library()

@register.filter
def client_feedback_exists(job_request):
    """Returns whether or not the client has given feedback on the job request.
    
    Usage:
        {% if object|client_feedback_exists %}
            ...
        {% endif %}
    """
    return BookingFeedback.objects.client_feedback_exists(job_request)


@register.inclusion_tag('feedback/includes/client_feedback.html')
def client_feedback(booking):
    """Outputs the client's feedback, give the booking.
    
    Usage:
    
        {% client_feedback booking %}
    """
    try:
        feedback = BookingFeedback.objects.client_feedback_from_booking(booking)
    except BookingFeedback.DoesNotExist:
        feedback = None
    return {
        'object': feedback
    }


@register.inclusion_tag('feedback/includes/feedback_score.html')
def feedback_score(score):
    """Outputs the given score in using icons.
    
    Usage:
    
        {% feedback_score feedback.score %}
    """
    return {'score': score, 'range': range(score)}
