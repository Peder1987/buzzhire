from django.contrib.gis.db import models
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from apps.job.models import JobRequest

BAR_SERVICE_TITLE = 'bar staff'

ROLE_MIXOLOGIST = 'MX'
ROLE_BARMAN = 'BM'
ROLE_BARISTA = 'BT'

ROLE_CHOICES = (
    (ROLE_BARMAN, 'Barman'),
    (ROLE_MIXOLOGIST, 'Mixologist'),
    (ROLE_BARISTA, 'Barista'),
)

class BarJobRequest(JobRequest):
    """A JobRequest that is specifically for bar staff to complete.
    """
    service = BAR_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_BARMAN,
                                     choices=ROLE_CHOICES)

class BarFreelancer(Freelancer):
    "A bar staff is a type of freelancer."

    service = BAR_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_BARMAN,
                                     choices=ROLE_CHOICES)

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()
