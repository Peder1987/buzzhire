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


@register.inclusion_tag('feedback/includes/feedback_for_freelancer_own.html')
def feedback_for_freelancer_own(booking):
    """Outputs the client's own feedback for a freelancer, given the booking.
    
    Usage:
    
        {% feedback_for_freelancer_own booking %}
    """
    try:
        feedback = BookingFeedback.objects.client_feedback_from_booking(booking)
    except BookingFeedback.DoesNotExist:
        feedback = None
    return {
        'object': feedback
    }

@register.inclusion_tag('feedback/includes/feedback_for_freelancer_all.html')
def feedback_for_freelancer_all(freelancer):
    """Outputs the all the client feedback for a freelancer.
    
    Usage:
    
        {% feedback_for_freelancer_all freelancer %}
    """
    return {
        'object_list': BookingFeedback.objects.feedback_for_freelancer(
                                                                    freelancer)
    }


@register.inclusion_tag('feedback/includes/feedback_score.html')
def feedback_score(score):
    """Outputs the given score in using icons.
    
    Usage:
    
        {% feedback_score feedback.score %}
    """
    return {'score': score, 'range': range(score)}
