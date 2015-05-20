from django.conf.urls import url
from apps.core.views import ContextTemplateView
from . import views

urlpatterns = [
    url(r"^photo/$", views.FreelancerPhotoView.as_view(),
        name="freelancer_photo"),
    url(r"^photo/add/$", views.FreelancerPhotoUpdateView.as_view(),
        name="freelancer_photo_update"),
]

