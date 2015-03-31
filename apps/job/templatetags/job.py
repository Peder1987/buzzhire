from django import template
from ..models import JobRequest
from django.utils.safestring import mark_safe

register = template.Library()

STATUS_MAP = {
    JobRequest.STATUS_NEW: {
        'color': 'primary',
        'icon': 'circle-o'
    },
    JobRequest.STATUS_OPEN: {
        'color': 'success',
        'icon': 'check',
    },
    JobRequest.STATUS_FOLLOW_UP: {
        'color': 'warning',
        'icon': 'clock-o',
    },
    JobRequest.STATUS_CANCELLED: {
        'color': 'danger',
        'icon': 'close',
    },
    JobRequest.STATUS_COMPLETE: {
        'color': 'info',
        'icon': 'check-square-o',
    },
}


@register.filter
def jobrequest_status_color(status):
    """Returns a color suffix that should be added to the css class for
    the job request status, e.g. 'danger'.  This is used to get things
    a standard colour for each status.
    
    Usage:
    
        <a class='btn btn-{{ object.status|jobrequest_status_color }}'>
    """
    return STATUS_MAP[status]['color']


@register.filter
def jobrequest_status_icon(status):
    """Returns the icon that should be applied to the job request status.
    
    Usage:
    
        {{ object.status|jobrequest_status_icon }}
    """
    return mark_safe('<i class="fa fa-%s"></i>' % STATUS_MAP[status]['icon'])

