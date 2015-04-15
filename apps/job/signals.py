import django.dispatch


# Signal that is sent when a driver job request is created
driverjobrequest_created = django.dispatch.Signal(
                                        providing_args=['driverjobrequest'])
#
# # Signal that is sent when a job request is cancelled
# jobrequest_cancelled = django.dispatch.Signal(providing_args=['jobrequest'])
#
# # Signal that is sent when a job request is completed
# job_request_completed = django.dispatch.Signal(providing_args=['job_request'])
