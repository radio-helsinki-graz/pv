from django.views.generic import list_detail, simple
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic, TimeSlot

from datetime import date, datetime, time, timedelta

import json

def show_list(request):
    queryset = Show.objects.filter(programslots__until__gt=date.today()).exclude(id=1).distinct()

    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        queryset = queryset.filter(broadcastformat=broadcastformat)
    elif 'musicfocus' in request.GET:
        musicfocus = get_object_or_404(MusicFocus, slug=request.GET['musicfocus'])

        queryset = queryset.filter(musicfocus=musicfocus)
    elif 'showinformation' in request.GET:
        showinformation = get_object_or_404(ShowInformation, slug=request.GET['showinformation'])

        queryset = queryset.filter(showinformation=showinformation)
    elif 'showtopic' in request.GET:
        showtopic = get_object_or_404(ShowTopic, slug=request.GET['showtopic'])

        queryset = queryset.filter(showtopic=showtopic)

    return list_detail.object_list(request, queryset=queryset, template_object_name='show', template_name='show_list.html')

def recommendations(request, template_name='recommendations.html'):
    now = datetime.now()
    end = now + timedelta(weeks=1)

    queryset = TimeSlot.objects.filter(Q(note__isnull=False, note__status=1, start__range=(now, end)) |
                                       Q(show__broadcastformat__slug='sondersendung', start__range=(now, end))).order_by('start')[:20]
    return list_detail.object_list(request, queryset=queryset, template_name=template_name, template_object_name='recommendation')

def day_schedule(request, year=None, month=None, day=None):
    if year is None and month is None and day is None:
        today = datetime.combine(date.today(), time(6, 0))
    else:
        today = datetime.strptime('%s__%s__%s__06__00' % (year, month, day), '%Y__%m__%d__%H__%M')

    tomorrow = today+timedelta(days=1)

    recommendations = Note.objects.filter(status=1, timeslot__start__range=(today, tomorrow))

    default_show = Show.objects.get(pk=1)

    extra_context = dict(day=today, recommendations=recommendations, default_show=default_show)

    timeslots = TimeSlot.objects.get_day_timeslots(today)

    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        extra_context['timeslots'] = timeslots.filter(show__broadcastformat=broadcastformat)
    elif 'musicfocus' in request.GET:
        musicfocus = get_object_or_404(MusicFocus, slug=request.GET['musicfocus'])

        extra_context['timeslots'] = timeslots.filter(show__musicfocus=musicfocus)
    elif 'showinformation' in request.GET:
        showinformation = get_object_or_404(ShowInformation, slug=request.GET['showinformation'])

        extra_context['timeslots'] = timeslots.filter(show__showinformation=showinformation)
    elif 'showtopic' in request.GET:
        showtopic = get_object_or_404(ShowTopic, slug=request.GET['showtopic'])

        extra_context['showtopic'] = timeslots.filter(show__showtopic=showtopic)
    else:
        extra_context['timeslots'] = timeslots

    return simple.direct_to_template(request, extra_context=extra_context, template='day_schedule.html')

def current_show(request):
    current = TimeSlot.objects.get_or_create_current()
    previous = current.get_previous_by_start()
    next = current.get_next_by_start()
    after_next = next.get_next_by_start()

    extra_context = dict(current=current,
            previous=previous,
            next=next,
            after_next=after_next)

    return simple.direct_to_template(request, template='boxes/current.html', extra_context=extra_context)

def week_schedule(request, year=None, week=None):
    if year is None and week is None:
        year, week = datetime.strftime(datetime.now(), '%G__%V').split('__')

    monday = tofirstdayinisoweek(int(year), int(week))
    tuesday = monday+timedelta(days=1)
    wednesday = monday+timedelta(days=2)
    thursday = monday+timedelta(days=3)
    friday = monday+timedelta(days=4)
    saturday = monday+timedelta(days=5)
    sunday = monday+timedelta(days=6)

    default_show = Show.objects.get(pk=1)

    extra_context = dict(monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday, default_show=default_show)

    extra_context['monday_timeslots'] = TimeSlot.objects.get_day_timeslots(monday)
    extra_context['tuesday_timeslots'] = TimeSlot.objects.get_day_timeslots(tuesday)
    extra_context['wednesday_timeslots'] = TimeSlot.objects.get_day_timeslots(wednesday)
    extra_context['thursday_timeslots'] = TimeSlot.objects.get_day_timeslots(thursday)
    extra_context['friday_timeslots'] = TimeSlot.objects.get_day_timeslots(friday)
    extra_context['saturday_timeslots'] = TimeSlot.objects.get_day_timeslots(saturday)
    extra_context['sunday_timeslots'] = TimeSlot.objects.get_day_timeslots(sunday)

    extra_context['last_w'] = datetime.strftime(monday-timedelta(days=7), '%G/%V')
    extra_context['cur_w'] = datetime.strftime(monday, '%G/%V')
    extra_context['next_w1'] = datetime.strftime(monday+timedelta(days=7), '%G/%V')
    extra_context['next_w2'] = datetime.strftime(monday+timedelta(days=14), '%G/%V')
    extra_context['next_w3'] = datetime.strftime(monday+timedelta(days=21), '%G/%V')
    extra_context['next_w4'] = datetime.strftime(monday+timedelta(days=28), '%G/%V')

    return simple.direct_to_template(request, template='week_schedule.html', extra_context=extra_context)

def styles(request):
    extra_context = dict()
    extra_context['broadcastformats'] = BroadcastFormat.objects.filter(enabled=True)
    extra_context['musicfocus'] = MusicFocus.objects.all()
    extra_context['showinformation'] = ShowInformation.objects.all()
    extra_context['showtopic'] = ShowTopic.objects.all()
    return simple.direct_to_template(request, template='styles.css', mimetype='text/css', extra_context=extra_context)

def json_day_schedule(request, year=None, month=None, day=None):
    if year is None and month is None and day is None:
        today = datetime.combine(date.today(), time(0, 0))
    else:
        today = datetime.strptime('%s__%s__%s__00__00' % (year, month, day), '%Y__%m__%d__%H__%M')

    timeslots = TimeSlot.objects.get_24h_timeslots(today)
    schedule = []
    for ts in timeslots:
        if ts.programslot.automation_id:
            schedule.append((ts.start.strftime('%H:%M:%S'), ts.programslot.show.name, ts.programslot.automation_id))
        elif ts.programslot.show.automation_id:
            schedule.append((ts.start.strftime('%H:%M:%S'), ts.programslot.show.name, ts.programslot.show.automation_id))
        else:
            schedule.append((ts.start.strftime('%H:%M:%S'), ts.programslot.show.name, -1))

    return HttpResponse(json.dumps(schedule), content_type="application/json; charset=utf-8")

def tofirstdayinisoweek(year, week):
    # http://stackoverflow.com/questions/5882405/get-date-from-iso-week-number-in-python
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret
