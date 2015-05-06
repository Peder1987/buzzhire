import django.dispatch


# Signal that is sent when a job is booked
booking_created = django.dispatch.Signal(providing_args=['booking'])
