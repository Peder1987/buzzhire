from django.forms import widgets
from rest_framework import serializers
from apps.api.serializers import MoneyField
from .. import service_from_class
from ..models import JobRequest


class SpecificJobRequestIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the job request.
    """
    def get_url(self, obj, view_name, request, format):
        service = service_from_class(obj.__class__)
        view_name = service.key + '_' + view_name
        return super(SpecificJobRequestIdentityField, self).get_url(obj,
                                                    view_name, request, format)


class JobRequestSerializer(serializers.ModelSerializer):
    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        return service_from_class(obj.__class__).key


    specific_object = SpecificJobRequestIdentityField(
                                            view_name='job_requests-detail')

    client = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='clients-detail')

    address = serializers.SerializerMethodField('_address')
    def _address(self, obj):
        return {
            'address1': obj.address1,
            'address2': obj.address2,
            'city': obj.get_city_display(),
            'postcode': str(obj.postcode),
        }

    client_pay_per_hour = MoneyField()
    freelancer_pay_per_hour = MoneyField()

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'service_key',
                  'specific_object',
                  'client', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'number_of_freelancers', 'address',
                  'phone_requirement', 'client_pay_per_hour',
                  'freelancer_pay_per_hour', 'years_experience', 'comments'
                  )


