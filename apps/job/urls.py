from django.conf.urls import url
from . import views
from apps.job.models import JobRequest


urlpatterns = [
#     url(r'^$', views.JobRequestList.as_view(),
#         name='jobrequest_list'),

    url(r'^create/$', views.JobRequestCreate.as_view(),
        name='jobrequest_create'),

    url(r'^create/sign-in/$', views.JobRequestCreateAnonymous.as_view(),
        name='jobrequest_create_anon'),

#     url(r'^create/done/$', views.JobRequestComplete.as_view(),
#         name='jobrequest_complete'),
#
#     url(r'^requests/moderation/$', views.JobRequestsModeration.as_view(),
#         name='jobrequest_moderation'),
#     url(r'^requests/(?P<pk>[\d]+)/$', views.JobRequestDetail.as_view(),
#         name='jobrequest_detail'),
#
#     url(r'^requests/(?P<pk>[\d]+)/open/$',
#         views.JobRequestConfirmAction.as_view(status=JobRequest.STATUS_OPEN),
#         name='jobrequest_open'),
#     url(r'^requests/(?P<pk>[\d]+)/follow-up/$',
#         views.JobRequestConfirmAction.as_view(
#                                     status=JobRequest.STATUS_FOLLOW_UP),
#         name='jobrequest_followup'),
#     url(r'^requests/(?P<pk>[\d]+)/cancel/$',
#         views.JobRequestConfirmAction.as_view(
#                                         status=JobRequest.STATUS_CANCELLED),
#         name='jobrequest_cancel'),

]
