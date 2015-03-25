from django.contrib import admin
from . import models


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created')


admin.site.register(models.Lead, LeadAdmin)
