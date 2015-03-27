from django.contrib import admin
from . import models


class DriverAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'user', 'first_name', 'last_name',
                    'published')
    list_filter = ('published',)


admin.site.register(models.Driver, DriverAdmin)
