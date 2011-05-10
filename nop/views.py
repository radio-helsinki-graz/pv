from django.http import HttpResponse
from models import Master
import json
#import time
#from datetime import date, datetime, time, timedelta

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
    #if year is None and month is None and day is None:
    #    today = datetime.combine(date.today(), time(6, 0))
    #else:
    #    today = datetime.strptime('%s__%s__%s__06__00' % (year, month, day), '%Y__%m__%d__%H__%M')
    return None

