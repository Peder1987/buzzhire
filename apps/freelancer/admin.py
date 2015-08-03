from django.contrib import admin
from apps.freelancer.templatetags.freelancer import profile_photo
from django.template.loader import render_to_string
from . import models


class FreelancerAdmin(admin.ModelAdmin):
    def photo_display(self, obj):
        return render_to_string('freelancer/includes/profile_photo.html',
                                profile_photo(obj, 'small'))

    photo_display.short_description = 'Photo'
    photo_display.allow_tags = True

    list_display = ('photo_display', 'reference_number', 'user',
                    'first_name', 'last_name',
                    'published', 'postcode')
    list_filter = ('published',)
    search_fields = ('first_name', 'last_name', 'user__email')

admin.site.register(models.Freelancer, FreelancerAdmin)
