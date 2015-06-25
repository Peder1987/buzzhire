from django.contrib import admin
from . import models

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created', 'date_accepted', 'manual')
    search_fields = ('jobrequest', 'freelancer')
    raw_id_fields = ('jobrequest', 'freelancer')
    list_filter = ('manual',)

admin.site.register(models.Invitation, InvitationAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created')
    search_fields = ('jobrequest', 'freelancer')
    raw_id_fields = ('jobrequest', 'freelancer')

admin.site.register(models.Booking, BookingAdmin)
