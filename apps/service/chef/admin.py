from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from . import models

# class ChefAdmin(admin.ModelAdmin):
#     list_display = ('photo_display', 'reference_number', 'user',
#                     'first_name', 'last_name',
#                     'published', 'postcode')
#     list_filter = ('published',)
#     exclude = ('driving_experience_old', 'vehicle_types_old')
#
# admin.site.register(models.Chef, ChefAdmin)


class ChefJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('certification',)

admin.site.register(models.ChefJobRequest, ChefJobRequestAdmin)
