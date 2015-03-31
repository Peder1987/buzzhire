from django.conf.urls import url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [
    url(r"^express-interest/$", views.LeadCreateView.as_view(),
        name="express_interest"),
    url(r"^express-interest/thankyou/$", ContextTemplateView.as_view(
                template_name='client/thankyou.html',
                extra_context={'title': 'Thanks for your interest'}),
                name="express_interest_thankyou"),

    url(r"^(?P<pk>[\d]+)/edit/$", views.ClientUpdateView.as_view(),
        name="client_change"),
]
