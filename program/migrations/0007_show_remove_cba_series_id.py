# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_note_remove_cba_entry_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='cba_series_id',
        ),
    ]
