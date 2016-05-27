# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_programslot_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='cba_entry_id',
        ),
    ]
