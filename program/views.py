from django.views.generic import list_detail, simple
from django.shortcuts import get_object_or_404

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic, TimeSlot

from datetime import date, datetime, time, timedelta

def show_list(request):
    queryset = Show.objects.exclude(id=1)

    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        queryset = queryset.filter(broadcastformat=broadcastformat)
    elif 'musicfocus' in request.GET:
        musicfocus = get_object_or_404(MusicFocus, slug=request.GET['musicfocus'])

        queryset = queryset.filter(musicfocus=musicfocus)
    elif 'showinformation' in request.GET:
        showinformation = get_object_or_404(ShowInformation, slug=request.GET['showinformation'])

        queryset = queryset.exfilter(showinformation=showinformation)
    elif 'showtopic' in request.GET:
        showtopic = get_object_or_404(ShowTopic, slug=request.GET['showtopic'])

        queryset = queryset.filter(showtopic=showtopic)
    
    return list_detail.object_list(request, queryset=queryset, template_object_name='show')

def recommendations(request, template_name='program/recommendations.html'):
    now = datetime.now()
    in_one_week = now + timedelta(weeks=1)

    queryset = Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:10]

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

    return simple.direct_to_template(request, extra_context=extra_context, template='program/day_schedule.html')

def current_show(request):
    current = TimeSlot.objects.get_or_create_current()
    next = current.get_next_by_start()
    after_next = next.get_next_by_start()

    extra_context = dict(current=current, next=next, after_next=after_next)

    return simple.direct_to_template(request, template='program/boxes/current.html', extra_context=extra_context)

def week_schedule(request, year=None, week=None):
    if year is None and week is None:
        year, week = datetime.strftime(datetime.today(), '%Y__%W').split('__')

    monday = datetime.strptime('%s__%s__1__06__00' % (year, week), '%Y__%W__%w__%H__%M')

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

    return simple.direct_to_template(request, template='program/week_schedule.html', extra_context=extra_context)
