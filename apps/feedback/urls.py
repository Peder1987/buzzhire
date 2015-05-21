from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.BookingFeedbackCreate.as_view(),
        name='booking_feedback_create'),
]
