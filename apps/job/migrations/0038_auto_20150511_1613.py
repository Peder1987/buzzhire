# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

# Note this migration doesn't work and needs to be faked; which is fine since
# it's only a ForeignKey changing to a proxy model.
# This bug is fixed Django 1.8.

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0037_auto_20150511_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_type',
            field=models.ForeignKey(related_name='jobrequests', to='driver.FlexibleVehicleType', help_text=b'Which type of vehicle would be appropriate for the job. ', null=True),
            preserve_default=True,
        ),
    ]
