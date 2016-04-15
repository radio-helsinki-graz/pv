# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('format', models.CharField(max_length=32, verbose_name='Format')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('color', models.CharField(default=b'#ffffff', max_length=7, verbose_name='Color')),
                ('text_color', models.CharField(default=b'#000000', max_length=7, verbose_name='Text color')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
            options={
                'ordering': ('format',),
                'verbose_name': 'Broadcast format',
                'verbose_name_plural': 'Broadcast formats',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail', blank=True)),
                ('website', models.URLField(verbose_name='Website', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
        ),
        migrations.CreateModel(
            name='MusicFocus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('focus', models.CharField(max_length=32, verbose_name='Focus')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('focus',),
                'verbose_name': 'Music focus',
                'verbose_name_plural': 'Music focus',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', tinymce.models.HTMLField(verbose_name='Content')),
                ('status', models.IntegerField(default=1, verbose_name='Status', choices=[(0, 'Cancellation'), (1, 'Recommendation'), (2, 'Repetition')])),
                ('cba_entry_id', models.IntegerField(null=True, verbose_name='CBA entry ID', blank=True)),
                ('start', models.DateTimeField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('timeslot',),
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='ProgramSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('byweekday', models.IntegerField(verbose_name='Weekday', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('dstart', models.DateField(verbose_name='First date')),
                ('tstart', models.TimeField(verbose_name='Start time')),
                ('tend', models.TimeField(verbose_name='End time')),
                ('until', models.DateField(verbose_name='Last date')),
                ('is_repetition', models.BooleanField(default=False, verbose_name='Is repetition')),
                ('automation_id', models.IntegerField(blank=True, null=True, verbose_name='Automation ID', choices=[])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('dstart', 'tstart'),
                'verbose_name': 'Program slot',
                'verbose_name_plural': 'Program slots',
            },
        ),
        migrations.CreateModel(
            name='RRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name='Name')),
                ('freq', models.IntegerField(verbose_name='Frequency', choices=[(1, 'Monthly'), (2, 'Weekly'), (3, 'Daily')])),
                ('interval', models.IntegerField(default=1, verbose_name='Interval')),
                ('bysetpos', models.IntegerField(blank=True, null=True, verbose_name='Set position', choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (-1, 'Last')])),
                ('count', models.IntegerField(null=True, verbose_name='Count', blank=True)),
            ],
            options={
                'ordering': ('-freq', 'interval', 'bysetpos'),
                'verbose_name': 'Recurrence rule',
                'verbose_name_plural': 'Recurrence rules',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.CharField(unique=True, max_length=255, verbose_name='Slug')),
                ('image', models.ImageField(upload_to=b'show_images', null=True, verbose_name='Image', blank=True)),
                ('image_enabled', models.BooleanField(default=True, verbose_name='show Image')),
                ('short_description', models.CharField(max_length=64, verbose_name='Short description')),
                ('description', tinymce.models.HTMLField(null=True, verbose_name='Description', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='E-Mail', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('cba_series_id', models.IntegerField(null=True, verbose_name='CBA series ID', blank=True)),
                ('automation_id', models.IntegerField(blank=True, null=True, verbose_name='Automation ID', choices=[])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('broadcastformat', models.ForeignKey(related_name='shows', verbose_name='Broadcast format', to='program.BroadcastFormat')),
                ('hosts', models.ManyToManyField(related_name='shows', verbose_name='Hosts', to='program.Host', blank=True)),
                ('musicfocus', models.ManyToManyField(related_name='shows', verbose_name='Music focus', to='program.MusicFocus', blank=True)),
                ('owners', models.ManyToManyField(related_name='shows', verbose_name='Owners', to=settings.AUTH_USER_MODEL, blank=True)),
                ('predecessor', models.ForeignKey(related_name='successors', verbose_name='Predecessor', blank=True, to='program.Show', null=True)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name': 'Show',
                'verbose_name_plural': 'Shows',
            },
        ),
        migrations.CreateModel(
            name='ShowInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('information', models.CharField(max_length=32, verbose_name='Information')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('information',),
                'verbose_name': 'Show information',
                'verbose_name_plural': 'Show information',
            },
        ),
        migrations.CreateModel(
            name='ShowTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=32, verbose_name='Show topic')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('topic',),
                'verbose_name': 'Show topic',
                'verbose_name_plural': 'Show topics',
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(unique=True, verbose_name='Start time')),
                ('end', models.DateTimeField(verbose_name='End time')),
                ('programslot', models.ForeignKey(related_name='timeslots', verbose_name='Program slot', to='program.ProgramSlot')),
                ('show', models.ForeignKey(related_name='timeslots', editable=False, to='program.Show')),
            ],
            options={
                'ordering': ('start', 'end'),
                'verbose_name': 'Time slot',
                'verbose_name_plural': 'Time slots',
            },
        ),
        migrations.AddField(
            model_name='show',
            name='showinformation',
            field=models.ManyToManyField(related_name='shows', verbose_name='Show information', to='program.ShowInformation', blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='showtopic',
            field=models.ManyToManyField(related_name='shows', verbose_name='Show topic', to='program.ShowTopic', blank=True),
        ),
        migrations.AddField(
            model_name='programslot',
            name='rrule',
            field=models.ForeignKey(related_name='programslots', verbose_name='Recurrence rule', to='program.RRule'),
        ),
        migrations.AddField(
            model_name='programslot',
            name='show',
            field=models.ForeignKey(related_name='programslots', verbose_name='Show', to='program.Show'),
        ),
        migrations.AddField(
            model_name='note',
            name='show',
            field=models.ForeignKey(related_name='notes', editable=False, to='program.Show'),
        ),
        migrations.AddField(
            model_name='note',
            name='timeslot',
            field=models.OneToOneField(verbose_name='Time slot', to='program.TimeSlot'),
        ),
        migrations.AlterUniqueTogether(
            name='programslot',
            unique_together=set([('rrule', 'byweekday', 'dstart', 'tstart')]),
        ),
    ]
