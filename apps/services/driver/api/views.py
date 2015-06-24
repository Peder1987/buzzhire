from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from apps.job.api.views import JobRequestViewSet
from apps.freelancer.api.views import (PublicFreelancerViewSet,
                                       OwnFreelancerViewSet)
from .serializers import (PrivateDriverSerializer, VehicleTypeSerializer,
                    FlexibleVehicleTypeSerializer, DriverJobRequestSerializer)
from ..models import VehicleType, FlexibleVehicleType, Driver, DriverJobRequest
from apps.freelancer.api.permissions import FreelancerOnlyPermission
from apps.api.views import RetrieveAndUpdateViewset


class PublicDriverViewSet(PublicFreelancerViewSet):
    "All published freelancers - publicly available information."

    def get_queryset(self):
        return Driver.published_objects.all()


class OwnDriverViewSet(OwnFreelancerViewSet):
    """Returns the driver's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to drivers:
    
    - Currently no fields.
     
    """
    pass


class DriverJobRequestViewSet(JobRequestViewSet):
    """All driver job requests.  Publicly viewable information.
    
    The generic fields are documented on the job request endpoint.
    
    - `flexible_vehicle_type`: The flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    - `own_vehicle`: Whether the driver needs to supply their own vehicle.
    - `delivery_box_applicable`: Whether the minimum delivery box requirement
      is relevant. 
    - `minimum_delivery_box`: The minimum size of delivery box required (only
      relevant if `delivery_box_applicable` is `true`).  Integer.  Choices are:
        - `0` - None
        - `2` - Standard
        - `4` - Pizza
    """
    serializer_class = DriverJobRequestSerializer

    def get_queryset(self):
        return DriverJobRequest.objects.all()


class VehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All vehicle types.
    """
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()


class FlexibleVehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """All flexible vehicle types.
    
    These are vehicle types that can include more than one vehicle type,
    e.g. Motorcycle / Scooter.  They are used on job requests, where the
    vehicle requirements are less strict.
    
    """
    serializer_class = FlexibleVehicleTypeSerializer

    def get_queryset(self):
        return FlexibleVehicleType.objects.all()


