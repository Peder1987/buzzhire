from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# class UserNotificationSettings(models.Model):
#     """Settings for each user related to notifications.
#     """
#     user = models.OneToOneField(User, related_name='notification_settings')


class NotificationQuerySet(models.QuerySet):
    "Custom queryset for Notifications."

    def for_user(self, user):
        "Filters by notifications for the current user."
        return self.filter(user=user)


class Notification(models.Model):
    """A notification is a message sent by the system to a particular user.
    Optionally, it is linked by a generic relation 
    """
    message = models.TextField()
    category = models.CharField(max_length=30,
                    help_text='What kind of notification this is.')

    user = models.ForeignKey(User, related_name='notifications')

    datetime_created = models.DateTimeField(auto_now_add=True)

    # Optionally, relate the notification to another model
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        created = not self.pk
        super(Notification, self).save(*args, **kwargs)
        # If the Notification is being created, send as a push notification too
        if created:
            self.send_as_push()

    def send_as_push(self):
        """Sends the notification as an push notification."""
        # TODO
        pass

    def __unicode__(self):
        return "%s..." % self.message[:15]

    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-datetime_created',)

# def dispatch_notifications(user, category, context={},
#                            related_object=None):
#     """Dispatches any notifications the user has opted in to, including
#     emails and push notifications.
#     """
#     # Create notification instance
#     notification = Notification(
#         user=user,
#         category=category,
#         message='',  # TODO
#         related_object=related_object,
#     )
#     notification.save()
#
#     # If the user has email notifications enabled
#     # Detect email callback for the supplied category
#     # Send email (via huey)
#     notification.send_as_email()
#
#     # If the user has push notifications enabled
#     # Detect push callback for the supplied category
#     # Send push notification via huey
#     notification.send_as_push()
