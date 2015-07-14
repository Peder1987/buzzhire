from rest_framework import serializers
from apps.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    "Serializer for Notifications."

    content_type = serializers.SerializerMethodField()
    def get_content_type(self, obj):
        return obj.content_type.model

    class Meta:
        model = Notification
        fields = ('id', 'category', 'message',
                  'datetime_created', 'object_id', 'content_type')
