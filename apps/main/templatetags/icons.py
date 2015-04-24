from django import template
from django.utils.safestring import mark_safe

register = template.Library()


ICON_MAP = {
    'login': 'sign-in',
    'logout': 'sign-out',
    'register': 'user',
    'driver_register': 'motorcycle',
    'driver': 'motorcycle',
    'undo': 'reply',
    'confirm': 'check-circle',
    'user': 'user',
    'account': 'user',
    'forgot': 'question-circle',
    'admin': 'cogs',
    'edit': 'edit',
    'delete': 'trash',
    'password': 'lock',
    'book': 'calendar',
    'date': 'calendar',
    'time': 'clock-o',
    'reset_password': 'undo',
    'dashboard': 'dashboard',
    'driver_profile_view': 'eye',
    'driver_profile_change': 'edit',
    'client_profile_change': 'edit',
    'client': 'briefcase',
    'driverjobrequest_create': 'motorcycle',
    'requested_jobs': 'list',
    'freelancer_bookings': 'list',
    'availability': 'calendar',
    'save': 'check-circle',
    'job_matching': 'search',
    'create': 'plus-circle',
    'vehicletypes': 'car',
    'yes': 'check',
    'no': 'times',
    'location': 'map-marker',
    'search': 'search',
}

@register.filter
def icon(name):
    """Outputs icon markup based on the supplied name.
    
    Usage:
    
        {{ 'foo'|icon }}
    """
    return mark_safe("<i class='fa fa-%s'></i>" % ICON_MAP[name])
