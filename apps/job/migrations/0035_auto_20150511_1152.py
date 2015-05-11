# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0021_vehicletype_include_under'),
        ('job', '0034_auto_20150511_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='vehicle_type',
            field=models.ForeignKey(related_name='jobrequests', to='driver.VehicleType', help_text=b'Which types of vehicle would be appropriate for the job. (N.B. if you require a specific mixture of vehicles, such as one car and one van, then you should create these as separate bookings.)', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_types_old',
            field=models.ManyToManyField(related_name='jobrequests_old', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
