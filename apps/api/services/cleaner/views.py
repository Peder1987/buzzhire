from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import JobRequestForFreelancerViewSet
from apps.services.cleaner.models import Cleaner, CleanerJobRequest


class CleanerForClientViewSet(FreelancerForClientViewSet):
    """All published cleaners - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """

    def get_queryset(self):
        return Cleaner.published_objects.all()


class OwnCleanerViewSet(OwnFreelancerViewSet):
    """Returns the cleaner's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to cleaners:
    
    - Currently no fields.
     
    """
    pass


class CleanerJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All cleaner job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to cleaner job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return CleanerJobRequest.objects.all()
