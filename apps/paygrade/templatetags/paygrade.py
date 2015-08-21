from django import template
from django.core.urlresolvers import reverse
from django.conf import settings


register = template.Library()

@register.simple_tag
def min_pay_ajax_endpoint(service_name):
    """Includes the endpoint for getting the minimum pay by ajax.
    {% min_ajax_endpoint 'driver' %}
    """
    url_name = settings.PAY_GRADE_REVERSE_URL % {'service': service_name}
    return reverse(url_name)

