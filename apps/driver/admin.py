from django.contrib import admin
from . import models


class DriverAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'user', 'first_name', 'last_name',
                    'published', 'postcode')
    list_filter = ('published',)
    exclude = ('driving_experience_old', 'vehicle_types_old')


class DriverVehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'driver', 'own_vehicle', 'delivery_box')


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'equivalent_to')


admin.site.register(models.Driver, DriverAdmin)
admin.site.register(models.VehicleType, VehicleTypeAdmin)
admin.site.register(models.DriverVehicleType, DriverVehicleTypeAdmin)
