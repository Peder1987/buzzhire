from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.job.models import JobRequest

BAR_SERVICE_TITLE = 'bar staff'


class BarJobRequest(JobRequest):
    """A JobRequest that is specifically for bar staff to complete.
    """
    service = BAR_SERVICE_TITLE


class BarFreelancer(Freelancer):
    "A bar staff is a type of freelancer."

    service = BAR_SERVICE_TITLE

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()
