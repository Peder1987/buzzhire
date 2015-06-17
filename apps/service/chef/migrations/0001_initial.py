# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0043_move_driverjobrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefJobRequest',
            fields=[
                ('jobrequest_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='job.JobRequest')),
                ('certification', models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'SC', b'Sous chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')])),
            ],
            options={
            },
            bases=('job.jobrequest',),
        ),
    ]
