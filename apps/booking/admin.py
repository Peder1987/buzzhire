from django.contrib import admin
from . import models

class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest', 'created')
    search_fields = ('jobrequest', 'freelancer')
    raw_id_fields = ('jobrequest', 'freelancer')

admin.site.register(models.Booking, BookingAdmin)
