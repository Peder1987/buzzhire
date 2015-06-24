# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0011_auto_20150528_1021'),
        ('chef', '0002_setup_perms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('freelancer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='freelancer.Freelancer')),
                ('certification', models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'Chef'), (b'SC', b'Sous chef'), (b'KA', b'Kitchen assistant'), (b'PO', b'Kitchen porter')])),
            ],
            options={
            },
            bases=('freelancer.freelancer',),
        ),
    ]
