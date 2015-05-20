from django import template

register = template.Library()


@register.inclusion_tag('freelancer/includes/profile_photo.html')
def profile_photo(freelancer, size='medium'):
    """Renders the freelancer's profile photo, or a default image.
    
    Usage:
        {% profile_photo object 'large' %}
    
    """
    DIMENSIONS = {
        'small': '75x97',
        'medium': '150x193',
        'large': '233x300',
    }
    return {
        'object': freelancer,
        'dimensions': DIMENSIONS[size],
        'width': '150',
        'height': '193',
    }

