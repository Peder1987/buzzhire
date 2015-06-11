from rest_framework import serializers
from apps.core.views import POUND_SIGN


class ChoiceField(serializers.Field):
    """Serializer field that outputs a ChoiceField in the form:
    
        {
            'value': 'AB',
            'text': get_FOO_display(),
        }
    """
    def __init__(self, *args, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super(ChoiceField, self).__init__(**kwargs)

    def to_representation(self, value):
        return {
            'value': str(getattr(value, self.field_name)),
            'text': getattr(value, 'get_%s_display' % self.field_name)(),
        }


class MoneyField(serializers.Field):
    """Serializer field that outputs a MoneyField in the form:
    
        {
            'amount': 7.25,
            'currency': "GBP",
        }
    """

    def to_representation(self, value):
        return {
            'amount': value.amount,
            'currency': str(value.currency),
            # TODO - make this work for other currencies,
            # not necessary at the moment
            'display': "%s%s" % (POUND_SIGN, value.amount)
        }
