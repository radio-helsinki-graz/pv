from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from models import Master
import json
import time
from datetime import datetime

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


def _current():
    #current = int(time.time())*1000000
    #time.gmtime(Master.objects.using('nop').all()[6000].timestamp//1000000)
    # select all where timestamp < givenTS, get most recent one -> order DESC

    # reverse sorted. get the first object = last played
    result = Master.objects.using('nop').all()[0]
    return {'artist': result.artist, 'title': result.title}

def _bydate(year=None, month=None, day=None, hour=None, minute=None):
    try:
        # tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst
        ts = int(time.mktime((
                int(year),
                int(month),
                int(day),
                int(hour),
                int(minute),0,0,0,-1))) * 1000000

        result = Master.objects.using('nop').filter(timestamp__lt=ts)[:5]
        return [{'artist': item.artist, 'title': item.title, 'album': item.album,
                   'datetime': time.strftime('%Y-%m-%d %H:%M',
                       time.localtime(item.timestamp//1000000)),
                   'showtitle': item.showtitle} for item in result]
    except: # all errors
        return None


def get_current(request):
    response = json.dumps(_current())

    #return HttpResponse(response, mimetype='application/json')
    return HttpResponse(response, mimetype='text/plain')

def get(request, year=None, month=None, day=None, hour=None, minute=None):
    response = json.dumps(_bydate(year, month, day, hour, minute))

    #return HttpResponse(response, mimetype='application/json')
    return HttpResponse(response, mimetype='text/plain')


def nop_form(request):
    context = {}
    context.update(csrf(request))
    date = None
    time = None
    if request.method == 'POST':
        form = NopForm(request.POST)
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
