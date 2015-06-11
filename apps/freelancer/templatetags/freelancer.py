from django import template

register = template.Library()

PHOTO_DIMENSIONS = {
    'tiny': '20x20',
    'small': '54x70',
    'medium': '75x97',
    'large': '233x300',
}

@register.inclusion_tag('freelancer/includes/profile_photo.html')
def profile_photo(freelancer, size='medium', base_url=''):
    """Renders the freelancer's profile photo, or a default image.
    
    For emails, optionally provide the base_url.
    
    Usage:
        {% profile_photo object 'large' %}
    
    Or for emails:
    
        {% profile_photo object 'http://domain.co/' %}
    
    """

    return {
        'object': freelancer,
        'dimensions': PHOTO_DIMENSIONS[size],
        'base_url': base_url,
    }

