from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def min_pay_ajax_endpoint():
    """Includes the endpoint for getting the minimum pay by ajax.
    """
    return reverse('paygrade_get_min_pay')

