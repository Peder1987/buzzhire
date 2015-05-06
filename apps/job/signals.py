import django.dispatch


# Signal that is sent when a driver job request is created
driverjobrequest_created = django.dispatch.Signal(
                                        providing_args=['driverjobrequest'])

