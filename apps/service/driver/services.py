from apps.job import services, Service
from .models import DriverJobRequest, Driver
from .forms import DriverJobRequestForm, DriverForm
from django.core.urlresolvers import reverse_lazy


class DriverService(Service):
    "Class that defines the driver service."
    key = 'driver'

    job_request_model = DriverJobRequest
    job_request_form = DriverJobRequestForm

    freelancer_model = Driver
    freelancer_form = DriverForm

    freelancer_additional_menu_items = [
        (reverse_lazy('drivervehicletype_list'),
         'Vehicles', 'vehicletypes')
    ]

services.register(DriverService)
