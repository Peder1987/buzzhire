from django.contrib import admin
from . import models


class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'job_date',
                    'date_submitted', 'status')
    list_filter = ('job_date', 'status')

admin.site.register(models.JobRequest, JobRequestAdmin)
