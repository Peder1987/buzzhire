from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from apps.job.api.views import JobRequestViewSet
from ..models import BarFreelancer, BarJobRequest


class PublicBarFreelancerViewSet(PublicFreelancerViewSet):
    """All published bar staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """

    def get_queryset(self):
        return BarFreelancer.published_objects.all()


class OwnBarFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the bar staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to bar staff:
    
    - Currently no fields.
     
    """
    pass


class BarJobRequestViewSet(JobRequestViewSet):
    """All bar staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to bar staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return BarJobRequest.objects.all()
