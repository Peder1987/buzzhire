from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.FreelancerBacklog.as_view(),
        name='freelancer_backlog'),
    url(r'^client/(?P<pk>[\d]+)/$',
        views.ClientFeedbackCreate.as_view(),
        name='client_feedback_create'),
    url(r'^freelancer/(?P<pk>[\d]+)/$',
        views.FreelancerFeedbackCreate.as_view(),
        name='freelancer_feedback_create'),

]
