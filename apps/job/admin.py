from django.contrib import admin
from . import models


class DriverJobRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'client', 'status')
    list_filter = ('status',)

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)