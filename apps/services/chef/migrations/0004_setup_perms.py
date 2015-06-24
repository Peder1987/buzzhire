# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    add_admin_perms(apps.get_model('chef', 'Chef'))

class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0003_chef'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
