# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0008_show_remove_automation_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='is_active',
        ),
    ]
