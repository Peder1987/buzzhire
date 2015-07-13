from .serializers import PaymentTokenSerializer
from apps.client.models import Client
from apps.api.views import RetrieveViewset
from apps.api.client.permissions import ClientOnlyPermission

class PaymentTokenViewSet(RetrieveViewset):
    """A Braintree 'client token' for the currently logged in
    client.  This endpoint will generate a new token each time it is called.
    
    ## Fields
    
    - `client_token` The Braintree 'client token' for the client.

    """
    model = Client
    serializer_class = PaymentTokenSerializer
    permission_classes = (ClientOnlyPermission,)

    def get_object(self):
        return self.request.user.client
