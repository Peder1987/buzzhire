from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$',
        views.BookingFeedbackCreate.as_view(),
        name='booking_feedback_create'),
]
