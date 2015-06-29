from django.forms import widgets
from django.core import validators
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from ..serializers import MoneyField
from apps.freelancer.templatetags.freelancer import PHOTO_DIMENSIONS
from ..location.serializers import PostcodeField
from apps.freelancer.utils import service_for_freelancer
from apps.freelancer.models import Freelancer, FREELANCER_MIN_WAGE
from apps.core.validators import mobile_validator


class SpecificFreelancerIdentityField(serializers.HyperlinkedIdentityField):
    """A read-only field that represents the identity URL for the specific,
    non-generic version of the freelancer.
    """
    def get_url(self, obj, view_name, request, format):
        service = service_for_freelancer(obj)
        view_name = service.key + '_' + view_name
        return super(SpecificFreelancerIdentityField, self).get_url(obj,
                                                    view_name, request, format)


class FreelancerForClientSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for client use.
    """

    service_key = serializers.SerializerMethodField()
    def get_service_key(self, obj):
        "Returns the service key."
        return service_for_freelancer(obj).key

    full_name = serializers.SerializerMethodField()
    specific_object = SpecificFreelancerIdentityField(
                                    view_name='freelancers_for_client-detail')

    minimum_pay_per_hour = MoneyField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    photo_thumbnail_medium = serializers.SerializerMethodField()
    def get_photo_thumbnail_medium(self, obj):
        if obj.photo:
             return "%s%s" % (settings.BASE_URL,
                    get_thumbnail(obj.photo, PHOTO_DIMENSIONS['medium']).url)
        return None

    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number', 'specific_object',
                  'service_key', 'photo_thumbnail_medium', 'english_fluency',
                  'full_name', 'first_name', 'last_name',
                  'years_experience', 'minimum_pay_per_hour')


class PrivateFreelancerSerializer(FreelancerForClientSerializer):
    """Serializer that exposes information on the freelancer
    profile for their own use.
    """

    specific_object = serializers.SerializerMethodField()
    def get_specific_object(self, obj):
        return

    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email

    photo_thumbnail_medium = serializers.SerializerMethodField()
    def get_photo_thumbnail_medium(self, obj):
        if obj.photo:
             return "%s%s" % (settings.BASE_URL,
                    get_thumbnail(obj.photo, PHOTO_DIMENSIONS['medium']).url)
        return None

    minimum_pay_per_hour = MoneyField(
            validators=[validators.MinValueValidator(FREELANCER_MIN_WAGE)])

    postcode = PostcodeField()

    class Meta(FreelancerForClientSerializer.Meta):
        fields = FreelancerForClientSerializer.Meta.fields + ('email', 'mobile',
                  'photo_thumbnail_medium', 'english_fluency',
                  'eligible_to_work', 'minimum_pay_per_hour',
                  'postcode',
                  'travel_distance', 'years_experience')
