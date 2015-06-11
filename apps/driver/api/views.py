from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OwnDriverSerializer, VehicleTypeSerializer, \
                        FlexibleVehicleTypeSerializer
from ..models import VehicleType, FlexibleVehicleType, Driver
from .permissions import DriverOnlyPermission


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


class OwnDriverViewSet(viewsets.ModelViewSet):
    """Returns the driver's own profile.
    
    - `photo` - thumbnail of the driver, 75px x 97px.
    """
    model = Driver
    serializer_class = OwnDriverSerializer

    permission_classes = (DriverOnlyPermission,)

    def get_object(self):
        return self.request.user.driver

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

