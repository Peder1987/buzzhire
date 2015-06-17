from django.conf.urls import url
from . import views, services
from apps.job.models import JobRequest



urlpatterns = [
     url(r'^admin/$', views.AdminJobList.as_view(),
         name='job_request_admin_list'),
     url(r'^admin/(?P<status>[\w]+)/$', views.AdminJobList.as_view(),
        name='job_request_admin_list_tab'),

     url(r'^requested/$', views.RequestedJobList.as_view(),
         name='requested_jobs'),

     url(r'^requested/past/$', views.RequestedJobList.as_view(past=True),
         name='requested_jobs_past'),

    url(r'^create/(?P<service_key>[\w]+)/$',
                       views.JobRequestCreate.as_view(),
                       name='job_request_create'),

#
#      url(r'^accepted/$', views.DriverJobRequestForFreelancerList.as_view(),
#          name='freelancer_driverjobrequest_list'),

     url(r'^create/new-client/$', views.DriverJobRequestCreateAnonymous.as_view(),
         name='driverjobrequest_create_anon'),

    url(r'^requests/(?P<pk>[\d]+)/checkout/$',
        views.DriverJobRequestCheckout.as_view(),
        name='driverjobrequest_checkout'),

     url(r'^requests/(?P<pk>[\d]+)/done/$',
         views.DriverJobRequestDone.as_view(),
         name='driverjobrequest_done'),

    url(r'^requests/(?P<pk>[\d]+)/$', views.JobRequestDetail.as_view(),
        name='jobrequest_detail'),


    url(r'^requests/(?P<pk>[\d]+)/edit/$',
        views.JobRequestUpdate.as_view(),
        name='jobrequest_edit'),
]

