from django.forms import widgets
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from apps.api.serializers import MoneyField
from apps.freelancer.templatetags.freelancer import PHOTO_DIMENSIONS
from ..models import Freelancer


class PublicFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for public use.
    """
    class Meta:
        model = Freelancer
        fields = ('id', 'first_name', 'last_name')


class OwnFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    profile for their own use.
    """
    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email

    full_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return obj.get_full_name()

    # english_fluency = ChoiceField()
    # phone_type = ChoiceField()
    # travel_distance = ChoiceField()

    postcode = serializers.SerializerMethodField()
    def get_postcode(self, obj):
        return str(obj.postcode)

    photo = serializers.SerializerMethodField()
    def get_photo(self, obj):
         return "%s%s" % (settings.BASE_URL,
                get_thumbnail(obj.photo, PHOTO_DIMENSIONS['medium']).url)

    minimum_pay_per_hour = MoneyField()

    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number', 'email', 'full_name',
                  'first_name', 'last_name',
                  'mobile',
                  'photo', 'english_fluency', 'eligible_to_work',
                  'phone_type',
                  # 'minimum_pay_per_hour',
                  'postcode',
                  'travel_distance')
