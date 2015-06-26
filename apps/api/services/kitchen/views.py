from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import JobRequestForFreelancerViewSet
from apps.services.kitchen.models import KitchenFreelancer, KitchenJobRequest
from .serializers import (KitchenFreelancerForClientSerializer,
                          PrivateKitchenFreelancerSerializer,
                          KitchenJobRequestForFreelancerSerializer)


class KitchenFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published kitchen staff - publicly available information.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to kitchen staff:
        
    - `role`: The role of the freelancer.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = KitchenFreelancerForClientSerializer

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


class KitchenJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All kitchen staff job requests.  Publicly viewable information.
    
    ## Fields
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to kitchen staff job requests:
    
    - `role`: The role needed.  Choices are:
        - `"CH"` - Chef
        - `"KA"` - Kitchen assistant
        - `"PO"` - Porter
    """
    serializer_class = KitchenJobRequestForFreelancerSerializer

    def get_queryset(self):
        return KitchenJobRequest.objects.all()
