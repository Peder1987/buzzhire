from django.forms import widgets
from rest_framework import serializers
from apps.api.serializers import MoneyField
from apps.job import service_from_class
from apps.job.models import JobRequest


class SpecificJobRequestIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the job request.
    """
    def get_url(self, obj, view_name, request, format):
        service = service_from_class(obj.__class__)
        view_name = service.key + '_' + view_name
        return super(SpecificJobRequestIdentityField, self).get_url(obj,
                                                    view_name, request, format)


class BaseJobRequestSerializer(serializers.ModelSerializer):
    """Base serializer for job requests ."""
    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        return service_from_class(obj.__class__).key

    address = serializers.SerializerMethodField('_address')
    def _address(self, obj):
        return {
            'address1': obj.address1,
            'address2': obj.address2,
            'city': obj.get_city_display(),
            'postcode': str(obj.postcode),
        }

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'service_key',
                  'specific_object', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'number_of_freelancers', 'address',
                  'years_experience', 'comments'
                  )

class JobRequestForFreelancerSerializer(BaseJobRequestSerializer):
    """Serializer for job requests for freelancer."""
    client = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='clients_for_freelancer-detail')

    freelancer_pay_per_hour = MoneyField()

    specific_object = SpecificJobRequestIdentityField(
                            view_name='job_requests_for_freelancer-detail')

    class Meta(BaseJobRequestSerializer.Meta):
        fields = BaseJobRequestSerializer.Meta.fields + ('client',
                                                    'freelancer_pay_per_hour')

class JobRequestForClientSerializer(BaseJobRequestSerializer):
    """Serializer for job requests for client."""

    client_pay_per_hour = MoneyField()

    specific_object = SpecificJobRequestIdentityField(
                            view_name='job_requests_for_client-detail')

    class Meta(BaseJobRequestSerializer.Meta):
        fields = BaseJobRequestSerializer.Meta.fields + ('client_pay_per_hour',)
