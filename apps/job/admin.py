from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin
from . import models

# This is necessary just to allow search_fields to work elsewhere
class JobRequestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'postcode')
    list_filter = ('status', 'date',)
    search_fields = ('reference_number',)
    date_hierarchy = 'date'
    fsm_field = ['status']
    exclude = ['status']
    readonly_fields = ['status_display']

    def status_display(self, instance):
        return instance.get_status_display()
    status_display.short_description = 'Status'

admin.site.register(models.JobRequest, JobRequestAdmin)


class DriverJobRequestAdmin(JobRequestAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'duration', 'client_pay_per_hour', 'number_of_freelancers',
                    'status')

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)