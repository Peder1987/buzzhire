from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [
    url(r'^$', ContextTemplateView.as_view(
                            template_name='main/home.html'),
                            name='index'),

    url(r'^contact/$', ContextTemplateView.as_view(
                            template_name='main/contact.html',
                            extra_context={'title': 'Contact us'}),
                            name='contact'),

    url(r'^credits/$', ContextTemplateView.as_view(
                            template_name='main/credits.html',
                            extra_context={'title': 'Site credits'}),
                            name='credits'),

    url(r'^testerror$', views.TestError.as_view()),
    url(r'^testdenied$', views.TestDenied.as_view()),
]
