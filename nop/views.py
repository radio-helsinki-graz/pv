from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from models import Master, Standby, State
from program.models import TimeSlot

import json
import time
from datetime import datetime

DB = 'nop'
MUSIKPROG_IDS = (1,17,60,81)
        # 1 - unmodieriertes musikprogramm
        # 17 - bumbumtschak
        # 60 - musikprogramm bunt gemischt
        # 81 - selchfleisch

class NopForm(forms.Form):
    date = forms.DateField(
            required=True,
            initial=datetime.date(datetime.now()),
            widget=forms.DateInput(
                format='%Y-%m-%d',
                attrs={'id':'nop_date', 'class':'date'})
            )
    time = forms.TimeField(
            required=True,
            initial=datetime.time(datetime.now()),
            widget=forms.TimeInput(
                format='%H:%M',
                attrs={'id':'nop_time', 'class':'date'})
            )

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

def _get_show(datetime = None):
    try:
        if datetime:
            timeslot = TimeSlot.objects.get(start__lte=datetime, end__gt=datetime)
        else:
            timeslot = TimeSlot.objects.get_or_create_current()
        return {'start': _dtstring(timeslot.start.timetuple()),
                'id': timeslot.show.id,
                'name': timeslot.show.name}
    except: # e.g. DoesNotExist
        return {'start': None, 'id': None, 'name': None}


def _current():
    #current = int(time.time())*1000000
    #time.gmtime(_which().objects.using(DB).all()[6000].timestamp//1000000)
    # select all where timestamp < givenTS, get most recent one -> order DESC

    artist = None
    title = None
    album = None
    show = _get_show()
    if show['id'] in MUSIKPROG_IDS:
        # reverse sorted. get the first object = last played
        result = _which().objects.using(DB).all()[0]
        artist = result.artist
        title = result.title
        album = result.album
    return {'show': show['name'],
            'start': show['start'],
            'artist': artist,
            'title': title,
            'album': album}

def _bydate(year=None, month=None, day=None, hour=None, minute=None):
    #try:
        #import pdb;pdb.set_trace()
        show = _get_show(datetime(year, month, day, hour, minute))
        if show['id'] and show['id'] not in MUSIKPROG_IDS:
            return [{'show': show['name'],
                     'start': show['start'],
                     'artist': None,
                     'title': None,
                     'album': None}]
        else:
            # tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst
            ts = int(time.mktime((
                 int(year),
                 int(month),
                 int(day),
                 int(hour),
                 int(minute),0,0,0,-1))) * 1000000
            result = _which(ts).objects.using(DB).filter(timestamp__lt=ts)[:5]
            return [{'show': show['name'],
                     'start': _dtstring(time.localtime(item.timestamp//1000000)),
                     'artist': item.artist,
                     'title': item.title,
                     'album': item.album} for item in result]
    #except: # all errors
    #    return None


def get_current(request):
    response = json.dumps(_current())

    return HttpResponse(response, mimetype='application/json')
    #return HttpResponse(response, mimetype='text/plain')

def get(request, year=None, month=None, day=None, hour=None, minute=None):
    response = json.dumps(_bydate(year, month, day, hour, minute))

    return HttpResponse(response, mimetype='application/json')
    #return HttpResponse(response, mimetype='text/plain')


def nop_form(request):
    context = {}
    # currently no csrf security for nicier forms 
    #context.update(csrf(request)) # in django template: {% csrf_token %}
    date = None
    time = None
    if request.method == 'GET' and\
            ('date' in request.GET or 'time' in request.GET):
        form = NopForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
    else:
        form = NopForm()
    if not date: date = datetime.date(datetime.now())
    if not time: time = datetime.time(datetime.now())
    result = _bydate(date.year, date.month, date.day, time.hour, time.minute)
    context['nowplaying'] = result
    context['form'] = form
    return render_to_response('nop_form.html', context)
