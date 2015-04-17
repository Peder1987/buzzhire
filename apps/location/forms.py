from django import forms
from apps.location.models import Postcode
from apps.location.utils import GeoLocationMatchException


class PostcodeFormMixin(forms.Form):
    """Mixin for a form that has a Postcode ForeignKey field on it.
    Defines a 'raw_postcode' field that should be displayed on the form
    (instead of the postcode field) and then the postcode will be populated.
    
    TODO - consider whether this should be done using a widget/alternative
    form field instead.
    """
    raw_postcode = forms.CharField(label='Postcode', max_length=10,
                               required=False)

    def clean_raw_postcode(self):
        # We use the raw postcode form field to generate a postcode instance
        # to link with the postcode ForeignKey field.
        compressed_postcode = self.cleaned_data['raw_postcode'].replace(
                                                                    ' ', '')
        if compressed_postcode:
            # If they supply a postcode
            if self.instance.postcode_id and compressed_postcode \
                            == self.instance.postcode.compressed_postcode:
                # Postcode is the same, don't attempt to recreate it
                self.cleaned_data['postcode'] = self.instance.postcode
            else:
                # If the postcode is new or different, create/link it
                # with a new postcode instance
                try:
                    self.cleaned_data['postcode'], created = \
                                Postcode.objects.get_or_create(
                                    compressed_postcode=compressed_postcode)
                except GeoLocationMatchException:
                    raise ValidationError('That was not a valid postcode.')

        return compressed_postcode
