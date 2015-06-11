from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView
from . import views
from django.conf import settings

# Not very DRY but it'll only be here briefly
if settings.COMING_SOON:
    urlpatterns = [
        url(r'^$', ContextTemplateView.as_view(
                                template_name='main/holding/home.html'),
                                name='index'),
        url(r'^book/$', ContextTemplateView.as_view(
                                template_name='main/holding/book.html',
                                extra_context={'title': 'Book a driver'}),
                                name='book'),

        url(r'^contact/$', ContextTemplateView.as_view(
                                template_name='main/contact.html',
                                extra_context={'title': 'Contact us'}),
                                name='contact'),

        url(r'^credits/$', ContextTemplateView.as_view(
                                template_name='main/credits.html',
                                extra_context={'title': 'Site credits'}),
                                name='credits'),
        url(r'^privacy/$', ContextTemplateView.as_view(
                                template_name='main/privacy.html',
                                extra_context={'title': 'Privacy policy'}),
                                name='privacy'),

        url(r'^testerror$', views.TestError.as_view()),
        url(r'^testdenied$', views.TestDenied.as_view()),
    ]
else:
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

        url(r'^privacy/$', ContextTemplateView.as_view(
                                template_name='main/privacy.html',
                                extra_context={'title': 'Privacy policy'}),
                                name='privacy'),

        url(r'^testerror$', views.TestError.as_view()),
        url(r'^testdenied$', views.TestDenied.as_view()),
    ]



