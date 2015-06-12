from rest_framework import serializers
from ..models import Postcode
from ..utils import GeoLocationMatchException


class PostcodeField(serializers.Field):
    """Serializer for postcodes.
    """
    default_error_messages = {
        'invalid': 'Not a valid UK postcode.',
    }

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        compressed_postcode = data.replace(' ', '')
        if compressed_postcode:
            instance = self.parent.instance
            if instance.postcode_id and compressed_postcode == \
                                        instance.postcode.compressed_postcode:
                # Postcode is the same, don't attempt to recreate it
                postcode = instance.postcode
            else:
                # If the postcode is new or different, create/link it
                # with a new postcode instance
                try:
                    postcode, created = \
                                Postcode.objects.get_or_create(
                                    compressed_postcode=compressed_postcode)
                except GeoLocationMatchException:
                    self.fail('invalid')

        return postcode


