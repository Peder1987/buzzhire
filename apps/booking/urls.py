from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView
from . import views


urlpatterns = [
    url(r'^bookings/$', views.FreelancerBookingsList.as_view(),
         name='freelancer_bookings_list'),

    url(r'^bookings/past/$', views.FreelancerBookingsList.as_view(past=True),
         name='freelancer_bookings_list_past'),

    url(r'^availability/$', views.AvailabilityUpdate.as_view(),
         name='availability_update'),

    url(r'^job-matching/$', views.JobMatchingView.as_view(),
         name='job_matching'),

    url(r'^job-matching/(?P<job_request_pk>[\d]+)/$', views.JobMatchingView.as_view(),
         name='job_matching_for_job_request'),
]
