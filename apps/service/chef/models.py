from django.contrib.gis.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from django.core.urlresolvers import reverse
from apps.job.models import JobRequest, JobRequestQuerySet


CERTIFICATION_CHEF = 'CH'
CERTIFICATION_SOUS_CHEF = 'SC'
CERTIFICATION_ASSISTANT = 'KA'
CERTIFICATION_PORTER = 'PO'

CERTIFICATION_CHOICES = (
    (CERTIFICATION_CHEF, 'Chef'),
    (CERTIFICATION_SOUS_CHEF, 'Sous chef'),
    (CERTIFICATION_ASSISTANT, 'Kitchen assistant'),
    (CERTIFICATION_PORTER, 'Kitchen porter'),
)

CHEF_SERVICE_TITLE = 'kitchen staff'

class ChefJobRequest(JobRequest):
    """A JobRequest that is specifically for chefs to complete.
    """
    service = CHEF_SERVICE_TITLE

    certification = models.CharField(max_length=2,
                                     default=CERTIFICATION_CHEF,
                                     choices=CERTIFICATION_CHOICES)


class Chef(Freelancer):
    "A chef is a type of freelancer."

    service = CHEF_SERVICE_TITLE

    certification = models.CharField(max_length=2,
                                     default=CERTIFICATION_CHEF,
                                     choices=CERTIFICATION_CHOICES)

    objects = models.GeoManager()
    published_objects = PublishedFreelancerManager()
