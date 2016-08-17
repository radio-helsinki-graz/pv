# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0010_show_remove_is_active.py'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programslot',
            name='is_active',
        ),
    ]
