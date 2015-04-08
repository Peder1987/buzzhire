from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^job-matching/$', views.JobMatchingView.as_view(),
         name='driver_search'),
]
