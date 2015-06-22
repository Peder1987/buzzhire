from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateDriverSerializer, VehicleTypeSerializer, \
                    FlexibleVehicleTypeSerializer, DriverJobRequestSerializer
from ..models import VehicleType, FlexibleVehicleType, Driver, DriverJobRequest
from .permissions import DriverOnlyPermission
from apps.api.views import RetrieveAndUpdateViewset


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


class OwnDriverViewSet(RetrieveAndUpdateViewset):
    """Returns the driver's own profile.
    
    ## Fields
    
    The generic fields are documented on the freelancer endpoint.
    
    These are the fields specific to drivers:
    
    - `driving_experience` The number of years of driving experience.
        Integer.  Choices are:
        - `0` - Less than 1 year
        - `1` - 1 - 3 years
        - `3` - 3 - 5 years
        - `5` - More than 5 years
     
    """
    model = Driver
    serializer_class = PrivateDriverSerializer

    permission_classes = (DriverOnlyPermission,)

    def get_object(self):
        return self.request.user.driver


class DriverJobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """All driver job requests.  Publicly viewable information.
    
    * `flexible_vehicle_type`: The flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    """
    serializer_class = DriverJobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DriverJobRequest.objects.all()
