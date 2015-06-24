from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from apps.job.api.views import JobRequestViewSet
from ..models import KitchenFreelancer, KitchenJobRequest


class PublicKitchenFreelancerViewSet(PublicFreelancerViewSet):
    """All published kitchen staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """

    def get_queryset(self):
        return KitchenFreelancer.published_objects.all()


class OwnKitchenFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the kitchen staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
    
    - Currently no fields.
     
    """
    pass


class KitchenJobRequestViewSet(JobRequestViewSet):
    """All kitchen staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to kitchen staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return KitchenJobRequest.objects.all()
