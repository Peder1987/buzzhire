from django.forms import widgets
from rest_framework import serializers
from apps.api.serializers import ChoiceField, MoneyField
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

    english_fluency = ChoiceField()
    phone_type = ChoiceField()

    postcode = serializers.SerializerMethodField()
    def get_postcode(self, obj):
        return str(obj.postcode)

    # TODO - photo should return thumbnail
    # photo = serializers.SerializerMethodField()
    # def get_photo(self, obj):
    #     pass

    minimum_pay_per_hour = MoneyField()

    class Meta:
        model = Freelancer
        fields = ('id', 'reference_number', 'email', 'full_name',
                  'first_name', 'last_name',
                  'mobile',
                  'photo', 'english_fluency', 'eligible_to_work',
                  'phone_type',
                  'minimum_pay_per_hour',
                  'postcode',
                  'travel_distance')
