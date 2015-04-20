from django.contrib import admin
from . import models

# This is necessary just to allow search_fields to work elsewhere
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'postcode')
    list_filter = ('status', 'date',)
    search_fields = ('reference_number',)
    date_hierarchy = 'date'

admin.site.register(models.JobRequest, JobRequestAdmin)


class DriverJobRequestAdmin(JobRequestAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'duration', 'client_pay_per_hour', 'number_of_freelancers',
                    'status')

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)
