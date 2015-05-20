from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from apps.core.views import ContextMixin
from .models import Freelancer
from .forms import PhotoUploadForm
from django.views.generic import DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy


class FreelancerOnlyMixin(object):
    """Views mixin - only allow freelancers to access.
    Adds freelancer as an attribute on the view.
    """
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        try:
            self.freelancer = self.request.user.freelancer
        except Freelancer.DoesNotExist:
            raise PermissionDenied
        return super(FreelancerOnlyMixin, self).dispatch(request,
                                                         *args, **kwargs)


class FreelancerPhotoView(FreelancerOnlyMixin, ContextMixin, DetailView):
    "View of a freelancer's own photo."
    template_name = 'freelancer/photo_page.html'
    extra_context = {'title': 'Photo'}

    def get_object(self):
        return self.freelancer

class FreelancerPhotoUpdateView(FreelancerOnlyMixin, ContextMixin,
                                SuccessMessageMixin, UpdateView):
    "Page for freelancer to upload their own photo."
    template_name = 'freelancer/photo_upload.html'
    extra_context = {'title': 'Upload photo'}
    form_class = PhotoUploadForm
    success_url = reverse_lazy('freelancer_photo')
    success_message = 'Uploaded.'

    def get_object(self):
        return self.freelancer

