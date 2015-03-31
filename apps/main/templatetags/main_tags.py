from django import template

register = template.Library()


@register.filter
def is_in_dashboard(path):
    """Returns whether or not the supplied path should be treated
    as within the dashboard.  Used to decide whether or not to 
    show links as active.
    
    Usage:
    
        <a{% if request.path|is_in_dashboard %} class='active'{% endif %}>
    """
    return True
