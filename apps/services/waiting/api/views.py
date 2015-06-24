from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from apps.job.api.views import JobRequestViewSet
from ..models import WaitingFreelancer, WaitingJobRequest


class PublicWaitingFreelancerViewSet(PublicFreelancerViewSet):
    "All published waiting staff - publicly available information."

    def get_queryset(self):
        return WaitingFreelancer.published_objects.all()


class OwnWaitingFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the waiting staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to waiting staff:
    
    - Currently no fields.
     
    """
    pass


class WaitingJobRequestViewSet(JobRequestViewSet):
    """All waiting staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return WaitingJobRequest.objects.all()
