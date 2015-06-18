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
    'clear': 'times',
    'password': 'lock',
    'book': 'calendar',
    'date': 'calendar',
    'time': 'clock-o',
    'reset_password': 'undo',
    'dashboard': 'dashboard',
    'freelancer_profile_view': 'eye',
    'freelancer_profile_change': 'edit',
    'client_profile_change': 'edit',
    'client': 'briefcase',
    'job_request_create': 'plus-circle',
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
    'right_arrow': 'arrow-circle-right',
    'phone': 'phone',
    'pay': 'check-circle',
    'photo': 'camera-retro',
    'upload': 'upload',
    'feedback': 'comment-o',
    'score_full': 'star',
    'score_empty': 'star-o',
    'score_half': 'star-half-o',
    'invitation': 'paper-plane-o',
    'chef': 'cutlery',
}

@register.filter
def icon(name):
    """Outputs icon markup based on the supplied name.
    
    Usage:
    
        {{ 'foo'|icon }}
    """
    return mark_safe("<i class='fa fa-%s'></i>" % ICON_MAP[name])
