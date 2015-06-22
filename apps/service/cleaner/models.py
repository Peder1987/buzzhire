from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.job.models import JobRequest

CLEANER_SERVICE_TITLE = 'cleaner'


class CleanerJobRequest(JobRequest):
    """A JobRequest that is specifically for a cleaner to complete.
    """
    service = CLEANER_SERVICE_TITLE


class Cleaner(Freelancer):
    "A waiting staff is a type of freelancer."

    service = CLEANER_SERVICE_TITLE

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()
