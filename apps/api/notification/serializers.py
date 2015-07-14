from rest_framework import serializers
from apps.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    "Serializer for Notifications."

    class Meta:
        model = Notification
        fields = ('id', 'category', 'message',
                  'datetime_created', 'object_id', 'content_type')
