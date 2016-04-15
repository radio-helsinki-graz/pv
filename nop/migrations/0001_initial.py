# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    app_label = 'nop'

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('timestamp', models.BigIntegerField(serialize=False, primary_key=True)),
                ('cart', models.IntegerField()),
                ('len', models.IntegerField(null=True, blank=True)),
                ('showtitle', models.CharField(max_length=765, blank=True)),
                ('title', models.CharField(max_length=765, blank=True)),
                ('artist', models.CharField(max_length=765, blank=True)),
                ('album', models.CharField(max_length=765, blank=True)),
                ('ismusic', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'db_table': 'master',
            },
        ),
        migrations.CreateModel(
            name='Standby',
            fields=[
                ('timestamp', models.BigIntegerField(serialize=False, primary_key=True)),
                ('cart', models.IntegerField()),
                ('len', models.IntegerField(null=True, blank=True)),
                ('showtitle', models.CharField(max_length=765, blank=True)),
                ('title', models.CharField(max_length=765, blank=True)),
                ('artist', models.CharField(max_length=765, blank=True)),
                ('album', models.CharField(max_length=765, blank=True)),
                ('ismusic', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'db_table': 'standby',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('timestamp', models.BigIntegerField(serialize=False, primary_key=True)),
                ('state', models.CharField(max_length=96, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'db_table': 'state',
            },
        ),
    ]
