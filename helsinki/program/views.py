from django.views.generic import list_detail
from django.views.generic import simple
from django.shortcuts import get_object_or_404

from helsinki.program.models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic, TimeSlot

from datetime import date, datetime, time, timedelta

def show_list(request):
    broadcastformats = BroadcastFormat.objects.all()
    musicfoci = MusicFocus.objects.all()
    showinformation = ShowInformation.objects.all()
    showtopics = ShowTopic.objects.all()

    extra_context = dict(broadcastformats=broadcastformats, musicfoci=musicfoci, showinformation=showinformation, showtopics=showtopics)
    
    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        queryset = Show.objects.filter(broadcastformat=broadcastformat)
    elif 'musicfocus' in request.GET:
        musicfocus = get_object_or_404(MusicFocus, slug=request.GET['musicfocus'])

        queryset = Show.objects.filter(musicfocus=musicfocus)
    elif 'showinformation' in request.GET:
        showinformation = get_object_or_404(ShowInformation, slug=request.GET['showinformation'])

        queryset = Show.objects.filter(showinformation=showinformation)
    elif 'showtopic' in request.GET:
        showtopic = get_object_or_404(ShowTopic, slug=request.GET['showtopic'])

        queryset = Show.objects.filter(showtopic=showtopic)
    else:
        queryset = Show.objects.all()


    return list_detail.object_list(request, queryset=queryset, extra_context=extra_context, template_object_name='show')

def recommendations(request, template_name='program/recommendations.html'):
    now = datetime.now()
    in_one_week = now + timedelta(weeks=1)

    queryset = Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:10]

    return list_detail.object_list(request, queryset=queryset, template_name=template_name, template_object_name='recommendation')

def today_schedule(request):
    now = datetime.now()
    today = datetime.combine(date.today(), time(6, 0))
    tomorrow = today + timedelta(days=1)

    broadcastformats = BroadcastFormat.objects.all()
    recommendations = Note.objects.filter(status=1, timeslot__start__range=(now, tomorrow))

    extra_context = dict(day=today, broadcastformats=broadcastformats, recommendations=recommendations)

    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        extra_context['timeslots'] = TimeSlot.objects.filter(start__range=(today, tomorrow), show__broadcastformat=broadcastformat)
    else:
        extra_context['timeslots'] = TimeSlot.objects.filter(start__range=(today, tomorrow))

    return simple.direct_to_template(request, extra_context=extra_context, template='program/day_schedule.html')

def day_schedule(request, year, month, day):
    this_day = datetime.strptime('%s__%s__%s__06__00' % (year, month, day), '%Y__%m__%d__%H__%M')
    that_day = this_day+timedelta(days=1)

    broadcastformats = BroadcastFormat.objects.all()
    recommendations = Note.objects.filter(status=1, timeslot__start__range=(this_day, that_day))

    extra_context = dict(day=this_day, broadcastformats=broadcastformats, recommendations=recommendations)

    if 'broadcastformat' in request.GET:
        broadcastformat = get_object_or_404(BroadcastFormat, slug=request.GET['broadcastformat'])

        extra_context['timeslots'] = TimeSlot.objects.filter(start__range=(this_day, that_day), show__broadcastformat=broadcastformat)
    else:
        extra_context['timeslots'] = TimeSlot.objects.filter(start__range=(this_day, that_day))

    return simple.direct_to_template(request, extra_context=extra_context, template='program/day_schedule.html')

def current_show(request):
    current = TimeSlot.objects.get_or_create_current()
    next = current.get_next_by_start()
    after_next = next.get_next_by_start()

    extra_context = dict(current=current, next=next, after_next=after_next)

    return simple.direct_to_template(request, template='program/current_box.html', extra_context=extra_context)

def week_schedule(request, year, week):
    monday = datetime.strptime('%s__%s__1__06__00' % (year, week), '%Y__%W__%w__%H__%M')
    tuesday = monday+timedelta(days=1)
    wednesday = monday+timedelta(days=2)
    thursday = monday+timedelta(days=3)
    friday = monday+timedelta(days=4)
    saturday = monday+timedelta(days=5)
    sunday = monday+timedelta(days=6)
    next_monday = monday+timedelta(days=7)

    extra_context = dict(monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)

    extra_context['monday_timeslots'] = TimeSlot.objects.filter(start__range=(monday, tuesday))
    extra_context['tuesday_timeslots'] = TimeSlot.objects.filter(start__range=(tuesday, wednesday))
    extra_context['wednesday_timeslots'] = TimeSlot.objects.filter(start__range=(wednesday, thursday))
    extra_context['thursday_timeslots'] = TimeSlot.objects.filter(start__range=(thursday, friday))
    extra_context['friday_timeslots'] = TimeSlot.objects.filter(start__range=(friday, saturday))
    extra_context['saturday_timeslots'] = TimeSlot.objects.filter(start__range=(saturday, sunday))
    extra_context['sunday_timeslots'] = TimeSlot.objects.filter(start__range=(sunday, next_monday))

    return simple.direct_to_template(request, template='program/week_schedule.html', extra_context=extra_context)
