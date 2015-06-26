from django.db.models import Q
from rest_framework import viewsets
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import JobRequestSerializer
from apps.job.models import JobRequest


class JobRequestForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """All job requests for the logged in freelancer
    (ones either invited or booked on).
    
    - `id` Unique id for the job request.  Can be used as a unique id for 
           more specific kinds of job request objects,
           such as driver job requests. Integer. Read only.
    - `reference_number` Public reference number for the job request.  Read only.
    - `service_key` Name of the service provided.
    - `specific_object` API URL for the service-specific version
       of the job request, which may contain additional service-specific fields.  
    - `client` The client who created the job request.  API endpoint.  Read only.
    - `status` The status of the job request:  Choices are:
        - `"IC"` - The client has created the job request but has not yet paid.
        - `"OP"` -  Open.  The client has paid and the job request is now ready for booking.
        - `"CF"` - Confirmed.  The freelancers have now been assigned.
        - `"CP"` - Complete.  The work has been completed.
        - `"CA"` - Cancelled.  The job request has been cancelled.
    - `tips_included` Whether tips are included in the fee.  Boolean.
    - `date` The start date of the job.  Format `"YYYY-MM-DD"`.
    - `start_time` The start time of the job.  Format `"00:00:00"`.
    - `duration` The duration of the job, in hours.  Integer.
    - `number_of_freelancers` The number of freelancers required to
      undertake the job.  Integer.
    - `address` The address that the job is taking place at.  Format: a JSON
      object with the following named values:
        - `address1` - First line of address.
        - `address2` - Second line of address.
        - `city` - City.  Must be `"London"`.
        - `postcode` - A valid London postcode.
    - `client_pay_per_hour`: The amount, in GBP, that the client will
      pay per hour.  Not visible to freelancers (TODO). Decimal.
    - `freelancer_pay_per_hour`: The amount, in GBP, that the freelancer will
      be paid per hour.  This is based on the `client_pay_per_hour` field.
      Not visible to clients (TODO). Decimal.  Read only.
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - No preference
        - `1` - 1 year
        - `3` - 3 years
        - `5` - 5 years
    - `comments` Any extra information the client wants to tell the freelancer.
      Free text.    
    """
    serializer_class = JobRequestSerializer
    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        # TODO
        return JobRequest.objects.all()

