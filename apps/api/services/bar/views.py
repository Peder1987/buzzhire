from ...freelancer.views import (FreelancerForClientViewSet,
                                       OwnFreelancerViewSet)
from ...job.views import JobRequestForFreelancerViewSet
from apps.services.bar.models import BarFreelancer, BarJobRequest
from .serializers import (BarFreelancerForClientSerializer,
                          PrivateBarFreelancerSerializer,
                          BarJobRequestSerializer)


class BarFreelancerForClientViewSet(FreelancerForClientViewSet):
    """All published bar staff - publicly available information.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to bar staff:
        
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = BarFreelancerForClientSerializer

    def get_queryset(self):
        return BarFreelancer.published_objects.all()


class OwnBarFreelancerViewSet(OwnFreelancerViewSet):
    """Returns the bar staff's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to bar staff:
    
    - `role`: The role of the freelancer.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = PrivateBarFreelancerSerializer


class BarJobRequestForFreelancerViewSet(JobRequestForFreelancerViewSet):
    """All bar staff job requests.  Publicly viewable information.
    
    ## Fields
    
    The generic fields are documented on the job request endpoint.
    
    These are the fields specific to bar staff job requests:
    
    - `role`: The role needed.  Choices are:
        - `"MX"` - Mixologist
        - `"BM"` - Barman
        - `"BT"` - Barista
    """
    serializer_class = BarJobRequestSerializer

    def get_queryset(self):
        return BarJobRequest.objects.all()
