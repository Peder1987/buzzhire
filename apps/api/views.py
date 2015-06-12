from rest_framework import mixins
from rest_framework import viewsets


class RetrieveAndUpdateViewset(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """A viewset for retrieving/updating single objects.
    Use this viewset with apps.api.routers.SingleObjectFriendlyRouter
    for nicer routing.
    
    """
    detail_root = True
