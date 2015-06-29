from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import (JobRequestForFreelancerViewSet,
                          ServiceSpecificJobRequestForClientViewSet)
from apps.services.waiting.models import WaitingFreelancer, WaitingJobRequest


class OwnWaitingFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the waiting staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to waiting staff:
    
    - Currently no fields.
     
    """
    pass


class WaitingFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published waiting staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """
    model_class = WaitingFreelancer



class WaitingJobRequestForClientViewSet(ServiceSpecificJobRequestForClientViewSet):
    """Waiting staff job requests for the currently logged in client.
    
    ## Fields
    
    The generic fields are documented on the job request
    endpoint for the client.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    model_class = WaitingJobRequest


class WaitingJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All waiting staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to waiting staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return WaitingJobRequest.objects.all()
