from apps.core.utils import WeightedRegistry
from django.utils.module_loading import autodiscover_modules


default_app_config = 'apps.job.config.JobConfig'


"""Allows different job request types to be registered with the job app.

Usage:

   # services.py

   from apps.job import services, Service

   class MyService(Service):
       weight = 0
       model = MyModel
       
   services.register(MyService)
"""

services = WeightedRegistry()


class Service(object):
    """Class for registering different job services.  Apps should subclass
    Service, setting the attributes below and registering them
    as per the documentation above.
    """
    weight = 0
    model = None


def autodiscover():
    """Automatically imports any services.py file in an app.
    """
    autodiscover_modules('services')


def service_from_job_request(job_request):
    # Returns the service for the supplied job request
    for service in services.values():
        if service.job_request_model == job_request.__class__:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s job_request.' % job_request.__class__)

