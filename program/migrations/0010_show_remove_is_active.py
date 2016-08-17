# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0009_host_remove_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='is_active',
        ),
    ]
