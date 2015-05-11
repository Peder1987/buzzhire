# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0036_vehicle_types_to_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_type',
            field=models.ForeignKey(related_name='jobrequests', to='driver.VehicleType', help_text=b'Which type of vehicle would be appropriate for the job. (N.B. if you require a specific mixture of vehicles, such as one car and one van, then you should create these as separate bookings.)', null=True),
            preserve_default=True,
        ),
    ]
