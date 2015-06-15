from django import template

register = template.Library()

PHOTO_DIMENSIONS = {
    'tiny': '20x20',
    'small': '54x70',
    'medium': '75x97',
    'large': '233x300',
}

@register.inclusion_tag('freelancer/includes/profile_photo.html')
def profile_photo(freelancer, size='medium', for_email=False):
    """Renders the freelancer's profile photo, or a default image.
    
    For emails, optionally provide the base_url.
    
    Usage:
        {% profile_photo object 'large' %}
    
    Or for emails:
    
        {% profile_photo object for_email=True %}
    
    """

    return {
        'object': freelancer,
        'dimensions': PHOTO_DIMENSIONS[size],
        'for_email': for_email,
    }

