from django.forms import widgets
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from apps.api.serializers import MoneyField
from apps.freelancer.templatetags.freelancer import PHOTO_DIMENSIONS
from apps.location.api.serializers import PostcodeField
from ..utils import service_for_freelancer
from ..models import Freelancer


class SpecificFreelancerIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the freelancer.
    """
    def get_url(self, obj, view_name, request, format):
        service = service_for_freelancer(obj)
        view_name = service.key + '_' + view_name
        return super(SpecificFreelancerIdentityField, self).get_url(obj,
                                                    view_name, request, format)


class PublicFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for public use.
    """

    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        return service_for_freelancer(obj).key

    full_name = serializers.SerializerMethodField()
    specific_object = SpecificFreelancerIdentityField(
                                                view_name='freelancers-detail')

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number', 'specific_object',
                  'service_key', 'full_name', 'first_name', 'last_name')


class PrivateFreelancerSerializer(PublicFreelancerSerializer):
    """Serializer that exposes information on the freelancer
    profile for their own use.
    """
    specific_object = serializers.SerializerMethodField()
    def get_specific_object(self, obj):
        return

    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email

    photo = serializers.SerializerMethodField()
    def get_photo(self, obj):
        if obj.photo:
             return "%s%s" % (settings.BASE_URL,
                    get_thumbnail(obj.photo, PHOTO_DIMENSIONS['medium']).url)
        return None

    minimum_pay_per_hour = MoneyField()

    postcode = PostcodeField()

    class Meta(PublicFreelancerSerializer.Meta):
        fields = PublicFreelancerSerializer.Meta.fields + ('email', 'mobile',
                  'photo', 'english_fluency', 'eligible_to_work',
                  'phone_type',
                  'minimum_pay_per_hour',
                  'postcode',
                  'travel_distance', 'years_experience')
