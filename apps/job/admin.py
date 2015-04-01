from django.contrib import admin
from . import models


class DriverJobRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time', 'duration',
                    'pay_per_hour', 'number_of_freelancers', 'status')
    list_filter = ('status', 'date',)
    date_hierarchy = 'date'

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)