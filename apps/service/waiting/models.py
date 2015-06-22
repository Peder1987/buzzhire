from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.job.models import JobRequest

WAITING_SERVICE_TITLE = 'waiting staff'


class WaitingJobRequest(JobRequest):
    """A JobRequest that is specifically for waiting staff to complete.
    """
    service = WAITING_SERVICE_TITLE


class WaitingFreelancer(Freelancer):
    "A waiting staff is a type of freelancer."

    service = WAITING_SERVICE_TITLE

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()
