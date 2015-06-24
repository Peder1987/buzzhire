from django.forms import widgets
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from apps.api.serializers import MoneyField
from apps.freelancer.templatetags.freelancer import PHOTO_DIMENSIONS
from apps.location.api.serializers import PostcodeField
from ..models import Freelancer


class PublicFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for public use.
    """

    full_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number',
                  'service', 'full_name', 'first_name', 'last_name')


class PrivateFreelancerSerializer(PublicFreelancerSerializer):
    """Serializer that exposes information on the freelancer
    profile for their own use.
    """
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
        fields = PublicFreelancerSerializer.Meta.fields + ('mobile',
                  'photo', 'english_fluency', 'eligible_to_work',
                  'phone_type',
                  'minimum_pay_per_hour',
                  'postcode',
                  'travel_distance', 'years_experience')
