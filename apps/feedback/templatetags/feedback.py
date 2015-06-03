from django import template
from ..models import BookingFeedback
from django.conf import settings
from apps.main.templatetags.icons import icon
from django.contrib.admin.templatetags.admin_list import items_for_result


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


def split_score(score):
    """Splits a score (which can be a decimal or integer) into 
    a list of constituent units.
    
    E.g.:
        split_score(3.7) = [1, 1, 1, 0.7, 0]
    """
    items = []
    for i in range(BookingFeedback.MAX_SCORE):
        difference = i + 1 - score
        if difference <= 0:
            items.append(1)
        elif difference < 1:
            items.append(difference)
        else:
            items.append(0)
    return items


@register.inclusion_tag('feedback/includes/feedback_score.html')
def feedback_score(score, for_email=False):
    """Outputs the given score using icons.
    
    Can optionally specify whether it's for including in an email.  If it is,
    the icons will be shown as images instead.
    
    Usage:
    
        {% feedback_score feedback.score %}
    """
    context = {'score': score,
               'for_email': for_email}
    if score:
        context['split_score'] = split_score(score)
    return context


@register.inclusion_tag('feedback/includes/feedback_score.html')
def average_score(score, for_email=False):
    """Outputs the average score using icons.

    Can optionally specify whether it's for including in an email.  If it is,
    the icons will be shown as images instead.

    
    Usage:
    
        {% average_score feedback.average_score %}
    """
    context = {'score': score,
               'for_email': for_email,
               'include_value': True}
    if score:
        context['split_score'] = split_score(score)
    return context


@register.inclusion_tag('feedback/includes/feedback_icon.html')
def feedback_icon(unit, for_email=False):
    """Outputs an icon or image suitable for the unit supplied;
    Unit is 0, 1 or a fraction.
    If for_email is True, output as an image instead.
    """
    if unit == 1:
        name = 'score_full'
    elif unit == 0:
        name = 'score_empty'
    else:
        name = 'score_half'
    context = {'for_email': for_email}
    if for_email:
        context['image_path'] = 'img/email/feedback/%s.png' % name
        context['base_url'] = settings.BASE_URL
    else:
        context['icon_name'] = name

    return context
