# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def data_migration(apps, schema_editor):
    # Move the driving experience over to the field on the job request model
    DriverJobRequest = apps.get_model('driver', 'DriverJobRequest')
    for job_request in DriverJobRequest.objects.all():
        job_request.years_experience = job_request.driving_experience_old
        job_request.save()

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0030_auto_20150624_1115'),
    ]

    operations = [
        migrations.RunPython(data_migration)
    ]
