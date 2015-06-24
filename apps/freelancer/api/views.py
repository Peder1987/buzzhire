from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.api.views import RetrieveAndUpdateViewset
from .serializers import PublicFreelancerSerializer, PrivateFreelancerSerializer
from .permissions import FreelancerOnlyPermission
from ..models import Freelancer


class PublicFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    "All published freelancers - publicly available information."
    serializer_class = PublicFreelancerSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Freelancer.published_objects.all()


class OwnFreelancerViewSet(RetrieveAndUpdateViewset):
    """The currently logged in freelancer's profile.
    
    ## Fields
    
    - `id` Unique id for the freelancer.  Can be used as a unique id for 
           more specific kinds of freelancer objects, such as drivers.
           Integer. Read only.
    - `reference_number` Public reference number for the freelancer.  Read only.
    - `email` Their email address.  Read only.
    - `full_name` Their full name.  Read only.
    - `first_name` Their first name.
    - `last_name` Their last namee.
    - `mobile` Their mobile telephone number (must be UK based).
    - `photo` A thumbnail image, 75px x 97px.  Read only.
    - `english_fluency` Their English fluency level.  Choices are:
        - `"BA"` - Basic
        - `"CO"` - Conversational
        - `"FL"` - Fluent
        - `"NA"` - Native
    - `eligible_to_work` Whether they are eligible to work in the UK. Boolean.
    - `phone_type` What kind of phone they have.  Choices are:
        - `"AN"` - Android
        - `"IP"` - iPhone
        - `"WI"` - Windows
        - `"OT"` - Other smartphone
        - `"NS"` - Non smartphone
    - `minimum_pay_per_hour` The minimum pay they will accept per hour, in GBP.
       Decimal.
    - `postcode` The freelancer's home postcode.
    - `travel_distance` How far the freelancer is willing to travel for work.
       Integer. Choices are:
        - `1` - One mile
        - `2` - Two miles
        - `5` - Five miles
        - `10` - 10 miles
        - `20` - 20 miles
        - `50` - 50 miles
    - `years_experience` The number of years of working experience.
        Integer.  Choices are:
        - `0` - Less than 1 year
        - `1` - 1 - 3 years
        - `3` - 3 - 5 years
        - `5` - More than 5 years
    """
    model = Freelancer
    serializer_class = PrivateFreelancerSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_object(self):
        return self.request.user.freelancer