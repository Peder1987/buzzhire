from apps.core.utils import WeightedRegistry, classproperty
from django.utils.module_loading import autodiscover_modules
from apps.service import services

default_app_config = 'apps.job.config.JobConfig'


def service_from_class(job_request_model_class):
    "Returns the service for the supplied job request class."
    for service in services.values():
        if service.job_request_model == job_request_model_class:
            return service
    raise ValueError('Could not get find a service registered for '
                     '%s job_request.' % job_request_model_class)

