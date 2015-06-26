from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import JobRequestForFreelancerViewSet
from apps.services.waiting.models import WaitingFreelancer, WaitingJobRequest


class WaitingFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published waiting staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """

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


class WaitingJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All waiting staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return WaitingJobRequest.objects.all()
