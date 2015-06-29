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


class CreateUpdateNotDestroyViewset(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """Viewset which just leaves out the deletion capability from
    a standard ModelViewSet.
    """
    pass