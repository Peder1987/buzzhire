from django.contrib.gis.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from django.core.urlresolvers import reverse
from apps.job.models import JobRequest, JobRequestQuerySet
from apps.core.models import GeoPolymorphicManager


ROLE_CHEF = 'CH'
ROLE_ASSISTANT = 'KA'
ROLE_PORTER = 'PO'

ROLE_CHOICES = (
    (ROLE_CHEF, 'Chef'),
    (ROLE_ASSISTANT, 'Kitchen assistant'),
    (ROLE_PORTER, 'Kitchen porter'),
)

KITCHEN_SERVICE_TITLE = 'kitchen staff'



class KitchenJobRequest(JobRequest):
    """A JobRequest that is specifically for kitchen staff to complete.
    """
    service = KITCHEN_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_CHEF,
                                     choices=ROLE_CHOICES)


class KitchenFreelancer(Freelancer):
    "A kitchen staff is a type of freelancer."

    service = KITCHEN_SERVICE_TITLE

    role = models.CharField(max_length=2,
                                     default=ROLE_CHEF,
                                     choices=ROLE_CHOICES)

    objects = GeoPolymorphicManager()
    published_objects = PublishedFreelancerManager()


    class Meta:
        verbose_name = 'chef'
        verbose_name_plural = 'kitchen staff'