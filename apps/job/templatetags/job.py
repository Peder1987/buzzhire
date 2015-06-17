from django import template
from ..models import JobRequest
from django.utils.safestring import mark_safe
from .. import services
from django.template.loader import render_to_string


register = template.Library()


STATUS_MAP = {
    JobRequest.STATUS_OPEN: {
        'color': 'primary',
        'icon': 'circle-o'
    },
    JobRequest.STATUS_CONFIRMED: {
        'color': 'success',
        'icon': 'check',
    },
    JobRequest.STATUS_CHECKOUT: {
        'color': 'warning',
        'icon': 'cart',
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

@register.assignment_tag
def get_services():
    """Assignment tag for getting the registered services.
    
    Usage:
    
        {% get_services as services %}
        {% for service in services %}
            {# Do something #}
        {% endfor %} 
    """
    return services.values()


@register.simple_tag
def job_request_summary(job_request):
    """Outputs a summary of the supplied job request.
    Usage:
    
        {% job_request_summary object %}
    """
    template_name = '%s/includes/%s_summary.html' % (
                                            job_request._meta.app_label,
                                            job_request._meta.model_name)
    return render_to_string(template_name, {'object': job_request})
