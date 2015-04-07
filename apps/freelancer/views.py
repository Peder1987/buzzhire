from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from .models import Freelancer


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
