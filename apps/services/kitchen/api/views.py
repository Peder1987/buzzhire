from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from apps.job.api.views import JobRequestViewSet
from ..models import KitchenFreelancer, KitchenJobRequest
from .serializers import (PublicKitchenFreelancerSerializer,
                          PrivateKitchenFreelancerSerializer,
                          KitchenJobRequestSerializer)


class PublicKitchenFreelancerViewSet(PublicFreelancerViewSet):
    """All published kitchen staff - publicly available information.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
        
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = PublicKitchenFreelancerSerializer

    def get_queryset(self):
        return KitchenFreelancer.published_objects.all()


class OwnKitchenFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the kitchen staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = PrivateKitchenFreelancerSerializer


class KitchenJobRequestViewSet(JobRequestViewSet):
    """All kitchen staff job requests.  Publicly viewable information.
    
    ## Fields
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to kitchen staff job requests:
    
    - `role`: The role needed.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = KitchenJobRequestSerializer

    def get_queryset(self):
        return KitchenJobRequest.objects.all()
