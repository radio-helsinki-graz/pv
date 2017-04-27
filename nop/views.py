# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from models import Master, Standby, State
from program.models import TimeSlot

import json
import time
from datetime import datetime

DB = 'nop'

class NopForm(forms.Form):
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'id': 'nop_date', 'class': 'date'}))
    time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'id': 'nop_time', 'class': 'date'}))


def _dtstring(dt):
    return time.strftime('%Y-%m-%d %H:%M', dt)


def _which(timestamp=None):
    if timestamp:
        res = State.objects.using(DB).filter(timestamp__lt=timestamp)[0]
    else:
        res = State.objects.using(DB).all()[0]
    if not res or res.state == 'master':
        return Master
    else:
        return Standby


def _get_show(datetime=None):
    try:
        if datetime:
            timeslot = TimeSlot.objects.get(start__lte=datetime,
                                            end__gt=datetime)
        else:
            timeslot = TimeSlot.objects.get_or_create_current()
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return {'start': None, 'id': None, 'name': None}
    else:
        try:
            note = timeslot.note
        except ObjectDoesNotExist:
            note = None

        return {'start': _dtstring(timeslot.start.timetuple()),
                'id': timeslot.show.id,
                'name': timeslot.show.name,
                'note': note}


def _current():
    artist = None
    title = None
    album = None
    show = _get_show()

    if show['id'] in settings.MUSIKPROG_IDS \
            or (show['id'] in settings.SPECIAL_PROGRAM_IDS and not show['note']):
        result = _which().objects.using(DB).filter(carttype__exact='pool')[0]
        artist = result.artist
        title = result.title
        album = result.album

    return {'show': show['name'],
            'start': show['start'],
            'artist': artist,
            'title': title,
            'album': album}


def _bydate(year=None, month=None, day=None, hour=None, minute=None):
    show = _get_show(datetime(year, month, day, hour, minute))

    if show['id'] and show['id'] not in settings.MUSIKPROG_IDS:
        return [{'show': show['name'],
                 'start': show['start'],
                 'artist': None,
                 'title': None,
                 'album': None}]
    else:
        ts = int(time.mktime((int(year), int(month), int(day), int(hour),
                              int(minute), 0, 0, 0, -1))) * 1000000
        result = _which(ts).objects.using(DB).filter(carttype__exact='pool').filter(timestamp__lt=ts)[:5]
        return [{'show': show['name'],
                 'start': _dtstring(time.localtime(item.timestamp//1000000)),
                 'artist': item.artist,
                 'title': item.title,
                 'album': item.album} for item in result]


def get_current(request):
    response = json.dumps(_current())
    return HttpResponse(response, content_type='application/json')


def get(request, year=None, month=None, day=None, hour=None, minute=None):
    response = json.dumps(_bydate(year, month, day, hour, minute))
    return HttpResponse(response, content_type='application/json')


def nop_form(request):
    context = {}
    date = None
    time = None

    if request.method == 'GET' \
            and ('date' in request.GET or 'time' in request.GET):
        form = NopForm(request.GET)

        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
    else:
        form = NopForm(initial={'date': datetime.date(datetime.now()),
                                'time': datetime.time(datetime.now())})

    if not date:
        date = datetime.date(datetime.now())

    if not time:
        time = datetime.time(datetime.now())

    result = _bydate(date.year, date.month, date.day, time.hour, time.minute)
    context['nowplaying'] = result
    context['form'] = form
    return render_to_response('nop_form.html', context)
