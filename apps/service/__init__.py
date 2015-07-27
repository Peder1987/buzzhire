from apps.core.utils import WeightedRegistry, classproperty
from django.utils.module_loading import autodiscover_modules
from django.utils.encoding import force_text


default_app_config = 'apps.service.config.ServiceConfig'


"""Allows different job request types to be registered with the job app.

Usage:

   # services.py

   from apps.job import services, Service

   class MyService(Service):
       weight = 0
       job_request_model = MyModel
       
   services.register(MyService)
"""

services = WeightedRegistry()


class Service(object):
    """Class for registering different job services.  Apps should subclass
    Service, setting the attributes below and registering them
    as per the documentation above.
    """
    weight = 0
    job_request_model = None
    freelancer_model = None
    freelancer_additional_menu_items = []
    job_matching_form = None

    @classproperty
    def service_name(cls):
        """Human readable version of the service, e.g. 'delivery'.
        """
        return cls.job_request_model.service

    @classproperty
    def freelancer_name(cls):
        """Human readable version of the type of freelancer for this service.
        Should be in the singular version.
        """
        return cls.freelancer_model._meta.verbose_name

    @classproperty
    def freelancer_name_plural(cls):
        """Human readable version used to refer to multiple freelancers
        for this service.
        """
        return force_text(cls.freelancer_model._meta.verbose_name_plural)


def autodiscover():
    """Automatically imports any services.py file in an app.
    """
    autodiscover_modules('services')


def service_from_class(job_request_model_class):
    "Returns the service for the supplied job request class."
    for service in services.values():
        if service.job_request_model == job_request_model_class:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s job_request.' % job_request_model_class)

