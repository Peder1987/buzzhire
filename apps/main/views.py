from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from apps.core.views import ContextTemplateView


class TestError(TemplateView):
    "View used to trigger site error, for testing purposes."
    def dispatch(self, *args, **kwargs):
        raise Exception('Test exception raised.')


class TestDenied(TemplateView):
    "View used to trigger permission denied, for testing purposes."
    def dispatch(self, *args, **kwargs):
        raise PermissionDenied


