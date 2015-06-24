from apps.service import services


class ServiceViewMixin(object):
    """Views mixin for views connected to urls with a service_key
    url component.
    Sets self.service as equal to the service specified.
    """
    def dispatch(self, request, *args, **kwargs):
        self.service = services[kwargs['service_key']]
        return super(ServiceViewMixin, self).dispatch(request, *args, **kwargs)
