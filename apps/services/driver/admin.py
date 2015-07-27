from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from . import models

from apps.freelancer.templatetags.freelancer import profile_photo
from django.template.loader import render_to_string

class DriverAdmin(admin.ModelAdmin):

    def photo_display(self, obj):
        return render_to_string('freelancer/includes/profile_photo.html',
                                profile_photo(obj, 'small'))

    photo_display.short_description = 'Photo'
    photo_display.allow_tags = True

    list_display = ('photo_display', 'reference_number', 'user',
                    'first_name', 'last_name',
                    'published', 'postcode')
    list_filter = ('published',)
    exclude = ('driving_experience_old', 'driving_experience_old_2',
               'vehicle_types_old')


class DriverVehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'driver', 'own_vehicle', 'delivery_box')


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'equivalent_to', 'delivery_box_applicable')


admin.site.register(models.Driver, DriverAdmin)
admin.site.register(models.VehicleType, VehicleTypeAdmin)
admin.site.register(models.DriverVehicleType, DriverVehicleTypeAdmin)

class DriverJobRequestAdmin(JobRequestAdmin):
    list_display = ('reference_number', 'client', 'date', 'start_time',
                    'duration', 'end_datetime',
                    'client_pay_per_hour', 'number_of_freelancers',
                    'status')
    exclude = JobRequestAdmin.exclude + ('driving_experience_old',)

admin.site.register(models.DriverJobRequest, DriverJobRequestAdmin)
