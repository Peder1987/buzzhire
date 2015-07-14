from rest_framework import viewsets
from rest_framework import permissions
from apps.notification.models import Notification
from .serializers import NotificationSerializer


class NotificationsForUserViewSet(viewsets.ReadOnlyModelViewSet):
    """All notifications for the currently logged in user.  Read only.
    
    ## Fields
    
    - `id` Unique id for the notification. Integer.
    - `category` A machine-readable name to identify what
       kind of notification this is.
    - `message` The text of the message.  
    - `datetime_created` Date and time of the notification.
    - `object_id` and `content_type` Notifications can optionally be
       associated with a model in the system, known as the 'related object'.
       Together, the object id and content type form a unique reference to
       the related object.  Integers.  
    
    """
    serializer_class = NotificationSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.for_user(self.request.user)
