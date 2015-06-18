from apps.core.utils import WeightedRegistry, classproperty
from django.utils.module_loading import autodiscover_modules


default_app_config = 'apps.job.config.JobConfig'


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

    @classproperty
    def title(cls):
        """Human readable version of the service.  Should be the name of
        the kind of person that performs the service.
        """
        return cls.job_request_model.service


def autodiscover():
    """Automatically imports any services.py file in an app.
    """
    autodiscover_modules('services')


def service_from_class(job_request_model_class):
    # Returns the service for the supplied job request class
    for service in services.values():
        if service.job_request_model == job_request_model_class:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s job_request.' % job_request_model_class)

