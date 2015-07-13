from rest_framework import serializers
from apps.client.models import Client
from apps.payment.utils import PaymentAPI


class PaymentTokenSerializer(serializers.ModelSerializer):
    """Serializer that provides client payment token.
    """
    client_token = serializers.SerializerMethodField()
    def get_client_token(self, obj):
        # Generates a Braintree 'client token' for the Client model
        return PaymentAPI().generate_client_token(obj)

    class Meta:
        model = Client
        fields = ('client_token',)
