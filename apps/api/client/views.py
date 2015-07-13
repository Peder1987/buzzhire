from rest_framework import viewsets
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import ClientForFreelancerSerializer, OwnClientSerializer
from apps.client.models import Client
from apps.api.views import RetrieveAndUpdateViewset
from .permissions import ClientOnlyPermission

class ClientForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """Clients viewable by the currently logged in freelancer.
    
    TODO - limit for the freelancer.  Currently this shows all clients.
    
    ## Fields
    
    - `id` Unique id for the client. Integer.
    - `reference_number` Public reference number for the client.
    - `first_name` Their first name.
    - `last_name` Their last name.
    - `company_name` The name of their company, if applicable.
    """
    serializer_class = ClientForFreelancerSerializer
    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        # TODO
        return Client.objects.all()


class OwnClientViewSet(RetrieveAndUpdateViewset):
    """The currently logged in client's profile.
    
    ## Fields
    
    - `id` Unique id for the client. Integer. Read only.
    - `reference_number` Public reference number for the client.  Read only.
    - `email` Their email address.  Read only.
    - `mobile` Their UK mobile phone number.
    - `company_name` The name of their company, if applicable.

    """
    model = Client
    serializer_class = OwnClientSerializer

    permission_classes = (ClientOnlyPermission,)

    def get_object(self):
        return self.request.user.client