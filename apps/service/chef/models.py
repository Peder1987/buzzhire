from django.contrib.gis.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer, PublishedFreelancerManager
from django.core.urlresolvers import reverse
from apps.job.models import JobRequest, JobRequestQuerySet


class ChefJobRequest(JobRequest):
    """A JobRequest that is specifically for chefs to complete.
    """
    service = 'chef'

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
    certification = models.CharField(max_length=2,
                                     default=CERTIFICATION_CHEF,
                                     choices=CERTIFICATION_CHOICES)

    # TODO - make generic
    # objects = DriverJobRequestManager.from_queryset(JobRequestQuerySet)()


# class Chef(Freelancer):
#     "A chef is a type of freelancer."
#
#     objects = models.GeoManager()
#     published_objects = PublishedFreelancerManager()
