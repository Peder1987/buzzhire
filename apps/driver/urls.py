from django.conf.urls import url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [
   url(r'^$', ContextTemplateView.as_view(
            template_name='driver/become.html',
            extra_context={'title': 'Become a driver'}),
            name='driver_become'),

    url(r"^signup/$", views.SignupView.as_view(), name="driver_signup"),
    url(r"^signup/thankyou/$", ContextTemplateView.as_view(
                template_name='driver/thankyou.html',
                extra_context={'title': 'Thanks for signing up'}),
                name="driver_thankyou"),

#     url(r"^(?P<pk>[\d]+)/$", views.DriverDetailView.as_view(),
#         name="driver_detail"),
    url(r"^(?P<pk>[\d]+)/edit/$", views.DriverUpdateView.as_view(),
        name="driver_change"),
]

