from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from apps.job.api.views import JobRequestViewSet
from ..models import Chef, ChefJobRequest


class PublicChefViewSet(PublicFreelancerViewSet):
    """All published kitchen staff - publicly available information.
    
    The generic fields are documented on the freelancer endpoint.
    """

    def get_queryset(self):
        return Chef.published_objects.all()


class OwnChefViewSet(OwnFreelancerViewSet):
    """Returns the kitchen staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
    
    - Currently no fields.
     
    """
    pass


class ChefJobRequestViewSet(JobRequestViewSet):
    """All kitchen staff job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to kitchen staff job requests:
    
    - Currently no fields.
 
    """
    def get_queryset(self):
        return ChefJobRequest.objects.all()
