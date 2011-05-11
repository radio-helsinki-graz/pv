from django.http import HttpResponse
from models import Master
import json
import time

def get_current(request):

    #current = int(time.time())*1000000
    #time.gmtime(Master.objects.using('nop').all()[6000].timestamp//1000000)
    # select all where timestamp < givenTS, get most recent one -> order DESC

    # reverse sorted. get the first object = last played
    result = Master.objects.using('nop').all()[0]
    response = json.dumps({'artist': result.artist, 'title': result.title})

    #return HttpResponse(response, mimetype='application/json')
    return HttpResponse(response, mimetype='text/plain')

def get(request, year=None, month=None, day=None, hour=None, minute=None):

    try:
        # tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst
        ts = int(time.mktime((
                int(year),
                int(month),
                int(day),
                int(hour),
                int(minute),0,0,0,-1))) * 1000000

        result = Master.objects.using('nop').filter(timestamp__lt=ts)[:5]
        response = json.dumps(
                [{'artist': item.artist, 'title': item.title, 'album': item.album,
                  'datetime': time.strftime('%Y-%m-%d %H:%M',
                      time.localtime(item.timestamp//1000000)),
                  'showtitle': item.showtitle} for item in result])
    except: # all errors
        response = ''

    #return HttpResponse(response, mimetype='application/json')
    return HttpResponse(response, mimetype='text/plain')
